import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from batch import Batch
from gudang import Gudang
from error import StokTidakCukupError, QueueOverflowError

HARI_INI = date(2026, 1, 1)


def buat(no, expiry, jumlah=100):
    return Batch(no, "P1", "Produk", "Makanan", jumlah, 1000, expiry)


class TestGudang(unittest.TestCase):
    def setUp(self):
        self.gudang = Gudang(kapasitas=3)

    def test_restock_dan_total_stok(self):
        self.gudang.restock(buat("A", date(2026, 2, 1), 50), HARI_INI)
        self.gudang.restock(buat("B", date(2026, 3, 1), 70), HARI_INI)
        self.assertEqual(self.gudang.total_stok("P1"), 120)

    def test_restock_nomor_batch_sama(self):
        self.gudang.restock(buat("A", date(2026, 2, 1)), HARI_INI)
        with self.assertRaises(ValueError):
            self.gudang.restock(buat("A", date(2026, 3, 1)), HARI_INI)

    def test_restock_barang_kedaluwarsa(self):
        with self.assertRaises(ValueError):
            self.gudang.restock(buat("A", date(2025, 12, 31)), HARI_INI)

    def test_restock_overflow(self):
        for i in range(3):
            self.gudang.restock(buat("B" + str(i), date(2026, 2, 1 + i)), HARI_INI)
        with self.assertRaises(QueueOverflowError):
            self.gudang.restock(buat("X", date(2026, 5, 1)), HARI_INI)

    def test_keluarkan_dari_expiry_terdekat(self):
        self.gudang.restock(buat("JAUH", date(2026, 6, 1)), HARI_INI)
        self.gudang.restock(buat("DEKAT", date(2026, 2, 1)), HARI_INI)
        hasil = self.gudang.keluarkan_stok("P1", 30, HARI_INI)
        self.assertEqual(hasil, [("DEKAT", 30)])

    def test_keluarkan_lintas_batch(self):
        self.gudang.restock(buat("A", date(2026, 2, 1), 40), HARI_INI)
        self.gudang.restock(buat("B", date(2026, 3, 1), 40), HARI_INI)
        self.gudang.restock(buat("C", date(2026, 4, 1), 40), HARI_INI)
        hasil = self.gudang.keluarkan_stok("P1", 100, HARI_INI)
        self.assertEqual(hasil, [("A", 40), ("B", 40), ("C", 20)])
        self.assertEqual(self.gudang.total_stok("P1"), 20)

    def test_stok_tidak_cukup(self):
        self.gudang.restock(buat("A", date(2026, 2, 1), 40), HARI_INI)
        with self.assertRaises(StokTidakCukupError):
            self.gudang.keluarkan_stok("P1", 41, HARI_INI)
        self.assertEqual(self.gudang.total_stok("P1"), 40)   # stok tidak berubah

    def test_produk_tidak_ada(self):
        with self.assertRaises(ValueError):
            self.gudang.keluarkan_stok("XXX", 1, HARI_INI)

    def test_keluarkan_diblokir_kalau_ada_kedaluwarsa(self):
        self.gudang.restock(buat("A", date(2026, 1, 5)), HARI_INI)
        with self.assertRaises(ValueError):
            self.gudang.keluarkan_stok("P1", 1, date(2026, 2, 1))


if __name__ == "__main__":
    unittest.main()
