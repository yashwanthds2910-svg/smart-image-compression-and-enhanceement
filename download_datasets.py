import os
from PIL import Image
import numpy as np

OUT_DIR = "data/sample_images"

def generate_image(w=256, h=256):
    arr = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
    return Image.fromarray(arr)

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Generating offline sample images...")

    for i in range(50):
        img = generate_image()
        img.save(os.path.join(OUT_DIR, f"img_{i:04d}.png"))

    print("✔ Saved 50 offline images to", OUT_DIR)
