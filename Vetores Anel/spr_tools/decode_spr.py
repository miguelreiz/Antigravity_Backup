import numpy as np
import os
import matplotlib.pyplot as plt

file_path = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP\EX003977.SPR'

with open(file_path, 'rb') as f:
    raw_data = f.read()

# Skip the first 2048 bytes (header)
offset = 2048
img_data = raw_data[offset:]

# Convert to uint8 array
arr = np.frombuffer(img_data, dtype=np.uint8)

# Find stride by autocorrelation
# We test widths from 400 to 2000
def find_stride(data, min_w=400, max_w=2000):
    best_w = 0
    max_corr = 0
    # Use a slice to speed up
    slice_data = data[100000:200000].astype(np.float32)
    slice_data -= np.mean(slice_data)
    
    for w in range(min_w, max_w):
        # correlation between data[i] and data[i+w]
        corr = np.sum(slice_data[:-w] * slice_data[w:])
        if corr > max_corr:
            max_corr = corr
            best_w = w
    return best_w

stride = find_stride(arr)
print(f"Detected stride (width): {stride}")

if stride > 0:
    height = len(arr) // stride
    valid_len = height * stride
    
    img2d = arr[:valid_len].reshape((height, stride))
    
    # Save image
    out_img = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\images\CH-037_Elastografia_Optica_Indireta\spr_raw_decode.png"
    plt.figure(figsize=(10, 10))
    plt.imshow(img2d, cmap='gray')
    plt.title(f"Decoded SPR Image (Width: {stride})")
    os.makedirs(os.path.dirname(out_img), exist_ok=True)
    plt.savefig(out_img, dpi=300, bbox_inches='tight')
    print(f"Image saved to {out_img}")
