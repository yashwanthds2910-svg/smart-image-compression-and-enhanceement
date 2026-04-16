"""
EntropyModel
-------------
Simple practical entropy estimator used for quick bitrate estimates.
This is not a full arithmetic coder; it's an estimator that learns
to predict per-latent bit-costs. It returns per-sample estimated bits.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class EntropyModel(nn.Module):
    def __init__(self, latent_dim=128):
        super().__init__()
        # small predictor: maps latent vector -> estimated bits per latent element
        self.net = nn.Sequential(
            nn.Linear(latent_dim, latent_dim // 2),
            nn.ReLU(),
            nn.Linear(latent_dim // 2, latent_dim),
            nn.Softplus()  # positive estimated "cost" per element
        )

    def forward(self, latents):
        """
        latents: tensor (B, L) where L is latent_dim
        returns: per-sample estimated bits (B,) and per-element predicted bits (B,L)
        """
        # predict positive cost per latent element
        bits_per_elem = self.net(latents)  # (B, L) positive values
        # sum to get bits per latent vector
        bits_per_sample = bits_per_elem.sum(dim=1)
        return bits_per_sample, bits_per_elem
