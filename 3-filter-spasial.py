import cv2
import matplotlib.pyplot as plt
import numpy as np


# Part 1 dari konvolusi (berbagai jenis)

def konvolusi(f, w, tepi="replicate"):
    """Konvolusi f dengan kernel w, ditulis eksplisit agar mekanikanya terlihat.
    Untuk pemakaian nyata gunakan cv2.filter2D yang jauh lebih cepat."""
    m, n = w.shape
    a, b = m // 2, n // 2

    # Langkah 1: putar kernel 180 derajat -> inilah yang membedakan
    # konvolusi dari korelasi
    w_putar = np.flipud(np.fliplr(w))

    # Langkah 2: lebarkan citra supaya tepi punya tetangga
    mode_map = {"zero": "constant", "replicate": "edge", "reflect": "reflect"}
    if tepi not in mode_map:
        raise ValueError(f"Mode tepi tidak valid: {tepi}")

    mode = mode_map[tepi]
    f_pad = np.pad(f.astype(np.float64), ((a, a), (b, b)), mode=mode)

    # Langkah 3: geser jendela ke seluruh posisi
    g = np.zeros(f.shape, dtype=np.float64)
    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            jendela = f_pad[x:x + m, y:y + n]  # ambil ketetanggaan
            g[x, y] = np.sum(jendela * w_putar)  # jumlah hasil kali
    return g


def ke_uint8(g):
    """Bulatkan setengah ke atas lalu potong ke rentang yang sah."""
    return np.clip(np.floor(g + 0.5), 0, 255).astype(np.uint8)


f = np.array([
    [10, 10, 10, 10, 10],
    [10, 50, 50, 50, 10],
    [10, 50, 150, 50, 10],
    [20, 40, 40, 40, 20],
    [20, 20, 20, 20, 20],
], dtype=np.float64)

w = np.ones((3, 3), np.float64) / 9.0

print("Manual convolution:")
print(np.round(konvolusi(f, w, tepi="zero"), 2))

# Versi OpenCV. Perhatikan: filter2D menghitung KORELASI,
# jadi untuk kernel tak simetris kernelnya perlu dibalik lebih dulu.
# Disini bisa berubah value dari borderType jadi gak selalu sama, tergantung kebutuhan
hasil_cv = cv2.filter2D(f, -1, cv2.flip(w, -1), borderType=cv2.BORDER_CONSTANT)
print("\nOpenCV convolution:")
print(np.round(hasil_cv, 2))

# part 2 gaussian

im = cv2.imread("img/rektorat.jpg")

# box filter
kernel_box = np.ones((3,3), np.float32) / 9.0
hasil_box = cv2.filter2D(im, -1, kernel_box, borderType=cv2.BORDER_REPLICATE)
hasil_box2 = cv2.blur(im, (3,3))

# Gaussian
kernel_gauss = np.array([[1, 2, 1],
                        [2, 4, 2],
                        [1, 2, 1]], np.float32) / 16.0

hasil_gauss = cv2.filter2D(im, -1, kernel_gauss, borderType=cv2.BORDER_REPLICATE)
hasil_gauss2 = cv2.GaussianBlur(im, (5,5), sigmaX = 1.0)

kid = cv2.getGaussianKernel(ksize=5, sigma= 1.0)
print(np.round((kid @ kid.T), 4))

hasil_median = cv2.medianBlur(im,3)

for name, hasil in [("asli", im), ("box", hasil_box), ("gaussian", hasil_gauss), ("median", hasil_median)]:
    print("%-8s simpangan baku = %.2f" % (name, hasil.std()))

# Tampilkan hasil blur secara langsung
fig, axes = plt.subplots(1, 5, figsize=(18, 5))
axes[0].imshow(im, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(hasil_box, cmap="gray")
axes[1].set_title("Box Filter")
axes[2].imshow(hasil_box2, cmap="gray")
axes[2].set_title("Blur OpenCV")
axes[3].imshow(hasil_gauss, cmap="gray")
axes[3].set_title("Gaussian Filter")
axes[4].imshow(hasil_median, cmap="gray")
axes[4].set_title("Median Blur")
for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()


# ---------- Laplacian dan penajamannya ----------
im = cv2.imread("img/darren.jpg", cv2.IMREAD_GRAYSCALE)
imf = im.astype(np.float64)  # kerjakan dalam float, jangan uint8

kernel_lap = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
], np.float64)

lap = cv2.filter2D(imf, -1, kernel_lap, borderType=cv2.BORDER_REPLICATE)
# pusat kernel bernilai -4, maka citra dikurangi Laplacian-nya
tajam = imf - lap
tajam = np.clip(tajam, 0, 255).astype(np.uint8)  # WAJIB dipotong

# Laplacian bawaan OpenCV, hasilnya setara
lap_cv = cv2.Laplacian(im, cv2.CV_64F, ksize=1)

# ---------- Unsharp masking dan highboost ----------
def unsharp(im, k=1.0, ukuran=3):
    imf = im.astype(np.float64)
    halus = cv2.blur(imf, (ukuran, ukuran))  # versi halus
    mask = imf - halus  # bagian yang hilang
    hasil = imf + k * mask  # dikembalikan, dikuatkan k
    return np.clip(hasil, 0, 255).astype(np.uint8)


hasil_unsharp = unsharp(im, k=1.0)  # unsharp masking
hasil_highboost = unsharp(im, k=2.5)  # highboost, penajaman lebih kuat

# ---------- Sobel ----------
gx = cv2.Sobel(imf, cv2.CV_64F, 1, 0, ksize=3)  # turunan arah x
gy = cv2.Sobel(imf, cv2.CV_64F, 0, 1, ksize=3)  # turunan arah y
besar = np.abs(gx) + np.abs(gy)  # hampiran murah
besar_tepat = np.sqrt(gx**2 + gy**2)  # bentuk sebenarnya
arah = np.arctan2(gy, gx)  # arah gradien, radian
tepi = np.clip(besar, 0, 255).astype(np.uint8)

print("\nLaplacian sharpened image shape:", tajam.shape)
print("Unsharp result shape:", hasil_unsharp.shape)
print("Highboost result shape:", hasil_highboost.shape)
print("Sobel edge magnitude shape:", tepi.shape)
print("Sobel direction sample:", np.round(arah[0, 0], 4))

# Tampilkan hasil penajaman dan tepi secara langsung
fig2, axes2 = plt.subplots(1, 4, figsize=(18, 5))
axes2[0].imshow(tajam, cmap="gray")
axes2[0].set_title("Laplacian Sharpen")
axes2[1].imshow(hasil_unsharp, cmap="gray")
axes2[1].set_title("Unsharp Masking")
axes2[2].imshow(hasil_highboost, cmap="gray")
axes2[2].set_title("Highboost")
axes2[3].imshow(tepi, cmap="gray")
axes2[3].set_title("Sobel Edge")
for ax in axes2:
    ax.axis("off")
plt.tight_layout()
plt.show()