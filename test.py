from PIL import Image
import os

# Fungsi untuk mencari file gambar dengan ukuran pixel paling besar
def cari_gambar_terbesar(direktori):
    gambar_terbesar = None
    ukuran_terbesar = (0, 0)

    for root, dirs, files in os.walk(direktori):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                ukuran = image.size

                if ukuran[0] * ukuran[1] > ukuran_terbesar[0] * ukuran_terbesar[1]:
                    ukuran_terbesar = ukuran
                    gambar_terbesar = file_path

    return gambar_terbesar, ukuran_terbesar

# Ganti 'direktori' dengan direktori yang ingin Anda telusuri
direktori = "C:/Users/Ghandi/Downloads/Construction Site Safety.v27-yolov8.yolov8/test/images"
gambar_terbesar, ukuran_terbesar = cari_gambar_terbesar(direktori)

if gambar_terbesar is not None:
    print(f"File gambar terbesar: {gambar_terbesar}")
    print(f"Ukuran gambar terbesar: {ukuran_terbesar[0]} x {ukuran_terbesar[1]} piksel")
else:
    print("Tidak ada file gambar ditemukan di direktori yang Anda tentukan.")