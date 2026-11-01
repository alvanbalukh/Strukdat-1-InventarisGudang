import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from antrian import Antrian
from batch import Batch
from error import QueueUnderflowError, QueueOverflowError


def buat(no, tanggal):
    return Batch(no, "P1", "Produk", "Makanan", 10, 1000, tanggal)


class TestAntrian(unittest.TestCase):
    def test_dequeue_kosong(self):
        with self.assertRaises(QueueUnderflowError):
            Antrian().dequeue()

    def test_overflow(self):
        q = Antrian(2)
        q.enqueue(buat("A", date(2026, 1, 1)))
        q.enqueue(buat("B", date(2026, 1, 2)))
        with self.assertRaises(QueueOverflowError):
            q.enqueue(buat("C", date(2026, 1, 3)))

    def test_urutan_expiry(self):
        q = Antrian()
        q.enqueue(buat("B", date(2026, 3, 1)))
        q.enqueue(buat("A", date(2026, 1, 1)))
        q.enqueue(buat("C", date(2026, 2, 1)))
        urutan = [b.no_batch for b in q.ke_list()]
        self.assertEqual(urutan, ["A", "C", "B"])

    def test_expiry_sama_yang_duluan_masuk_keluar_duluan(self):
        q = Antrian()
        q.enqueue(buat("LAMA", date(2026, 1, 1)))
        q.enqueue(buat("BARU", date(2026, 1, 1)))
        self.assertEqual(q.dequeue().no_batch, "LAMA")

    def test_dequeue_dari_depan(self):
        q = Antrian()
        q.enqueue(buat("B", date(2026, 2, 1)))
        q.enqueue(buat("A", date(2026, 1, 1)))
        self.assertEqual(q.dequeue().no_batch, "A")
        self.assertEqual(q.jumlah(), 1)

    def test_hapus_depan_tengah_belakang(self):
        q = Antrian()
        for no, bulan in (("A", 1), ("B", 2), ("C", 3), ("D", 4)):
            q.enqueue(buat(no, date(2026, bulan, 1)))
        q.hapus("A")
        q.hapus("C")
        q.hapus("D")
        self.assertEqual([b.no_batch for b in q.ke_list()], ["B"])

    def test_hapus_batch_tidak_ada(self):
        with self.assertRaises(ValueError):
            Antrian().hapus("X")


if __name__ == "__main__":
    unittest.main()
