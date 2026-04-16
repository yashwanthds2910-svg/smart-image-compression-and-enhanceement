# prepares small patches from images for training
import os, argparse
from PIL import Image
import random

def extract_patches(root_in, root_out, patch_size=128, patches_per_image=8):
    os.makedirs(root_out, exist_ok=True)
    files = [os.path.join(root_in, f) for f in os.listdir(root_in) if f.lower().endswith(('.png','.jpg','.jpeg'))]
    count = 0

    for f in files:
        img = Image.open(f).convert("RGB")
        w, h = img.size

        for _ in range(patches_per_image):
            if w < patch_size or h < patch_size:
                continue

            x = random.randint(0, w - patch_size)
            y = random.randint(0, h - patch_size)

            patch = img.crop((x, y, x + patch_size, y + patch_size))
            patch.save(os.path.join(root_out, f"patch_{count:06d}.png"))
            count += 1

    print(f"Saved {count} patches to {root_out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in_dir", default="data/sample_images")
    p.add_argument("--out_dir", default="data/patches")
    p.add_argument("--patch_size", type=int, default=128)
    p.add_argument("--ppimg", type=int, default=8)
    args = p.parse_args()

    extract_patches(args.in_dir, args.out_dir, args.patch_size, args.ppimg)
