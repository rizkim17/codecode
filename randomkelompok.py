import random
import math

def buat_kelompok_acak(daftar_nama, ukuran_kelompok=3):
    """
    Membuat kelompok acak dari daftar nama dengan ukuran kelompok tertentu.
    
    Args:
        daftar_nama: Daftar nama anggota
        ukuran_kelompok: Jumlah anggota per kelompok (default: 3)
    
    Returns:
        List berisi kelompok-kelompok (setiap kelompok adalah list nama anggota)
    """
    # Buat salinan daftar agar tidak mengubah input asli
    nama_acak = daftar_nama.copy()
    
    # Acak daftar nama
    random.shuffle(nama_acak)
    
    # Hitung jumlah kelompok yang dibutuhkan
    jumlah_kelompok = math.ceil(len(nama_acak) / ukuran_kelompok)
    
    # Inisialisasi kelompok kosong
    kelompok = [[] for _ in range(jumlah_kelompok)]
    
    # Distribusikan nama ke kelompok
    for i, nama in enumerate(nama_acak):
        kelompok[i % jumlah_kelompok].append(nama)
    
    # Periksa kelompok dengan anggota kurang dari minimal (3)
    # dan pindahkan anggotanya ke kelompok lain
    kelompok_final = []
    anggota_tambahan = []
    
    for k in kelompok:
        if len(k) < 3:
            # Tambahkan anggota dari kelompok kecil ke daftar tambahan
            anggota_tambahan.extend(k)
        else:
            kelompok_final.append(k)
    
    # Distribusikan anggota tambahan ke kelompok lain
    for i, nama in enumerate(anggota_tambahan):
        # Tambahkan anggota ke kelompok dengan jumlah anggota paling sedikit
        kelompok_final.sort(key=len)
        kelompok_final[0].append(nama)
    
    return kelompok_final

def tampilkan_kelompok(daftar_kelompok):
    """
    Menampilkan daftar kelompok dengan format yang rapi.
    """
    for i, kelompok in enumerate(daftar_kelompok, 1):
        print(f"Kelompok {i} ({len(kelompok)} anggota):")
        for anggota in kelompok:
            print(f"  - {anggota}")
        print()

# Daftar nama siswa
nama_anggota = [
    "ABDUL AZIS BURHANUDIN",
    "ABDULLAH MUZAKI",
    "IRFAN SUTIAWAN",
    "M. FIKRY NH",
    "M. RIZKY MAULANA",
    "MUHAMAD NABIEL IPAR FATWA",
    "MUHAMAD RAFLI RAMLI",
    "MUHAMMAD SALMAN ALFARIZI",
    "NANDA IRSYAD MUZAMMIL",
    "NISRINA SALSABILA",
    "OSCAR HARIS NGARATU",
    "PUTRA RAMDITIANA",
    "RAFLY LUKMANUL HAKIM",
    "REZA AGUSTIAN KUSNADI",
    "RIZKI MAULANA",
    "SITI YENI MARLIAH",
    "WIDY PUTRI PRATIWI"
]

print(f"Total anggota: {len(nama_anggota)}")

# Buat kelompok dengan minimal 3 orang per kelompok
hasil_kelompok = buat_kelompok_acak(nama_anggota, ukuran_kelompok=4)

# Tampilkan hasil
tampilkan_kelompok(hasil_kelompok)