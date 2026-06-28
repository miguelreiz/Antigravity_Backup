import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np

file_path = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP\EX003977.SPR'

def entropy(data):
    if len(data) == 0:
        return 0
    p = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256) / len(data)
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

print(f"File size: {os.path.getsize(file_path)} bytes")

with open(file_path, 'rb') as f:
    data = f.read()

# Let's inspect the first 2048 bytes for ASCII strings
print("--- Header Strings ---")
header = data[:2048]
strings = []
current_str = ""
for b in header:
    if 32 <= b <= 126:
        current_str += chr(b)
    else:
        if len(current_str) > 3:
            strings.append(current_str)
        current_str = ""
for s in strings:
    print(s)

# Calculate entropy of 100KB chunks to find where raw image data might start
# Compressed data has entropy > 7.9. Uncompressed medical images have entropy ~ 4 to 6.
print("\n--- Entropy Analysis ---")
chunk_size = 100000
for i in range(0, min(len(data), 1000000), chunk_size):
    chunk = data[i:i+chunk_size]
    ent = entropy(chunk)
    print(f"Offset {i:08x}: Entropy = {ent:.2f}")

# Try to find common image headers
print("\n--- Magic Bytes Check ---")
if b'BM' in data[:1024]:
    print("Found BMP header")
if b'\xff\xd8\xff' in data[:1024]:
    print("Found JPEG header")
if b'II*\x00' in data[:1024] or b'MM\x00*' in data[:1024]:
    print("Found TIFF header")
    
# Let's assume the image starts somewhere. We can try to reshape a block of it.
# Let's write a small brute-force loop that looks for a valid width that produces a "cornea-like" image
# Actually, first let's see the entropy.
