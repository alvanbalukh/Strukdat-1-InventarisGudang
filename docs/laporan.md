# Laporan Ringkas - Kelompok 1

**Proyek:** Sistem Inventaris Gudang Distributor Bahan Makanan & Farmasi
## Anggota Kelompok
1. (YOEL PEGGI MAYLSAN TANEO - 2506080027)
2. (DEVINE AVMITHYA SANVI NDAOMANU - 2506080053)
3. (VERREL ADHENOVAL LIGNUM MAKATITA - 2506080058)
4. (APRIANUS RISKI MANEK - 2506080084)
5. (Alvan Arnold Balukh - 25060800089)

## 1. Latar Belakang
Gudang makanan dan farmasi harus mengeluarkan barang yang paling cepat kedaluwarsa lebih dulu supaya
tidak terbuang. Masalah ini cocok dimodelkan dengan Queue (FIFO).

## 2. Struktur Data
```
Gudang  --punya banyak-->  Antrian (satu per produk)  --berisi-->  Node --> Node --> Node
                                                                    |        |       |
                                                                  Batch    Batch   Batch
```
Contoh antrean produk SUSU (depan = keluar duluan):
```
head --> [B-SUSU-1 exp 10 hari] --> [B-SUSU-3 exp 45 hari] --> [B-SUSU-2 exp 90 hari] --> None
```
- `enqueue` menyisipkan batch sesuai urutan expiry.
- `dequeue` mengambil batch paling depan.

## 3. Class
| Class | Tugas |
|---|---|
| Node | satu simpul linked list |
| Batch | data satu batch (nomor, produk, jumlah, harga, expiry) |
| Antrian | queue linked list: enqueue, dequeue, peek, cari, hapus |
| Gudang | manajer utama: restock dan keluarkan stok |
| Pembuangan | buang barang rusak dan kedaluwarsa |
| Laporan | near-expired dan total nilai aset |

## 4. Aturan Program
| Aturan | Cara kerja |
|---|---|
| Expiry terdekat keluar duluan | enqueue terurut + dequeue dari depan |
| Permintaan lebih dari satu batch | lanjut ke batch berikutnya |
| Stok tidak cukup | StokTidakCukupError, stok tidak berubah |
| Antrean kosong / penuh | QueueUnderflowError / QueueOverflowError |
| Restock barang kedaluwarsa | ditolak |
| Nomor batch kembar | ditolak |
| Near-expired | sisa hari 0 sampai 30 |
| Total nilai aset | jumlah x harga semua batch |

## 5. Pengujian
Unit test: `python -m unittest discover -s tests`. Yang diuji: antrean kosong dan penuh, urutan expiry,
expiry sama, hapus node depan/tengah/belakang, keluarkan stok lintas batch, stok kurang,
barang rusak, barang kedaluwarsa, near-expired, total nilai aset.

## 6. Skenario Demo
1. Muat data contoh, lalu menu 3 (lihat batch SUSU yang terurut padahal dimasukkan acak).
2. Menu 1: restock SUSU dengan expiry paling dekat, lalu menu 3 (batch itu ada di depan).
3. Menu 2: keluarkan 300 unit SUSU (diambil dari beberapa batch).
4. Menu 2 dengan jumlah terlalu besar (error stok), lalu input huruf (diminta ulang).
5. Menu 4: buang sebagian barang rusak.
6. Menu 6: laporan harian.
7. Menu 7: majukan tanggal beberapa bulan, menu 2 ditolak, menu 5 buang kedaluwarsa, menu 6 lagi.

## 7. Kesimpulan
Queue berbasis linked list dengan penyisipan terurut cukup untuk mengeluarkan barang berdasarkan
tanggal kedaluwarsa, dengan dequeue yang cepat O(1).
