from error import StokTidakCukupError


class Pembuangan:
    def __init__(self, gudang):
        self._gudang = gudang
        self.total_kerugian = 0

    def buang_rusak(self, no_batch, jumlah):
        # hasil: nilai kerugian
        hasil = self._gudang.cari_batch(no_batch)
        if hasil is None:
            raise ValueError("Batch " + no_batch + " tidak ditemukan")

        kode, batch = hasil
        if jumlah > batch.jumlah:
            raise StokTidakCukupError(
                "Jumlah rusak (" + str(jumlah) + ") lebih banyak dari stok batch (" + str(batch.jumlah) + ")")

        kerugian = jumlah * batch.harga
        if jumlah == batch.jumlah:
            self._gudang.get_antrian(kode).hapus(no_batch)    # batch habis, hapus dari antrean
        else:
            batch.jumlah -= jumlah

        self.total_kerugian += kerugian
        return kerugian

    def buang_kedaluwarsa(self, hari_ini):
        # antrean terurut dari expiry terdekat, jadi yang kedaluwarsa pasti di depan
        # hasil: list batch yang dibuang
        dibuang = []
        for kode in self._gudang.daftar_kode():
            antrian = self._gudang.get_antrian(kode)
            while not antrian.kosong() and antrian.peek().sudah_kedaluwarsa(hari_ini):
                batch = antrian.dequeue()
                self.total_kerugian += batch.nilai()
                dibuang.append(batch)
        return dibuang
