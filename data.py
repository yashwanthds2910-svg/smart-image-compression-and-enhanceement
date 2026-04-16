import os
from PIL import Image, ImageFilter
import random
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

def add_noise(img_tensor, sigma=0.05):
    noise = torch.randn_like(img_tensor) * sigma
    return torch.clamp(img_tensor + noise, 0.0, 1.0)

def add_motion_blur_pil(img: Image.Image, radius=3):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

class PatchDataset(Dataset):
    def __init__(self, folder, patch_size=128, transform=None, corrupt_prob=0.9):
        self.files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png','.jpg'))]
        self.transform = transform or transforms.Compose([transforms.ToTensor()])
        self.patch_size = patch_size
        self.corrupt_prob = corrupt_prob

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        p = self.files[idx]
        img = Image.open(p).convert("RGB")

        w, h = img.size
        if w < self.patch_size or h < self.patch_size:
            img = img.resize((self.patch_size, self.patch_size))
        else:
            left = (w - self.patch_size)//2
            top = (h - self.patch_size)//2
            img = img.crop((left, top, left+self.patch_size, top+self.patch_size))

        clean = self.transform(img)
        corrupted = clean.clone()

        if random.random() < 0.5:
            pil_blurred = add_motion_blur_pil(img, radius=random.uniform(0.5,2.5))
            corrupted = self.transform(pil_blurred)

        if random.random() < 0.5:
            corrupted = add_noise(corrupted, sigma=random.uniform(0.01,0.08))

        return corrupted, clean

def get_dataloader(folder="data/patches", batch_size=8, patch_size=128, shuffle=True):
    ds = PatchDataset(folder, patch_size=patch_size)
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, num_workers=0)
