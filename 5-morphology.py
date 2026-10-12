import cv2
import numpy as np

A = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],  
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
        ],  # Cacat: jembatan di (4, 6)
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    dtype=np.uint8,
)


B = np.ones((3, 3), dtype=np.uint8)


def print_matrix(judul, matriks):
    """Mencetak matriks biner ke terminal secara rapi."""
    print(f"=== {judul} (Piksel 1 = {np.sum(matriks)}) ===")
    for row in matriks:
        print(" ".join(str(val) for val in row))
    print()



# Dilasi & Erosi (dengan borderValue=0 konvensi buku)
dilasi = cv2.dilate(A, B, borderType=cv2.BORDER_CONSTANT, borderValue=0)
erosi = cv2.erode(A, B, borderType=cv2.BORDER_CONSTANT, borderValue=0)

# Opening: Erosi lalu Dilasi (A o B)
opening = cv2.dilate(erosi, B, borderType=cv2.BORDER_CONSTANT, borderValue=0)

# Closing: Dilasi lalu Erosi (A • B)
closing = cv2.erode(dilasi, B, borderType=cv2.BORDER_CONSTANT, borderValue=0)


batas_dalam = cv2.subtract(A, erosi)  # A - (A ⊖ B)
batas_luar = cv2.subtract(dilasi, A)  # (A ⊕ B) - A
gradien = cv2.subtract(dilasi, erosi)  # (A ⊕ B) - (A ⊖ B)


top_hat = cv2.subtract(A, opening)  # A - (A o B)
black_hat = cv2.subtract(closing, A)  # (A • B) - A


pola_terisolasi = np.array(
    [[-1, -1, -1], [-1, 1, -1], [-1, -1, -1]], dtype=np.int8
)
hit_or_miss = cv2.morphologyEx(A, cv2.MORPH_HITMISS, pola_terisolasi)
hit_or_miss = (hit_or_miss > 0).astype(np.uint8)


se_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
A_komplemen = 1 - A
X = np.zeros_like(A)
X[2, 3] = 1  

while True:
    X_sebelumnya = X.copy()
    X = (
        cv2.dilate(X, se_cross, borderType=cv2.BORDER_CONSTANT, borderValue=0)
        & A_komplemen
    )
    if np.array_equal(X, X_sebelumnya):
        break

lubang_terisi = cv2.bitwise_or(X, A)


print_matrix("Matriks Acuan A", A)
print_matrix("Dilasi (A ⊕ B)", dilasi)
print_matrix("Erosi (A ⊖ B)", erosi)
print_matrix("Opening (A ∘ B)", opening)
print_matrix("Closing (A • B)", closing)
print_matrix("Batas Dalam (A - (A ⊖ B))", batas_dalam)
print_matrix("Batas Luar ((A ⊕ B) - A)", batas_luar)
print_matrix("Gradien Morfologi ((A ⊕ B) - (A ⊖ B))", gradien)
print_matrix("Top-Hat (A - (A ∘ B))", top_hat)
print_matrix("Black-Hat ((A • B) - A)", black_hat)
print_matrix("Hit-or-Miss (Piksel Terisolasi)", hit_or_miss)
print_matrix("Pengisian Lubang (Hole Filling)", lubang_terisi)