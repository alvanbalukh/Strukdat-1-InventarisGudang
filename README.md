git init# Strukdat-1-InventarisGudang

Sistem inventaris gudang distributor bahan makanan & farmasi.
Tugas Proyek Struktur Data - Kelompok 1 (Supply Chain & FMCG) - Fokus: FIFO & Expiry Date.

Program CLI Python (OOP). Barang disimpan per **batch** yang punya tanggal kedaluwarsa, dan saat ada
permintaan stok, batch dengan **expiry paling dekat dikeluarkan lebih dulu**. Queue dibuat sendiri
dengan **linked list** (tidak memakai `queue.Queue` dan tidak memakai `list.pop(0)`).

## Fitur
1. Restock (terima batch baru)
2. Keluarkan stok (ambil dari batch expiry terdekat, lanjut ke batch berikutnya kalau kurang)
3. Lihat stok
4. Buang barang rusak
5. Buang barang kedaluwarsa
6. Laporan harian (barang near-expired dan total nilai aset)
7. Ubah tanggal (untuk simulasi barang kedaluwarsa)

## Cara Menjalankan
Butuh Python 3.8 atau lebih baru.
```
python src/main.py
```
Menjalankan tes:
```
python -m unittest discover -s tests
```

## Struktur Folder
```
src/
  main.py         menu CLI
  gudang.py       class Gudang (manajer utama): restock & keluarkan stok
  antrian.py      class Antrian: queue linked list
  node.py         class Node
  batch.py        class Batch
  pembuangan.py   class Pembuangan: barang rusak & kedaluwarsa
  laporan.py      class Laporan: near-expired & total nilai aset
  error.py        error buatan sendiri
tests/            unit test
docs/             laporan & pembagian tugas
```

## Struktur Data
- **Node** punya `data` (objek Batch) dan `next` (node berikutnya).
- **Antrian** adalah linked list dengan `_head`. Tiap produk punya satu Antrian, disimpan di dictionary
  pada class `Gudang` (kode produk -> Antrian).
- **Kenapa enqueue disisipkan terurut?** Kalau FIFO biasa (urut kedatangan), batch baru yang expiry-nya
  lebih dekat akan keluar belakangan. Jadi batch disisipkan sesuai urutan expiry, sedangkan `dequeue` tetap
  mengambil dari depan. Kalau expiry sama, yang masuk duluan keluar duluan.

| Operasi | Kompleksitas |
|---|---|
| enqueue | O(n), harus mencari posisi |
| dequeue, peek | O(1), selalu dari depan |
| hapus, cari | O(n) |
| kosong, penuh, jumlah | O(1) |

**Error:** `QueueUnderflowError` (ambil dari antrean kosong), `QueueOverflowError` (antrean penuh, maksimal
10 batch per produk), `StokTidakCukupError`, dan `ValueError` untuk data yang salah (batch kembar, produk tidak ada, dll).
Input yang salah (huruf, angka negatif, format tanggal) diminta ulang, program tidak berhenti.

## Anggota Kelompok
1. (YOEL PEGGI MAYLSAN TANEO - 2506080027)
2. (DEVINE AVMITHYA SANVI NDAOMANU - 2506080053)
3. (VERREL ADHENOVAL LIGNUM MAKATITA - 2506080058)
4. (APRIANUS RISKI MANEK - 2506080084)
5. (Alvan Arnold Balukh - 25060800089)
 
 