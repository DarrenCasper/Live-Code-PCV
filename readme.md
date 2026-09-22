# Laporan Pengolahan Citra dan Video
## Pertemuan 2: Transformasi Intensitas & Peningkatan Citra

---

### Data Praktikan
* **Nama**        : Darren Dexter Thio
* **NRP**         : 5024241006
* **Kelas**       : Pengolahan Citra dan Video A
* **Departemen**  : Teknik Komputer - FTEIC ITS
* **Dosen Pengampu**: Ir. Arta Kusuma Hernanda, S.T., M.T.

---

## 1. Transformasi Intensitas Berbasis LUT

> **Referensi Kode:** `2-ti-eq.py`

### 1.1 Hasil Visualisasi
![Hasil 4 Transformasi](output/4-transform.png)

### 1.2 Analisis Hasil Transformasi
* **Citra Negatif ($s = 255 - r$):**
  Citra negatif mengubah nilai kebalikan dari value original, sehingga kalau gelap berubah menjadi terang, dan citra terang dibalik menjadi gelap.
* **Transformasi Log ($s = c \cdot \ln(1 + r)$):**
  Tujuan dari transformasi logaritme adalah mengubah warna yang gelap dinaikkan menjadi lebih terang (jadi menaikkan warna, serta menetralkan warna putih)
* **Koreksi Gamma $\gamma = 0.4$ ($\gamma < 1$):**
  Tujuan dari transformasi gamma kalau lebih kecil dari 1, adalah mengubah warna menjadi lebih terang
* **Koreksi Gamma $\gamma = 2.5$ ($\gamma > 1$):**
  sedangkan dari gamma lebih besar dari 2.5, mengubah warna menjadi lebih gelap.

---

## 2. Cacah Histogram Manual vs `np.bincount`

> **Referensi Kode:** `src/tugas2_histogram.py`

### 2.1 Bukti Verifikasi Numerik
Hasil pengujian kesamaan array antara perulangan manual dan fungsi bawaan:

```text
Eksekusi pengujian histogram:
- np.array_equal(hist_loop, hist_bincount) : True
- Total selisih absolut antar-bin         : 0
- Total piksel terhitung (Loop manual)    : [Contoh: 262144]
- Total piksel terhitung (np.bincount)    : [Contoh: 262144]
- Dimensi citra (M x N)                   : [Contoh: 512 x 512 = 262144]
```

## 3. Ekualisasi Histogram Manual

> **Referensi Kode:** `2-ti-eq.py`

### 3.1 Tahapan Perhitungan
1. Hitung histogram $h(r_k) = n_k$ dari citra masukan.
2. Normalisasi menjadi peluang $p(r_k) = n_k / MN$.
3. Hitung CDF kumulatif: $\text{cdf}(k) = \sum_{j=0}^{k} p(r_j)$.
4. Petakan ke intensitas baru: $s_k = \text{round}\big((L-1)\cdot \text{cdf}(k)\big)$.
5. Terapkan hasil pemetaan sebagai LUT ke seluruh piksel citra.

### 3.2 Hasil Visualisasi
![Hasil Ekualisasi Histogram](output/equalize.png)

[Sertakan minimal: citra asli, citra hasil ekualisasi manual, dan histogram sebelum/sesudah berdampingan]

### 3.3 Perbandingan dengan `cv2.equalizeHist`

```text
Eksekusi pengujian ekualisasi:
- Selisih maksimum piksel (manual vs cv2.equalizeHist) : [Contoh: 1]
- Selisih rata-rata piksel                              : [Contoh: 0.03]
- Jumlah piksel berbeda dari total                      : [Contoh: 512 dari 262144]
```

**Analisis Perbedaan:**
perbedaan yang bisa dihasilkan oleh kedua fungsi ini, antara built in dari opencv, atau hitung manual adalah disebabkan oleh value + 0,5 dari hitungan manual yang tujuan untuk melakukan flooring value.
---

## 4. Tabel Manual Ekualisasi (Citra 3-bit)

> **Data:** $n_k$ sesuai yang dibagikan oleh dosen pengampu (L = 8 level, 3 bit)

### 4.1 Tabel Perhitungan

