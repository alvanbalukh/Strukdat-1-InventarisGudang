from datetime import date, datetime, timedelta

from batch import Batch
from gudang import Gudang
from pembuangan import Pembuangan
from laporan import Laporan, cetak_batch, format_rupiah
from error import QueueUnderflowError, QueueOverflowError, StokTidakCukupError


#fungsi untuk input
def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        print("Tidak boleh kosong!")


def input_angka(pesan):
    while True:
        try:
            angka = int(input(pesan))
            if angka > 0:
                return angka
            print("Angka harus lebih dari 0!")
        except ValueError:
            print("Masukkan angka bulat!")


def input_tanggal(pesan):
    while True:
        try:
            return datetime.strptime(input(pesan), "%Y-%m-%d").date()
        except ValueError:
            print("Format salah! Contoh: 2026-12-31")


def input_kategori():
    while True:
        kategori = input("Kategori (makanan/farmasi): ").strip().capitalize()
        if kategori == "Makanan" or kategori == "Farmasi":
            return kategori
        print("Pilih makanan atau farmasi!")


#menu 
def tampilkan_menu(hari_ini):
    print("\n==============================")
    print("INVENTARIS GUDANG | " + str(hari_ini))
    print("==============================")
    print("1. Restock")
    print("2. Keluarkan stok")
    print("3. Lihat stok")
    print("4. Buang barang rusak")
    print("5. Buang barang kedaluwarsa")
    print("6. Laporan harian")
    print("7. Ubah tanggal (untuk simulasi)")
    print("0. Keluar")


def isi_data_contoh(gudang, hari_ini):
    # (no_batch, kode, nama, kategori, jumlah, harga, expiry = hari ini + sekian hari)
    data = [
        ("B-SUSU-1", "SUSU", "Susu UHT 1L", "Makanan", 120, 18000, 10),
        ("B-SUSU-2", "SUSU", "Susu UHT 1L", "Makanan", 200, 18000, 90),
        ("B-SUSU-3", "SUSU", "Susu UHT 1L", "Makanan", 150, 18500, 45),
        ("B-MIE-1", "MIE", "Mie Instan", "Makanan", 500, 3000, 20),
        ("B-MIE-2", "MIE", "Mie Instan", "Makanan", 800, 3000, 180),
        ("B-PARA-1", "PARA", "Paracetamol 500mg", "Farmasi", 300, 5000, 25),
        ("B-PARA-2", "PARA", "Paracetamol 500mg", "Farmasi", 400, 5200, 365),
        ("B-AMOX-1", "AMOX", "Amoxicillin 500mg", "Farmasi", 100, 12000, 7),
    ]
    for d in data:
        expiry = hari_ini + timedelta(days=d[6])
        gudang.restock(Batch(d[0], d[1], d[2], d[3], d[4], d[5], expiry), hari_ini)
    print(len(data), "batch contoh berhasil dimuat")


def menu_restock(gudang, hari_ini):
    print("\n--- RESTOCK ---")
    no_batch = input_teks("Nomor batch: ").upper()
    kode = input_teks("Kode produk: ").upper()
    nama = input_teks("Nama produk: ")
    kategori = input_kategori()
    jumlah = input_angka("Jumlah: ")
    harga = input_angka("Harga satuan: ")
    expiry = input_tanggal("Tanggal kedaluwarsa (YYYY-MM-DD): ")

    batch = Batch(no_batch, kode, nama, kategori, jumlah, harga, expiry)
    gudang.restock(batch, hari_ini)
    print("Batch", no_batch, "berhasil ditambahkan")


def menu_keluarkan(gudang, hari_ini):
    print("\n--- KELUARKAN STOK ---")
    for kode in gudang.daftar_kode():
        print(" ", kode, "- stok", gudang.total_stok(kode))
    kode = input_teks("Kode produk: ").upper()
    jumlah = input_angka("Jumlah diminta: ")

    hasil = gudang.keluarkan_stok(kode, jumlah, hari_ini)
    print("Berhasil mengeluarkan", jumlah, "unit. Diambil dari:")
    for no_batch, diambil in hasil:
        print("  - batch", no_batch, ":", diambil, "unit")


def menu_lihat(gudang, hari_ini):
    print("\n--- STOK GUDANG (paling atas = keluar duluan) ---")
    if len(gudang.daftar_kode()) == 0:
        print("Gudang masih kosong")
        return
    for kode in gudang.daftar_kode():
        antrian = gudang.get_antrian(kode)
        print("\nProduk", kode, "| batch", antrian.jumlah(), "/", antrian.kapasitas(),
              "| total stok", gudang.total_stok(kode))
        if antrian.kosong():
            print("  (kosong)")
        else:
            cetak_batch(antrian.ke_list(), hari_ini)


def menu_buang_rusak(pembuangan):
    print("\n--- BUANG BARANG RUSAK ---")
    no_batch = input_teks("Nomor batch: ").upper()
    jumlah = input_angka("Jumlah yang rusak: ")
    kerugian = pembuangan.buang_rusak(no_batch, jumlah)
    print("Barang rusak dibuang. Kerugian:", format_rupiah(kerugian))


def menu_buang_kedaluwarsa(pembuangan, hari_ini):
    print("\n--- BUANG BARANG KEDALUWARSA ---")
    dibuang = pembuangan.buang_kedaluwarsa(hari_ini)
    if len(dibuang) == 0:
        print("Tidak ada barang kedaluwarsa")
        return
    total = 0
    for b in dibuang:
        print("  -", b.no_batch, "(", b.jumlah, "unit )")
        total += b.nilai()
    print(len(dibuang), "batch dibuang. Kerugian:", format_rupiah(total))


def menu_laporan(laporan, pembuangan, hari_ini):
    laporan.cetak_laporan(hari_ini)
    print("\nTotal kerugian barang dibuang:", format_rupiah(pembuangan.total_kerugian))


#program utama 
def main():
    gudang = Gudang()
    pembuangan = Pembuangan(gudang)
    laporan = Laporan(gudang)
    hari_ini = date.today()

    print("=== SISTEM INVENTARIS GUDANG (FIFO & EXPIRY DATE) ===")
    try:
        if input("Muat data contoh? (y/n): ").lower() == "y":
            isi_data_contoh(gudang, hari_ini)

        while True:
            tampilkan_menu(hari_ini)
            pilihan = input("Pilih menu: ").strip()
            try:
                if pilihan == "1":
                    menu_restock(gudang, hari_ini)
                elif pilihan == "2":
                    menu_keluarkan(gudang, hari_ini)
                elif pilihan == "3":
                    menu_lihat(gudang, hari_ini)
                elif pilihan == "4":
                    menu_buang_rusak(pembuangan)
                elif pilihan == "5":
                    menu_buang_kedaluwarsa(pembuangan, hari_ini)
                elif pilihan == "6":
                    menu_laporan(laporan, pembuangan, hari_ini)
                elif pilihan == "7":
                    hari_ini = input_tanggal("Tanggal baru (YYYY-MM-DD): ")
                elif pilihan == "0":
                    print("Terima kasih!")
                    break
                else:
                    print("Menu tidak ada, pilih 0-7")
            except (QueueUnderflowError, QueueOverflowError, StokTidakCukupError, ValueError) as e:
                print("ERROR:", e)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan")


if __name__ == "__main__":
    main()
