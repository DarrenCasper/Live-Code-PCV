# Function for changing RGB to CMYK
import cv2
import numpy as np
import matplotlib.pyplot as plt


def rgb_to_cmyk(r,g, b):
    r,g,b = r/255, g/255, b/255
    k = 1 - max(r,g,b)
    
    if k == 1:
        return (0,0,0, 100)
    
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    
    return tuple(round(value * 100, 2) for value in (c,m,y,k))

print(rgb_to_cmyk(100,192,204))



def rgb_to_hsi(rgb):
    f = rgb.astype(np.float64)/ 255.0
    R, G, B = f[:, :, 0], f[:, :, 1], f[:, :, 2]
    
    pembilang = 0.5 * ((R - G) + (R - B))
    penyebut = np.sqrt((R - G)**2 + (R - B) * (G - B))
    rasio = np.divide(pembilang, penyebut, out=np.zeros_like(pembilang), where=penyebut > 1e-12)
    theta = np.degrees(np.arccos(np.clip(rasio, -1.0, 1.0)))
    H = np.where(B <= G, theta, 360.0 - theta)
    jumlah = R + G + B
    
    S = 1 - 3 * np.minimum(np.minimum(R, G), B) / np.where(jumlah == 0, 1, jumlah)
    I = jumlah/3.0
    return H, S, I


def rgb_to_cmyk_image(rgb):
    f = rgb.astype(np.float64) / 255.0
    R, G, B = f[:, :, 0], f[:, :, 1], f[:, :, 2]

    K = 1 - np.maximum(np.maximum(R, G), B)
    penyebut = np.where(K == 1, 1, 1 - K)

    C = np.where(K == 1, 0, (1 - R - K) / penyebut)
    M = np.where(K == 1, 0, (1 - G - K) / penyebut)
    Y = np.where(K == 1, 0, (1 - B - K) / penyebut)

    return C, M, Y, K


def hsi_to_rgb(hsi):
    # Asumsi: H = 0–360 derajat, S dan I = 0–1
    H = hsi[:, :, 0].astype(float) % 360
    S = hsi[:, :, 1].astype(float)
    I = hsi[:, :, 2].astype(float)

    sektor = (H // 120).astype(int)
    H_lokal = H % 120  # H setelah dikurangi 0, 120, atau 240 derajat

    rendah = I * (1 - S)
    dominan = I * (
        1 + S * np.cos(np.deg2rad(H_lokal))
        / np.cos(np.deg2rad(60 - H_lokal))
    )
    sisa = 3 * I - (rendah + dominan)

    # Sektor RG: R=dominan, G=sisa, B=rendah
    # Sektor GB: R=rendah, G=dominan, B=sisa
    # Sektor BR: R=sisa, G=rendah, B=dominan
    r = np.select([sektor == 0, sektor == 1, sektor == 2],
                  [dominan, rendah, sisa])
    g = np.select([sektor == 0, sektor == 1, sektor == 2],
                  [sisa, dominan, rendah])
    b = np.select([sektor == 0, sektor == 1, sektor == 2],
                  [rendah, sisa, dominan])

    rgb = np.stack((r, g, b), axis=-1)
    return np.round(np.clip(rgb, 0, 1) * 255).astype(np.uint8)


image_bgr = cv2.imread("img/darren.jpg")
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# CMYK on the center pixel of the image
h, w, _ = image_rgb.shape
r, g, b = image_rgb[h // 2, w // 2]
print("CMYK (center pixel):", rgb_to_cmyk(int(r), int(g), int(b)))

# HSI on the whole image
H, S, I = rgb_to_hsi(image_rgb)

# HSI -> RGB (reconstruction), then RGB -> HSV to build a red mask
hsi = np.stack((H, S, I), axis=-1)
rgb = hsi_to_rgb(hsi)

hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
h_ch, s_ch, v_ch = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
print("H maksimum pada gambar:", h_ch.max())

bawah = np.array([0, 50, 50], dtype=np.uint8)
atas = np.array([15, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, bawah, atas)

# CMYK on the whole image (for visualization)
C, M, Y, K = rgb_to_cmyk_image(image_rgb)

# --- Comparison figure: RGB vs HSI vs CMYK vs HSV ---
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

axes[0, 0].imshow(image_rgb)
axes[0, 0].set_title("RGB (Original)")

axes[0, 1].imshow(H, cmap="hsv")
axes[0, 1].set_title("HSI - Hue")
axes[0, 2].imshow(S, cmap="gray")
axes[0, 2].set_title("HSI - Saturation")
axes[0, 3].imshow(I, cmap="gray")
axes[0, 3].set_title("HSI - Intensity")

axes[1, 0].imshow(K, cmap="gray")
axes[1, 0].set_title("CMYK - Key (K)")
axes[1, 1].imshow(hsv[:, :, 0], cmap="hsv")
axes[1, 1].set_title("HSV - Hue")
axes[1, 2].imshow(hsv[:, :, 1], cmap="gray")
axes[1, 2].set_title("HSV - Saturation")
axes[1, 3].imshow(mask, cmap="gray")
axes[1, 3].set_title("HSV - Red Mask")

for row in axes:
    for ax in row:
        ax.axis("off")

plt.tight_layout()
plt.show()