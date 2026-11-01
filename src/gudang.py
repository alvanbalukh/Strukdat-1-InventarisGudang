from antrian import Antrian
from error import StokTidakCukupError


class Gudang:
    def __init__(self, kapasitas=10):
        self._kapasitas = kapasitas
        self._produk = {}      # kode produk -> Antrian berisi batch-batchnya

    def daftar_kode(self):
        return sorted(self._produk.keys())

    def get_antrian(self, kode):
        if kode not in self._produk:
            raise ValueError("Produk " + kode + " tidak ditemukan")
        return self._produk[kode]

    def total_stok(self, kode):
        total = 0
        for batch in self.get_antrian(kode).ke_list():
            total += batch.jumlah
        return total

    def semua_batch(self):
        hasil = []
        for kode in self.daftar_kode():
            hasil += self._produk[kode].ke_list()
        return hasil

    def cari_batch(self, no_batch):
        # hasil: (kode, batch), atau None kalau tidak ada
        for kode in self._produk:
            batch = self._produk[kode].cari(no_batch)
            if batch is not None:
                return (kode, batch)
        return None

    def restock(self, batch, hari_ini):
        if self.cari_batch(batch.no_batch) is not None:
            raise ValueError("Nomor batch " + batch.no_batch + " sudah ada")
        if batch.sudah_kedaluwarsa(hari_ini):
            raise ValueError("Barang sudah kedaluwarsa, tidak bisa masuk gudang")

        if batch.kode not in self._produk:
            self._produk[batch.kode] = Antrian(self._kapasitas)
        self._produk[batch.kode].enqueue(batch)

    def keluarkan_stok(self, kode, jumlah, hari_ini):
        # ambil dari batch expiry terdekat, kalau kurang lanjut ke batch berikutnya
        # hasil: list berisi (no_batch, jumlah yang diambil)
        antrian = self.get_antrian(kode)

        tersedia = self.total_stok(kode)
        if jumlah > tersedia:
            raise StokTidakCukupError(
                "Stok " + kode + " tidak cukup. Diminta " + str(jumlah) + ", tersedia " + str(tersedia))

        if antrian.peek().sudah_kedaluwarsa(hari_ini):
            raise ValueError("Ada batch kedaluwarsa di depan antrean, buang dulu lewat menu 5")

        hasil = []
        sisa = jumlah
        while sisa > 0:
            depan = antrian.peek()
            if depan.jumlah <= sisa:
                # batch ini habis diambil semua
                antrian.dequeue()
                sisa -= depan.jumlah
                hasil.append((depan.no_batch, depan.jumlah))
            else:
                # cukup ambil sebagian
                depan.jumlah -= sisa
                hasil.append((depan.no_batch, sisa))
                sisa = 0
        return hasil
