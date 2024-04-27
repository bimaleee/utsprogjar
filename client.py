import socket
import sys

# Membuat pemetaan antara warna dalam bahasa Indonesia dan bahasa Inggris
# Klien
KlienSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Membuat soket UDP
host = '127.0.0.1'  # Host lokal
port = 5555  # Port server

# Mengirim pesan kosong ke server untuk memulai komunikasi
KlienSocket.sendto(b'', (host, port))  # Mengirim pesan kosong ke server

berjalan = True  # Flag untuk menandai apakah program berjalan atau tidak
while berjalan:
    # Menerima warna dari server
    Respon, alamat = KlienSocket.recvfrom(1024)  # Menerima respon dari server
    warna = Respon.decode('utf-8')  # Mendecode pesan menjadi string
    print("[SERVER] Menerima warna dari server:", warna)  # Menampilkan pesan
    
    # Meminta jawaban dari pengguna dalam bahasa Indonesia
    jawaban = input("[SYSTEM] Apa warna ini? (Jawab dalam bahasa Indonesia): ")  # Meminta input dari pengguna
    
    # Mengirim jawaban pengguna ke server
    KlienSocket.sendto(str.encode(jawaban), (host, port))  # Mengirim jawaban ke server
    
    # Menerima umpan balik dari server
    umpan_balik, _ = KlienSocket.recvfrom(1024)  # Menerima umpan balik dari server
    print(umpan_balik.decode('utf-8'))  # Menampilkan umpan balik dari server

# Menutup koneksi soket saat loop selesai
KlienSocket.close()  # Menutup soket klien
sys.exit(0)  # Mengakhiri program dengan kode keluar 0