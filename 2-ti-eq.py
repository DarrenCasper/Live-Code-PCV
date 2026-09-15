import cv2
import numpy as np
import matplotlib.pyplot as plt


# Soal 1 melihat hasil dari Transformasi Negatif, Log, Gamma = 0,25, dan Gamma = 2,5
def get_lut_negative():
    r = np.arange(256, dtype=np.float64)
    return (255 - r).astype(np.uint8)

def get_lut_log():
    r = np.arange(256, dtype=np.float64)
    c = 255.0 / np.log(1.0 + 255.0)
    return np.clip(c * np.log(1.0 + r), 0, 255).astype(np.uint8)

def get_lut_gamma(gamma):
    r = np.arange(256, dtype=np.float64)
    return np.clip(255.0 * ((r / 255.0) ** gamma), 0, 255).astype(np.uint8)

def apply_lut(img, lut):
    return lut[img]


img = cv2.imread("img/darren.jpg", cv2.IMREAD_GRAYSCALE)
if img is None:
    img = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))


lut_neg = get_lut_negative()
lut_log = get_lut_log()
lut_gamma_04 = get_lut_gamma(0.4)
lut_gamma_25 = get_lut_gamma(2.5)


img_neg = apply_lut(img, lut_neg)
img_log = apply_lut(img, lut_log)
img_g04 = apply_lut(img, lut_gamma_04)
img_g25 = apply_lut(img, lut_gamma_25)


titles = ["Original", "Negatif", "Log Transform", "Gamma 0.4", "Gamma 2.5"]
images = [img, img_neg, img_log, img_g04, img_g25]

plt.figure(figsize=(15, 4))
for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(images[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titles[i])
    plt.axis("off")
plt.tight_layout()
plt.show()

def hitung_histogram(img):
    # mapping 256 array, baru dihitung per pixel value dari img ada berapa
    hist = np.zeros(256, dtype=np.int64)
    for pixel in img.ravel():
        hist[pixel] += 1
    return hist

hist_loop = hitung_histogram(img)
hist_bincount = np.bincount(img.ravel(), minlength=256)

# cek identical
is_identical = np.array_equal(hist_loop, hist_bincount)
print(f"Hasil hist loop dan np.bincount identik: {is_identical}")
print(f"Total piksel terhitung (Loop)    : {hist_loop.sum()}")
print(f"Total piksel terhitung (Bincount): {hist_bincount.sum()}")


# Hitung manual buat ekualisasi histogram
def ekualisasi_manual(img, L=256):
    MN = img.size
    hist = np.bincount(img.ravel(), minlength=L)
    p = hist / MN
    cdf = np.cumsum(p)
    s = np.floor((L - 1) * cdf + 0.5)
    lut = np.clip(s, 0, L-1).astype(np.uint8)
    return lut[img]

hasil_manual = ekualisasi_manual(img)
hasil_cv2 = cv2.equalizeHist(img)

# Hitung selisih
diff = np.abs(hasil_manual.astype(np.int32) - hasil_cv2.astype(np.int32))
max_diff = np.max(diff)

print(f"Selisih maksimum piksel: {max_diff}")
print(f"Jumlah piksel berbeda  : {np.count_nonzero(diff)} dari {img.size} piksel")

# Visualisasi perbandingan dan selisihnya
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(hasil_manual, cmap="gray")
plt.title("Ekualisasi Manual (NumPy)")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(hasil_cv2, cmap="gray")
plt.title("cv2.equalizeHist")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(diff, cmap="hot")
plt.title(f"Peta Selisih (Max: {max_diff})")
plt.axis("off")
plt.tight_layout()
plt.show()