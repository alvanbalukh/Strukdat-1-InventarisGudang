import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from batch import Batch
from gudang import Gudang
from pembuangan import Pembuangan
from laporan import Laporan
from error import StokTidakCukupError

HARI_INI = date(2026, 1, 1)


def buat(no, expiry, jumlah=10, harga=1000, kode="P1"):
    return Batch(no, kode, "Produk", "Farmasi", jumlah, harga, expiry)


class TestPembuanganLaporan(unittest.TestCase):
    def setUp(self):
        self.gudang = Gudang()
        self.pembuangan = Pembuangan(self.gudang)
        self.laporan = Laporan(self.gudang)

    def test_buang_rusak_sebagian(self):
        self.gudang.restock(buat("A", date(2026, 6, 1), 50), HARI_INI)
        self.pembuangan.buang_rusak("A", 20)
        self.assertEqual(self.gudang.total_stok("P1"), 30)

    def test_buang_rusak_semua(self):
        self.gudang.restock(buat("A", date(2026, 6, 1), 50, 2000), HARI_INI)
        kerugian = self.pembuangan.buang_rusak("A", 50)
        self.assertEqual(kerugian, 100000)
        self.assertIsNone(self.gudang.cari_batch("A"))

    def test_buang_rusak_melebihi_stok(self):
        self.gudang.restock(buat("A", date(2026, 6, 1), 50), HARI_INI)
        with self.assertRaises(StokTidakCukupError):
            self.pembuangan.buang_rusak("A", 51)

    def test_buang_rusak_batch_tidak_ada(self):
        with self.assertRaises(ValueError):
            self.pembuangan.buang_rusak("TIDAK-ADA", 1)

    def test_buang_kedaluwarsa(self):
        self.gudang.restock(buat("A", date(2026, 1, 5)), HARI_INI)
        self.gudang.restock(buat("B", date(2026, 1, 8)), HARI_INI)
        self.gudang.restock(buat("C", date(2026, 6, 1)), HARI_INI)
        dibuang = self.pembuangan.buang_kedaluwarsa(date(2026, 1, 10))
        self.assertEqual(len(dibuang), 2)
        self.assertEqual(len(self.gudang.semua_batch()), 1)

    def test_buang_kedaluwarsa_gudang_kosong(self):
        self.assertEqual(self.pembuangan.buang_kedaluwarsa(HARI_INI), [])

    def test_total_nilai_aset(self):
        self.gudang.restock(buat("A", date(2026, 6, 1), 10, 1000), HARI_INI)
        self.gudang.restock(buat("B", date(2026, 7, 1), 5, 2000, "P2"), HARI_INI)
        self.assertEqual(self.laporan.total_nilai_aset(), 20000)

    def test_total_nilai_aset_kosong(self):
        self.assertEqual(self.laporan.total_nilai_aset(), 0)

    def test_near_expired(self):
        self.gudang.restock(buat("DEKAT", date(2026, 1, 11)), HARI_INI)   # 10 hari
        self.gudang.restock(buat("PAS", date(2026, 1, 31)), HARI_INI)     # 30 hari
        self.gudang.restock(buat("JAUH", date(2026, 2, 1)), HARI_INI)     # 31 hari
        hasil = self.laporan.near_expired(HARI_INI)
        self.assertEqual([b.no_batch for b in hasil], ["DEKAT", "PAS"])


if __name__ == "__main__":
    unittest.main()
