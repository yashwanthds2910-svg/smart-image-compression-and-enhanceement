import torch
import torch.nn as nn
import torch.nn.functional as F

class CompressionNet(nn.Module):
    def __init__(self, latent_dim=128):
        super().__init__()
        # Encoder
        self.enc = nn.Sequential(
            nn.Conv2d(3, 32, 4, 2, 1),  # 128 -> 64
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2, 1),  # 64 -> 32
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, 2, 1),  # 32 -> 16
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, latent_dim)
        )

        # Decoder
        self.dec_fc = nn.Linear(latent_dim, 128 * 4 * 4)
        self.dec = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, 2, 1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 4, 2, 1),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 3, 4, 2, 1),
            nn.Sigmoid()
        )

    def forward(self, x, quantize=False):
        """
        x: (B,3,H,W)
        quantize: unused placeholder (kept for interface compatibility)
        returns: reconstructed image (B,3,H,W), latents (B,L)
        """
        z = self.enc(x)  # (B, latent_dim)
        zq = z  # placeholder for quantization (no hard quantization in beginner version)
        xhat = self.dec_fc(zq)
        xhat = xhat.view(x.size(0), 128, 4, 4)
        xhat = self.dec(xhat)
        xhat = F.interpolate(xhat, size=(x.shape[2], x.shape[3]), mode='bilinear', align_corners=False)
        return xhat, zq
