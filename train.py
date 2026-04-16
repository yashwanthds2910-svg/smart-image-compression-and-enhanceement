import os
import argparse
import yaml
import torch
import torch.nn as nn
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

from src.data import get_dataloader
from src.models.compression_net import CompressionNet
from src.models.entropy_model import EntropyModel
from src.utils import save_checkpoint, ensure_dir, calc_psnr_batch, calc_ssim_batch, latents_to_bpp, add_image_to_tensorboard

def train(cfg):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    batch = cfg["train"]["batch_size"]
    patch = cfg["train"]["patch_size"]

    dataloader = get_dataloader(folder="data/patches", batch_size=batch, patch_size=patch)

    model = CompressionNet(latent_dim=cfg["model"]["latent_dim"]).to(device)
    entropy = EntropyModel(latent_dim=cfg["model"]["latent_dim"]).to(device)

    opt = torch.optim.Adam(list(model.parameters()) + list(entropy.parameters()), lr=float(cfg["train"]["lr"]))
    loss_fn = nn.L1Loss()

    save_dir = cfg["train"]["save_dir"]
    ensure_dir(save_dir)

    tb_dir = os.path.join(save_dir, "tb")
    writer = SummaryWriter(tb_dir)

    global_step = 0

    for epoch in range(cfg["train"]["epochs"]):
        model.train()
        epoch_loss = 0.0

        pbar = tqdm(enumerate(dataloader), total=len(dataloader), desc=f"Epoch {epoch+1}")
        for i, (inp, tgt) in pbar:
            inp = inp.to(device)
            tgt = tgt.to(device)

            out, lat = model(inp)
            bits_per_sample, bits_per_elem = entropy(lat.detach())  # predict bits (learnable)
            # compute rate as mean bits-per-sample
            rate = bits_per_sample.mean()

            rec_loss = loss_fn(out, tgt)
            loss = rec_loss + 1e-3 * rate  # scale rate (adjustable)

            opt.zero_grad()
            loss.backward()
            opt.step()

            epoch_loss += loss.item()
            global_step += 1

            if global_step % cfg.get("logging", {}).get("log_interval", 50) == 0:
                # metrics on batch
                psnr_b = calc_psnr_batch(out, tgt)
                ssim_b = calc_ssim_batch(out, tgt)
                # convert bits->bpp per sample for display (image size equals patch)
                bpp = latents_to_bpp(bits_per_sample.detach().cpu(), inp.shape[2], inp.shape[3])
                pbar.set_postfix({"loss": loss.item(), "rec": rec_loss.item(), "rate": float(rate.item()), "psnr": psnr_b})

                writer.add_scalar("train/loss", loss.item(), global_step)
                writer.add_scalar("train/rec_loss", rec_loss.item(), global_step)
                writer.add_scalar("train/rate_bits", float(rate.item()), global_step)
                writer.add_scalar("train/psnr", psnr_b, global_step)
                writer.add_scalar("train/ssim", ssim_b, global_step)
                writer.add_scalar("train/bpp", float(bpp.mean()), global_step)

        avg_loss = epoch_loss / len(dataloader)
        # Quick validation on first batch
        model.eval()
        with torch.no_grad():
            sample_inp, sample_tgt = next(iter(dataloader))
            sample_inp = sample_inp.to(device)
            sample_tgt = sample_tgt.to(device)
            sample_out, sample_lat = model(sample_inp)
            psnr_val = calc_psnr_batch(sample_out, sample_tgt)
            ssim_val = calc_ssim_batch(sample_out, sample_tgt)
            bits_per_sample, _ = entropy(sample_lat)
            bpp = latents_to_bpp(bits_per_sample.detach().cpu(), sample_inp.shape[2], sample_inp.shape[3])

        print(f"Epoch {epoch+1} | AvgLoss={avg_loss:.4f} | PSNR={psnr_val:.2f} | SSIM={ssim_val:.4f} | BPP={float(bpp.mean()):.6f}")
        # write images to tensorboard
        add_image_to_tensorboard(writer, "val/input", sample_inp, epoch+1)
        add_image_to_tensorboard(writer, "val/output", sample_out, epoch+1)
        writer.add_scalar("val/psnr", psnr_val, epoch+1)
        writer.add_scalar("val/ssim", ssim_val, epoch+1)
        writer.add_scalar("val/bpp", float(bpp.mean()), epoch+1)

        # save checkpoint
        save_checkpoint({"epoch": epoch+1, "state_dict": model.state_dict(), "entropy": entropy.state_dict()},
                        os.path.join(save_dir, f"ckpt_epoch{epoch+1}.pth"))

    writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    cfg = yaml.safe_load(open(args.config, "r"))
    # ensure numeric lr
    cfg["train"]["lr"] = float(cfg["train"]["lr"])
    if "logging" not in cfg:
        cfg["logging"] = {"log_interval": 50}
    train(cfg)
