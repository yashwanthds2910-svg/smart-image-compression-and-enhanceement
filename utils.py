import os
import torch
import torch.nn.functional as F
from torchvision.utils import make_grid, save_image
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as sk_psnr
from skimage.metrics import structural_similarity as sk_ssim

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_checkpoint(state, path):
    ensure_dir(os.path.dirname(path))
    torch.save(state, path)

def calc_psnr_batch(output, target):
    # detach → move to cpu → convert to numpy
    output_np = output.detach().clamp(0,1).cpu().numpy()
    target_np = target.detach().clamp(0,1).cpu().numpy()

    ps_list = []
    for i in range(output_np.shape[0]):
        ps_val = sk_psnr(
            target_np[i].transpose(1,2,0),
            output_np[i].transpose(1,2,0),
            data_range=1.0
        )
        ps_list.append(ps_val)
    return float(np.mean(ps_list))

def calc_ssim_batch(output, target, window_size=11):
    # output, target: (B, C, H, W), in [0,1]
    output = output.detach()
    target = target.detach()

    # Gaussian window
    def gaussian_window(window_size, sigma=1.5):
        coords = torch.arange(window_size).float() - window_size//2
        g = torch.exp(-(coords**2) / (2*sigma**2))
        g = g / g.sum()
        return g.unsqueeze(0) * g.unsqueeze(1)  # (w,w)

    B, C, H, W = output.shape
    window = gaussian_window(window_size).to(output.device)
    window = window.expand(C, 1, window_size, window_size)

    mu_x = F.conv2d(output, window, padding=window_size//2, groups=C)
    mu_y = F.conv2d(target, window, padding=window_size//2, groups=C)

    mu_x2 = mu_x**2
    mu_y2 = mu_y**2
    mu_xy = mu_x * mu_y

    sigma_x2 = F.conv2d(output * output, window, padding=window_size//2, groups=C) - mu_x2
    sigma_y2 = F.conv2d(target * target, window, padding=window_size//2, groups=C) - mu_y2
    sigma_xy = F.conv2d(output * target, window, padding=window_size//2, groups=C) - mu_xy

    C1 = 0.01**2
    C2 = 0.03**2

    ssim_map = ((2*mu_xy + C1)*(2*sigma_xy + C2)) / (
        (mu_x2 + mu_y2 + C1)*(sigma_x2 + sigma_y2 + C2)
    )

    # reduce over H,W then mean over batch
    return ssim_map.mean([1,2,3]).mean().item()



def latents_to_bpp(bits_per_sample, image_h, image_w):
    """
    Convert estimated bits-per-sample (bits for latent representation) to bits-per-pixel (bpp).
    bits_per_sample: tensor or numpy array (B,)
    image_h, image_w: spatial dims of original image (e.g., 128,128)
    returns: bpp per sample (same shape)
    """
    num_pixels = image_h * image_w
    # bits_per_sample already in bits (sum over latent elements), bpp = bits / pixels
    bpp = bits_per_sample / float(num_pixels)
    return bpp

def add_image_to_tensorboard(writer, tag, tensor_batch, step, nrow=4):
    # tensor_batch: (B,C,H,W)
    grid = make_grid(tensor_batch, nrow=nrow, normalize=True)
    writer.add_image(tag, grid, step)