| $r_k$ | $n_k$ | $p(r_k)$ | cdf | $(L-1)\cdot\text{cdf}$ | $s_k$ |
| --- | --- | --- | --- | --- | --- |
| 0 | [ 0 ] | [ 0 ] | [ 0 ] | [ 0 ] | [ 0 ] |
| 1 | [ 1 ] | [ 0.04 ] | [ 0.04 ] | [ 0.28 ] | [ 0 ] |
| 2 | [ 3 ] | [ 0.12 ] | [ 0.16 ] | [ 1.12 ] | [ 1 ] |
| 3 | [ 6 ] | [ 0.24 ] | [ 0.40 ] | [ 2.80 ] | [ 3 ] |
| 4 | [ 7 ] | [ 0.28 ] | [ 0.68 ] | [ 4.76 ] | [ 5 ] |
| 5 | [ 5 ] | [ 0.20 ] | [ 0.88 ] | [ 6.16 ] | [ 6 ] |
| 6 | [ 3 ] | [ 0.12] | [ 1.00 ] | [ 7 ] | [ 7 ] |
| 7 | [ 0 ] | [ 0 ] | [ 1.00 ] | [ 7 ] | [ 7 ] |

### 4.2 Foto Perhitungan Tulis Tangan
![Perhitungan Manual Tulis Tangan](output/result.png)

---

## 5. Filter Spasial (Blur, Sharpening, Edge Detection)

> **Referensi Kode:** `3-filter-spasial.py`

### 5.1 Konvolusi pada Citra
![Hasil Konvolusi](img/konvolusi.png)

**Penjelasan:**
* Konvolusi adalah proses mengalikan setiap piksel citra dengan kernel/filter dan menjumlahkan hasilnya untuk menghasilkan piksel baru.
* Pada bagian ini, kernel rata-rata (average filter) diterapkan pada matriks contoh untuk melihat bagaimana nilai piksel dipengaruhi oleh tetangganya.
* Proses ini menjadi dasar dari operasi blur, sharpening, serta deteksi tepi pada citra digital.

**Placeholder Output Terminal:**
```text
Manual convolution:
[[ 8.89 15.56 20.   15.56  8.89]
 [15.56 38.89 47.78 38.89 15.56]
 [20.   46.67 57.78 46.67 20.  ]
 [17.78 41.11 47.78 41.11 17.78]
 [11.11 17.78 20.   17.78 11.11]]

OpenCV convolution:
[[ 8.89 15.56 20.   15.56  8.89]
 [15.56 38.89 47.78 38.89 15.56]
 [20.   46.67 57.78 46.67 20.  ]
 [17.78 41.11 47.78 41.11 17.78]
 [11.11 17.78 20.   17.78 11.11]]
```

### 5.2 Hasil Visualisasi Blur
![Hasil Blur Placeholder](output/blur.png)

**Penjelasan:**
* Filter box menghasilkan efek blur yang lebih halus dan merata.
* Gaussian blur menghasilkan efek blur yang lebih natural dan lembut.
* Median blur efektif untuk mengurangi noise salt-and-pepper tanpa menghilangkan tepi terlalu banyak.

### 5.3 Hasil Visualisasi Penajaman dan Tepi
![Hasil Sharpening & Tepi Placeholder](output/sharpen.png)

**Penjelasan:**
* Laplacian sharpening menonjolkan detail dan tepi pada citra.
* Unsharp masking meningkatkan ketajaman dengan cara menambahkan mask perbedaan antara citra asli dan versi yang diblur.
* Highboost memberikan penajaman lebih kuat dibanding unsharp masking biasa.
* Operasi Sobel mendeteksi perubahan intensitas pada arah horizontal dan vertikal.
* Magnitude gradien menunjukkan area dengan perubahan intensitas besar, yang biasanya menandakan tepi.
* Arah gradien membantu mengetahui orientasi tepi pada citra.

### 5.4 Analisis Umum
* Filter blur digunakan untuk meredam detail kecil dan noise.
* Filter sharpening digunakan untuk meningkatkan ketajaman citra.
* Filter tepi digunakan untuk menonjolkan struktur objek dalam citra.
* Kombinasi teknik ini sering dipakai untuk preprocessing sebelum analisis lanjutan seperti segmentasi dan pengenalan objek.

---

