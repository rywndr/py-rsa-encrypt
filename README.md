# 🎓 Program RSA Cryptography menggunakan standar PKCS1_OAEP dengan Python🛡️

## 🛠️ [Asymmetric Encryption](https://id.wikipedia.org/wiki/Kriptografi_kunci_publik): Apa Itu dan Mengapa Penting?

Asymmetric encryption adalah metode enkripsi yang menggunakan dua kunci berbeda:

    - Public key (untuk enkripsi).
    - Private key (untuk dekripsi).

Berbeda dengan enkripsi simetris, di mana satu kunci yang sama digunakan untuk enkripsi dan dekripsi, enkripsi asimetris lebih aman karena private key hanya diketahui oleh penerimanya.

## 📖 Contoh Penggunaan di dunia nyata

    - Pengiriman Data Aman: Saat Anda mengakses situs web HTTPS, public key situs digunakan untuk mengenkripsi data yang Anda kirimkan (misalnya, kata sandi). Hanya situs tersebut yang dapat mendekripsi data dengan private key-nya.
    - Tanda Tangan Digital: Dokumen ditandatangani dengan private key pengirim, sehingga penerima dapat memverifikasi keaslian dokumen menggunakan public key.

---

## 🔐 Apa Itu [RSA](https://id.wikipedia.org/wiki/RSA)?

RSA (Rivest–Shamir–Adleman) adalah salah satu algoritma enkripsi asimetris paling populer. RSA digunakan karena:

    - Aman (asalkan menggunakan ukuran kunci yang cukup besar, seperti 2048-bit).
    - Mendukung berbagai skenario, seperti key exchange, tanda tangan digital, dan enkripsi pesan.

---

## 🛠️ [PyCryptodome](https://www.pycryptodome.org): Library Python untuk Kriptografi

PyCryptodome adalah pustaka Python yang mendukung operasi kriptografi modern, termasuk RSA. Pustaka ini menyediakan:

    - Algoritma kriptografi standar.
    - Dukungan untuk enkripsi RSA dengan berbagai padding, termasuk PKCS1_OAEP.

### 📦 Instalasi

Anda dapat menginstal PyCryptodome menggunakan pip:

```bash
pip install pycryptodome
```

---

## PKCS#1 OAEP

### 🔑 **Apa itu [PKCS#1](https://en.wikipedia.org/wiki/PKCS_1)?**

PKCS#1 (Public Key Cryptography Standards #1) adalah standar yang mendefinisikan bagaimana menggunakan **RSA untuk enkripsi dan tanda tangan digital**. Standar ini mencakup:

- **Kompatibilitas** antar implementasi RSA yang berbeda.
- Cara melakukan padding (penambahan data acak) sebelum operasi kriptografi.
- Perlindungan terhadap **serangan keamanan**, seperti serangan ciphertext yang dipilih.

---

### 💡 **Mengapa RSA Membutuhkan Padding?**

RSA bekerja dengan memproses data dalam bentuk blok matematis. Namun, jika **RSA digunakan tanpa padding**, ada banyak risiko:

1. **Hasil yang Dapat Diprediksi:** Enkripsi pesan kecil seperti "123" atau "Hi" menghasilkan ciphertext yang mudah ditebak.
2. **Serangan Struktural:** Penyerang dapat mengeksploitasi pola ciphertext yang dapat diprediksi untuk menebak plaintext.

Padding menambahkan **randomness** dan struktur pada data, sehingga ciphertext menjadi tidak mudah ditebak dan lebih aman.

---

### 🔒 **Apa itu [PKCS#1 OAEP](https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html)?**

OAEP (Optimal Asymmetric Encryption Padding) adalah skema padding yang dirancang khusus untuk **RSA encryption** dalam standar PKCS#1. Tujuannya:

1. Menambahkan **randomness** pada plaintext agar setiap enkripsi menghasilkan ciphertext yang berbeda, meskipun plaintext-nya sama.
2. Melindungi RSA dari serangan canggih, seperti **chosen ciphertext attacks**.

#### **Bagaimana Cara Kerja OAEP?**

