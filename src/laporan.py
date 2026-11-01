from batch import AMBANG_NEAR_EXPIRED


def format_rupiah(angka):
    return "Rp" + f"{angka:,}".replace(",", ".")


def cetak_batch(daftar, hari_ini):
    print(f"{'No Batch':<12}{'Nama':<20}{'Jumlah':>7}{'Nilai':>15}  {'Expiry':<11}{'Sisa':>5}  Status")
    print("-" * 82)
    for b in daftar:
        print(f"{b.no_batch:<12}{b.nama:<20}{b.jumlah:>7}{format_rupiah(b.nilai()):>15}  "
              f"{str(b.expiry):<11}{b.sisa_hari(hari_ini):>5}  {b.status(hari_ini)}")


class Laporan:
    def __init__(self, gudang):
        self._gudang = gudang

    def near_expired(self, hari_ini):
        hasil = []
        for batch in self._gudang.semua_batch():
            sisa = batch.sisa_hari(hari_ini)
            if sisa >= 0 and sisa <= AMBANG_NEAR_EXPIRED:
                hasil.append(batch)
        return hasil

    def sudah_kedaluwarsa(self, hari_ini):
        hasil = []
        for batch in self._gudang.semua_batch():
            if batch.sudah_kedaluwarsa(hari_ini):
                hasil.append(batch)
        return hasil

    def total_nilai_aset(self):
        total = 0
        for batch in self._gudang.semua_batch():
            total += batch.nilai()
        return total

    def cetak_laporan(self, hari_ini):
        semua = self._gudang.semua_batch()
        total_unit = 0
        for b in semua:
            total_unit += b.jumlah

        print("=" * 82)
        print("LAPORAN HARIAN - " + str(hari_ini))
        print("=" * 82)
        print("Jumlah produk    :", len(self._gudang.daftar_kode()))
        print("Jumlah batch     :", len(semua))
        print("Total unit       :", total_unit)
        print("TOTAL NILAI ASET :", format_rupiah(self.total_nilai_aset()))

        print("\nBarang near-expired (sisa", AMBANG_NEAR_EXPIRED, "hari atau kurang):")
        near = self.near_expired(hari_ini)
        if len(near) == 0:
            print("  tidak ada")
        else:
            cetak_batch(near, hari_ini)

        print("\nBarang sudah kedaluwarsa (belum dibuang):")
        lewat = self.sudah_kedaluwarsa(hari_ini)
        if len(lewat) == 0:
            print("  tidak ada")
        else:
            cetak_batch(lewat, hari_ini)
