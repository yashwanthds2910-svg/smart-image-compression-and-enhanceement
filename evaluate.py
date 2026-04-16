import argparse
import torch
from src.models.compression_net import CompressionNet
from src.models.entropy_model import EntropyModel
from src.utils import calc_psnr_batch, calc_ssim_batch, latents_to_bpp
from src.data import get_dataloader

def evaluate(ckpt, data_folder="data/patches"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # create model + entropy
    model = CompressionNet()
    entropy = EntropyModel()
    data = torch.load(ckpt, map_location=device)
    if "state_dict" in data:
        model.load_state_dict(data["state_dict"])
    if "entropy" in data:
        try:
            entropy.load_state_dict(data["entropy"])
        except Exception:
            pass
    model.to(device).eval()
    entropy.to(device).eval()

    dl = get_dataloader(folder=data_folder, batch_size=8)
    psnr_list, ssim_list, bpp_list = [], [], []
    with torch.no_grad():
        for inp, tgt in dl:
            inp = inp.to(device)
            tgt = tgt.to(device)
            out, lat = model(inp)
            psnr_list.append(calc_psnr_batch(out, tgt))
            ssim_list.append(calc_ssim_batch(out, tgt))
            bits_per_sample, _ = entropy(lat)
            bpp = latents_to_bpp(bits_per_sample.cpu(), inp.shape[2], inp.shape[3])
            bpp_list.append(float(bpp.mean()))

    print("Avg PSNR:", sum(psnr_list)/len(psnr_list))
    print("Avg SSIM:", sum(ssim_list)/len(ssim_list))
    print("Avg bpp:", sum(bpp_list)/len(bpp_list))

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--data", default="data/patches")
    args=p.parse_args()
    evaluate(args.ckpt, args.data)
