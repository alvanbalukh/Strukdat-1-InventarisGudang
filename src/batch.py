# kalau sisa hari <= angka ini, barang dianggap near-expired
AMBANG_NEAR_EXPIRED = 30


class Batch:
    def __init__(self, no_batch, kode, nama, kategori, jumlah, harga, expiry):
        self.no_batch = no_batch
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.jumlah = jumlah
        self.harga = harga
        self.expiry = expiry      # bertipe date

    def nilai(self):
        return self.jumlah * self.harga

    def sisa_hari(self, hari_ini):
        return (self.expiry - hari_ini).days

    def sudah_kedaluwarsa(self, hari_ini):
        return self.expiry < hari_ini

    def status(self, hari_ini):
        sisa = self.sisa_hari(hari_ini)
        if sisa < 0:
            return "KEDALUWARSA"
        elif sisa <= AMBANG_NEAR_EXPIRED:
            return "NEAR-EXPIRED"
        else:
            return "Aman"
