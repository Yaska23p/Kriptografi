Encryption Web App
=================
Aplikasi web untuk enkripsi dan dekripsi file menggunakan algoritma Simple XOR, RC4, DES, dan AES.

Cara Menjalankan
----------------
1. Instalasi Dependensi  
   Pastikan Python 3.12 sudah terinstal di sistem Anda. Kemudian, instal dependensi yang diperlukan dengan perintah:

   [python -m venv venv]		#buat virtual environment	
   [venv\Scripts\activate]		#aktifkan virtual environment
   [pip install flask pycryptodome]	#install pycryptodome flask

2. Jalankan Aplikasi  
   Untuk menjalankan aplikasi, buka terminal atau command prompt dan jalankan perintah berikut:
   
   [python app.py]
   
   Setelah dijalankan, aplikasi dapat diakses di browser melalui URL:
   
   [http://127.0.0.1:5000]
   

Struktur Proyek
---------------

encryption-web-app/
│── app.py         # File utama untuk menjalankan aplikasi Flask
│── encryption.py  # File untuk implementasi algoritma enkripsi dan dekripsi
│── templates/
│   └── index.html # Tampilan utama aplikasi
│── static/
│   └── style.css  # Styling untuk tampilan web
│── README.txt     # Dokumentasi ini


Fitur Aplikasi
--------------
✅ Enkripsi dan Dekripsi file (teks, gambar, PDF, audio, video)  
✅ Algoritma yang didukung:
   - Simple XOR
   - RC4
   - DES (ECB, CBC, Counter)
   - AES (ECB, CBC, Counter)
✅ Input dari teks atau file yang diunggah pengguna
✅ Output dapat berupa tampilan Base64 (untuk teks) atau file terenkripsi