1. **Randomisasi Pesan:** Pesan dikombinasikan dengan nilai acak (seed) menggunakan fungsi hash untuk menghasilkan pesan yang teracak.
2. **Penambahan Struktur:** Pesan yang teracak diubah menjadi format yang terstruktur sebelum dienkripsi.
3. **Enkripsi RSA:** Algoritma RSA digunakan untuk mengenkripsi data yang sudah dipadding.

### 🧑‍🏫 **Perbandingan: Dengan dan Tanpa PKCS#1 OAEP**

#### **1. Tanpa Padding (RSA Tidak Aman):**

Jika menggunakan RSA tanpa padding:

- Pesan yang kecil atau mudah ditebak menghasilkan ciphertext yang dapat ditebak.
- Contoh:
  - Mengenkripsi `123` tanpa padding mungkin selalu menghasilkan ciphertext `C1`.
  - Jika seseorang melihat `C1` beberapa kali, mereka tahu bahwa itu adalah hasil enkripsi `123`.

#### **2. Dengan PKCS#1 OAEP (RSA Aman):**

- Setiap proses enkripsi melibatkan seed acak yang baru.
- Meskipun plaintext yang sama dienkripsi berkali-kali, ciphertext-nya akan selalu berbeda.

---

## 🧑‍💻 Panduan singkat Modul Program

### 1️⃣ Modul rsa.py: Modul utama untuk menangani operasi RSA

Modul ini menangani semua operasi dasar RSA:

    - Generate Keypair (Membuat kunci public dan private).
    - Encrypt (Mengenkripsi pesan).
    - Decrypt (Mendekripsi pesan).
    - Save Key (Menyimpan kunci ke file).
    - Load Key (Memuat kunci dari file).

#### Code snippet 📜:

```python
def generate_keypair(self):
    """
    Membuat keypair RSA (public dan private key).
    """
    key = RSA.generate(self.key_size)
    self.public_key = key.publickey()
    self.private_key = key
    return self.public_key, self.private_key
```

#### ✅ Penjelasan: Fungsi ini membuat pasangan kunci RSA dengan ukuran tertentu (2048-bit secara default).

---

### 2️⃣ Modul example.py: Program ringkas singkat Dedonstrasi

Ini adalah implementasi sederhana dari operasi RSA:

    - Membuat keypair.
    - Menyimpan dan memuat kunci.
    - Mengenkripsi dan mendekripsi pesan.

#### Code snippet 📜:

```python
encrypted_message = rsa_handler.encrypt(public_key, "Hello, World!")
print("Encrypted Message:", encrypted_message.hex())
```

#### ✅ Penjelasan: Pesan teks biasa dienkripsi menggunakan public key. Hasilnya ditampilkan dalam format hexadecimal untuk mempermudah pembacaan.

---

### 3️⃣ Modul main.py: Program Utama Interaktif

