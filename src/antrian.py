from node import Node
from error import QueueUnderflowError, QueueOverflowError


class Antrian:
    def __init__(self, kapasitas=10):
        self._head = None        
        self._ukuran = 0
        self._kapasitas = kapasitas

    def kosong(self):
        return self._ukuran == 0

    def penuh(self):
        return self._ukuran >= self._kapasitas

    def jumlah(self):
        return self._ukuran

    def kapasitas(self):
        return self._kapasitas

    def enqueue(self, batch):
        if self.penuh():
            raise QueueOverflowError("Antrean penuh (maksimal " + str(self._kapasitas) + " batch)")

        baru = Node(batch)

        # kasus 1: antrean kosong, atau expiry batch baru paling awal 
        if self._head is None or batch.expiry < self._head.data.expiry:
            baru.next = self._head
            self._head = baru
        else:
            # kasus 2: cari tempat di tengah / belakang
            bantu = self._head
            while bantu.next is not None and bantu.next.data.expiry <= batch.expiry:
                bantu = bantu.next
            baru.next = bantu.next
            bantu.next = baru

        self._ukuran += 1

    def dequeue(self):
        if self.kosong():
            raise QueueUnderflowError("Antrean kosong, tidak ada batch yang bisa diambil")
        depan = self._head
        self._head = depan.next
        self._ukuran -= 1
        return depan.data

    def peek(self):
        if self.kosong():
            raise QueueUnderflowError("Antrean kosong")
        return self._head.data

    def cari(self, no_batch):
        bantu = self._head
        while bantu is not None:
            if bantu.data.no_batch == no_batch:
                return bantu.data
            bantu = bantu.next
        return None

    def hapus(self, no_batch):
        # hapus batch di posisi mana saja (depan / tengah / belakang)
        sebelum = None
        bantu = self._head
        while bantu is not None and bantu.data.no_batch != no_batch:
            sebelum = bantu
            bantu = bantu.next

        if bantu is None:
            raise ValueError("Batch " + no_batch + " tidak ditemukan")

        if sebelum is None:            # yang dihapus node paling depan
            self._head = bantu.next
        else:
            sebelum.next = bantu.next
        self._ukuran -= 1

    def ke_list(self):
        # dipakai untuk menampilkan isi antrean
        hasil = []
        bantu = self._head
        while bantu is not None:
            hasil.append(bantu.data)
            bantu = bantu.next
        return hasil
