# UTS PEMROGRAMAN JARINGAN
Disusun oleh :
>Bima Arya Wismaya Putra Dharma : 1203220099, Kelas : IF02-01

## Pertanyaan

Buatlah sebuah permainan yang menggunakan soket dan protokol UDP. Permainannya cukup sederhana, dengan 1 server dapat melayani banyak klien (one-to-many). Setiap 10 detik, server akan mengirimkan kata warna acak dalam bahasa Inggris kepada semua klien yang terhubung. Setiap klien harus menerima kata yang berbeda (unik). Selanjutnya, klien memiliki waktu 5 detik untuk merespons dengan kata warna dalam bahasa Indonesia. Setelah itu, server akan memberikan nilai feedback 0 jika jawabannya salah dan 100 jika benar.

syarat UTS :

    1. Kerjakan dengan menggunakan bahasa pemrograman python
    2. Menggunakan protokol UDP
    3. Code untuk server dan client dikumpulkan di github repository masing masing
    4. Pada readme.md silahkan beri penjelaskan how code works.
    5. Pada readme.md silahkan beri screenshoot cara penggunaaan serta contoh ketika program berjalan
    6. Test case : 1 server 10 client.
    7. Pastikan memahami soal.
    8. Silahkan kumpulkan link github repository di assignment ini.
    9. JANGAN TELAT !

## File yang diperlukan
silahkan download file server dan client dibawah ini
>Server https://github.com/bimaleee/utsprogjar/blob/main/server.py, Client https://github.com/bimaleee/utsprogjar/blob/main/client.py

## Penjelasan kode server
dibawah ini adalah code server
>import  socket
import  random
import  threading
import  time
import  sys
  
# Membuat pemetaan antara warna dalam bahasa Inggris dan bahasa Indonesia
pemetaan_warna  = {
	'red': 'merah',
	'yellow': 'kuning',
	'blue': 'biru',
	'orange': 'orange',
	'purple': 'ungu',
	'green': 'green',
	'brown': 'coklat',
	'black': 'hitam',
	'white': 'putih'
}

  
# Fungsi untuk mengatur timer respons klien
def  klien_timer_respons(alamat_klien):
	time.sleep(5) # Klien memiliki 5 detik untuk merespons
	if  not  respons_diterima.is_set():
		print("[SERVER] Waktu respons telah habis. Tidak ada respons yang diterima.")
		umpan_balik  =  0
		kunci_umpan_balik.acquire()
		try:
			umpan_baliks[alamat_klien] =  umpan_balik
		finally:
			kunci_umpan_balik.release()
SocketServer.sendto(b'[SERVER] Waktu habis!', alamat_klien) # Kirim pesan "Waktu habis" ke klien

  

# Fungsi untuk menghentikan utas pengirim warna dan menutup soket server

def  hentikan_server():
	global  berjalan
	berjalan  =  False  # Set flag berjalan menjadi False untuk menghentikan perulangan while di kode server utama
	utas_pengirim_warna.join() # Tunggu utas pengirim warna untuk selesai
	SocketServer.close() # Tutup soket server
	sys.exit(0) # Keluar dari program dengan kode keluar 0

  
  
  

# Fungsi untuk mengirim warna ke semua klien
def  kirim_warna_ke_klien(warna):
	for  alamat_klien  in  klien:
		SoketKlien.sendto(str.encode(warna), alamat_klien)

  

# Server
SocketServer  =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host  =  '127.0.0.1'
port  =  5555 
warna  =  list(pemetaan_warna.keys())
try:
	SocketServer.bind((host, port))
except  socket.error  as  e:
	print(str(e))  

print('[SERVER] Menunggu Koneksi..')

umpan_baliks  = {} # Kamus untuk menyimpan umpan balik dari klien
kunci_umpan_balik  =  threading.Lock() # Kunci untuk mengakses kamus umpan balik
respons_diterima  =  threading.Event() # Event untuk menandai apakah respons dari klien diterima
klien  =  set() # Set untuk menyimpan alamat klien yang terhubung 
# Tentukan SoketKlien
SoketKlien  =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
# Mulai utas untuk terus-menerus mengirim warna ke semua klien
def  pengirim_warna(berjalan): # Terima flag berjalan sebagai argumen
while  berjalan:
	warna_acak  =  random.choice(warna)
	kirim_warna_ke_klien(warna_acak)
	time.sleep(10) # Kirim warna setiap 10 detik
	utas_pengirim_warna  =  threading.Thread(target=pengirim_warna, args=(True,)) # Lewati True untuk menunjukkan berjalan
	utas_pengirim_warna.start()
	berjalan  =  True  # Tentukan flag berjalan di sini
	while  berjalan:
	data, alamat  =  SocketServer.recvfrom(1024)

	print('[CONNECTED] Terhubung dengan: '  +  alamat[0] +  ':'  +  str(alamat[1]))
	klien.add(alamat) # Tambahkan alamat klien ke set klien yang terhubung

	# Mulai timer untuk waktu respons klien
	utas_timer  =  threading.Thread(target=klien_timer_respons, args=(alamat,))
	utas_timer.start()

	# Kirim warna acak ke klien
	warna_acak  =  random.choice(warna)
	SocketServer.sendto(str.encode(warna_acak), alamat)

	# Terima respons dari klien
	respons_diterima.clear() # Tandai bahwa respons belum diterima
	Respons, _  =  SocketServer.recvfrom(1024)
	respons_diterima.set() # Tandai bahwa respons diterima

	# Periksa jawaban klien
	jawaban_klien  =  Respons.decode('utf-8').lower().strip() # Ubah ke huruf kecil dan hapus spasi
	jawaban_benar  =  pemetaan_warna[warna_acak] # Dapatkan terjemahan Indonesia dari warna yang benar
	umpan_balik  =  100  if  jawaban_klien  ==  jawaban_benar  else  0

	# Berikan umpan balik kepada klien
	kunci_umpan_balik.acquire()
	try:
		umpan_baliks[alamat] =  umpan_balik
	finally:
		kunci_umpan_balik.release()

	# Perbaiki jawaban dan berikan umpan balik
	if  umpan_balik  ==  100:
		print("[SERVER] Klien di {} menjawab dengan benar '{}'.".format(alamat, jawaban_klien))
		SocketServer.sendto(b'[SERVER] Jawaban Anda benar! Nilai Anda 100', alamat)            
	else:
		print("[SERVER] Klien di {} menjawab dengan salah '{}' (jawaban benar: '{}').".format(alamat, jawaban_klien, jawaban_benar))
		SocketServer.sendto(b'[SERVER] Jawaban Anda salah! Nilai Anda 0', alamat)

hentikan_server()