![Main Program Display](https://github.com/rywndr/rsa/blob/main/img/main.png?raw=true)

Modul ini menambahkan antarmuka interaktif untuk pengguna. Anda dapat:

    - Membuat Keypair RSA (Public key dan Private key).
    - Mengenkripsi Pesan yang di Inputkan oleh User
    - Mendekripsi Pesan yang di Inputkan oleh User
    - Mengenkripsi sebuah file yang di inputkan oleh User
    - Mendekripsi sebuah file yang di inputkan oleh User
    - Menjalankan program sebagai server untuk mensimulasikan pengiriman pesan antar server dan client
    - Menjalankan program sebagai client untuk mensimulasikan pengiriman pesan antar server dan client

### Option 1:

![gen-1](https://github.com/rywndr/rsa/blob/main/img/gen-1.png?raw=true)
Saat user memilih opsi 1, program akan menanyakan user ingin menyimpan folder kunci di mana. jika user tidak memberi opsi (biarkan kosong) maka program akan secara default menyimpan folder kunci yang berisi kunci public dan private nya di directory yang sama dengan program.

![gen-2](https://github.com/rywndr/rsa/blob/main/img/gen-2.png?raw=true)
Setelah user memilih dimana folder kunci akan disimpan, program akan membuat keypair RSA dan menyimpannya di folder yang telah ditentukan.

### Option 2:

![en1](https://github.com/rywndr/rsa/blob/main/img/en1.png?raw=true)
Saat user memilih opsi 2, program akan menanyakan user ingin mengenkripsi pesan apa. User dapat memasukkan pesan yang ingin dienkripsi.

![en2](https://github.com/rywndr/rsa/blob/main/img/en2.png?raw=true)
Setelah user memasukkan pesan yang ingin dienkripsi, program akan menampilkan byte dari pesan yang dienkripsi. dan hex dari byte tersebut dan menanyakan user apakah ingin menyimpan pesan yang dienkripsi ke file.

### Option 3:

![de-1](https://github.com/rywndr/rsa/blob/main/img/de-1.png?raw=true)
Saat user memilih opsi 3, program akan mendekripsi pesan yang telah di enkripsi user sebelumnya saat memilih opsi 2

### Option 4:

![enf-1](https://github.com/rywndr/rsa/blob/main/img/enf-1.png?raw=true)
Saat user memilih opsi 4, program akan menanyakan user ingin mengenkripsi file apa. User dapat memasukkan path dari file yang ingin dienkripsi.

![enf-2](https://github.com/rywndr/rsa/blob/main/img/enf-2.png?raw=true)
Setelah itu program akan memberitahu user bahwa file tersebut sudah berhasil di enkripsi dan di save sebagai nama file apa

### Option 5:

![def-1](https://github.com/rywndr/rsa/blob/main/img/def-1.png?raw=true)
Saat user memilih opsi 5, program akan bertanya ke user path dari file yang ingin di dekripsi

![def-2](https://github.com/rywndr/rsa/blob/main/img/def-2.png?raw=true)
Setelah itu program akan memberitahu user bahwa file tersebut sudah berhasil di dekripsi dan di save sebagai nama file apa

### Option 6:

![server](https://github.com/rywndr/rsa/blob/main/img/server.png?raw=true)
Untuk demonstrasi simulasi server dan client, kami menggunakan 2 linux virtual machine, yang satunya akan berperan sebagai server dan satunya lagi berperan sebagai client, dalam kasus ini servernya kami menggunakan Lubuntu dan client kami menggunakan Arch linux.

Saat user memilih opsi 6, program akan mensimulasikan pengiriman pesan antar server dan client dan akan mendengarkan network untuk incoming connection dari client, setelah client terhubung, server akan mengirimkan public key nya ke client dan client akan mengirimkan pesan yang ingin di enkripsi ke server, setelah server mendapatkan pesan tersebut, server akan mendekripsikan pesan yang baru saja diterima dari client.

### Option 7:

![client-1](https://github.com/rywndr/rsa/blob/main/img/client-1.png?raw=true)
Saat user memilih opsi 7, program akan mensimulasikan pengiriman pesan antar server dan client dan awalnya akan menanyakan IP address dari server yang ingin dihubungi.

![client-2](https://github.com/rywndr/rsa/blob/main/img/client-2.png?raw=true)
Setelah itu program akan mencoba untuk terhubung ke server yang telah ditentukan oleh user, setelah terhubung, client akan menerima public key dari server

![client-3](https://github.com/rywndr/rsa/blob/main/img/client-3.png?raw=true)
Setelah menerima public key dari server, client akan mengirimkan pesan yang ingin di enkripsi ke server, setelah server mendapatkan pesan tersebut, server akan mendekripsikan pesan yang baru saja diterima dari client.

### Note:

![re](https://github.com/rywndr/rsa/blob/main/img/re.png?raw=true)
Saat user memilih selain opsi quit dan opsi berperan sebagai client, dan user belum mengenerate keypair RSA, maka program akan memberitahu user untuk menggenerate keypair RSA atau menginputkan path dari folder kunci yang sudah ada.

#### Code snippet 📜:

```python
def main(stdscr):
    """
    Main function for interactive RSA Cryptography program.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    rsa_handler = RSAHandler()
    history = [display_ascii_art(stdscr)]  # Initialize history with ASCII art
    last_encrypted_message = None
    keys_folder = None

    menu = [
        "Generate RSA keypairs",
        "Encrypt message",
        "Decrypt message",
        "Encrypt file",
        "Decrypt file",
        "Acts as a server",
        "Acts as a client",
        "Quit",
    ]
```

#### ✅ Penjelasan: Menu ini memandu pengguna melalui berbagai opsi dengan antarmuka berbasis teks menggunakan curses

---

### 🛠️ Cara Menggunakan Program Ini (How To)

1. Clone repository ini menggunakan git:

```bash
git clone https://github.com/rywndr/rsa.git
```

2. Buka terminal dan pindah ke direktori program:

```bash
cd rsa
```

3. Install dependencies di requirements.txt menggunakan pip:

```bash
pip install -r requirements.txt
```

### 🚀 Menjalankan Program

1. Jalankan program example.py untuk melihat contoh penggunaan:

```bash
python example.py
```

2. Jalankan program main.py untuk menggunakan program interaktif:

```bash
python main.py
```

---

## 🧪 Real World Applications

1. Chat Aman Antara Dua Orang

   - User A: Membuat pasangan kunci RSA dan membagikan public key kepada User B.
   - User B: Mengenkripsi pesan menggunakan public key A dan mengirim pesan terenkripsi.
   - User A: Mendekripsi pesan menggunakan private key mereka.

2. Pengamanan File Sensitif

   - File penting dapat dienkripsi sebelum disimpan atau dikirim. Hanya penerima dengan private key yang dapat membukanya.

## **📚 References**

1. [RSA Cryptography - Wikipedia](https://id.wikipedia.org/wiki/RSA)
2. [Asymmetric Encryption - Wikipedia](https://en.wikipedia.org/wiki/Public-key_cryptography)
3. [PKCS#1 - Wikipedia](https://en.wikipedia.org/wiki/PKCS_1)
4. [PKCS#1 OAEP - PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html)
5. [PyCryptodome Documentation](https://www.pycryptodome.org)
6. [Pycryptodome - RSA Source Code](https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/PublicKey/RSA.py#L457-L536)
7. [PyCryptodome - PKCS_OAEP Source Code](https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/Cipher/PKCS1_OAEP.py#L196-L231)

---

## Repo structure

```bash
rsa/
├── src/
│   ├── lib/
│   │   ├── __init.py__
│   │   └── rsa.py
│   ├── example.py
│   └── main.py
├── .gitignore
├── README.md
├── requirements.txt
└── welcome.py
```

---

## 🧑‍💻 About the Authors

---

🎓 **Author 1:**

       _____
     _/ _ _ \_
    (o / | \ o)
     || o|o ||
     | \_|_/ |
     |  ___  |
     | (___) |
     |\_____/|
     | \___/ |
     \       /
      \__ __/
         U

- **Nama**: _Haikhal Roywendra_

---

🎓 **Author 2:**

    ░░░░░░░░░░░░░░░░░░░░░▄▀░░▌
    ░░░░░░░░░░░░░░░░░░░▄▀▐░░░▌
    ░░░░░░░░░░░░░░░░▄▀▀▒▐▒░░░▌
    ░░░░░▄▀▀▄░░░▄▄▀▀▒▒▒▒▌▒▒░░▌
    ░░░░▐▒░░░▀▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒█
    ░░░░▌▒░░░░▒▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
    ░░░░▐▒░░░░░▒▒▒▒▒▒▒▒▒▌▒▐▒▒▒▒▒▀▄
    ░░░░▌▀▄░░▒▒▒▒▒▒▒▒▐▒▒▒▌▒▌▒▄▄▒▒▐
    ░░░▌▌▒▒▀▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▒█▄█▌▒▒▌
    ░▄▀▒▐▒▒▒▒▒▒▒▒▒▒▒▄▀█▌▒▒▒▒▒▀▀▒▒▐░░░▄
    ▀▒▒▒▒▌▒▒▒▒▒▒▒▄▒▐███▌▄▒▒▒▒▒▒▒▄▀▀▀▀
    ▒▒▒▒▒▐▒▒▒▒▒▄▀▒▒▒▀▀▀▒▒▒▒▄█▀░░▒▌▀▀▄▄
    ▒▒▒▒▒▒█▒▄▄▀▒▒▒▒▒▒▒▒▒▒▒░░▐▒▀▄▀▄░░░░▀
    ▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▄▒▒▒▒▄▀▒▒▒▌░░▀▄
    ▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▀▀▀▀▒▒▒▄▀

- **Nama**: _Maria Febrianti_

🎉 Semoga Bermanfaat
