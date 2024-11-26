# 🎓 Panduan Penggunaan RSA Cryptography Program dengan Python 🛡️

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

## 🧑‍💻 Membuat Program RSA Cryptography

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

Modul ini menambahkan antarmuka interaktif untuk pengguna. Anda dapat:

    - Membuat kunci RSA.
    - Mengenkripsi/mendekripsi pesan atau file.
    - Menyimpan kunci di lokasi tertentu.

#### Code snippet 📜:

```python
def main():
    display_ascii_art()
    print("Selamat datang di program RSA Cryptography!")
    while True:
        print("1. Generate RSA keypairs")
        print("2. Encrypt message")
        print("3. Decrypt message")
        print("6. Quit")
```

#### ✅ Penjelasan: Menu ini memandu pengguna melalui berbagai opsi dengan antarmuka berbasis teks.

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
