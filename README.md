# 🎓 Panduan Penggunaan RSA Cryptography Program dengan Python 🛡️

## 🛠️ Asymmetric Encryption: Apa Itu dan Mengapa Penting?

Asymmetric encryption adalah metode enkripsi yang menggunakan dua kunci berbeda:

    - Public key (untuk enkripsi).
    - Private key (untuk dekripsi).

Berbeda dengan enkripsi simetris, di mana satu kunci yang sama digunakan untuk enkripsi dan dekripsi, enkripsi asimetris lebih aman karena private key hanya diketahui oleh penerimanya.

## 📖 Contoh Penggunaan di dunia nyata

    - Pengiriman Data Aman: Saat Anda mengakses situs web HTTPS, public key situs digunakan untuk mengenkripsi data yang Anda kirimkan (misalnya, kata sandi). Hanya situs tersebut yang dapat mendekripsi data dengan private key-nya.
    - Tanda Tangan Digital: Dokumen ditandatangani dengan private key pengirim, sehingga penerima dapat memverifikasi keaslian dokumen menggunakan public key.

---

## 🔐 Apa Itu RSA?

RSA (Rivest–Shamir–Adleman) adalah salah satu algoritma enkripsi asimetris paling populer. RSA digunakan karena:

    - Aman (asalkan menggunakan ukuran kunci yang cukup besar, seperti 2048-bit).
    - Mendukung berbagai skenario, seperti key exchange, tanda tangan digital, dan enkripsi pesan.

---

## 🛠️ PyCryptodome: Library Python untuk Kriptografi

PyCryptodome adalah pustaka Python yang mendukung operasi kriptografi modern, termasuk RSA. Pustaka ini menyediakan:

    - Algoritma kriptografi standar.
    - Dukungan untuk enkripsi RSA dengan berbagai padding, termasuk PKCS1_OAEP.

### 📦 Instalasi

Anda dapat menginstal PyCryptodome menggunakan pip:

```bash
pip install pycryptodome
```

---

## ✍️ Apa itu PKCS1_OAEP

PKCS1_OAEP (Optimal Asymmetric Encryption Padding) adalah metode padding untuk RSA yang meningkatkan keamanan enkripsi. Padding ini mencegah serangan berbasis struktur pesan dengan:

    - Menambahkan pengacak (randomizer).
    - Memastikan pesan yang sama akan menghasilkan enkripsi berbeda setiap kali.

---

## 🧑‍💻 Membuat Program RSA Cryptography

### 1️⃣ Modul rsa.py: Mengelola Kunci dan Enkripsi

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

### 2️⃣ Modul main.py: Penggunaanaan Dasar

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

### 3️⃣ Modul interactive.py: Menu Interaktif

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

## 🧪 Real World Applications

1. Chat Aman Antara Dua Orang

   - Pengguna A: Membuat pasangan kunci RSA dan membagikan public key kepada Pengguna B.
   - Pengguna B: Mengenkripsi pesan menggunakan public key A dan mengirim pesan terenkripsi.
   - Pengguna A: Mendekripsi pesan menggunakan private key mereka.

2. Pengamanan File Sensitif

   - File penting dapat dienkripsi sebelum disimpan atau dikirim. Hanya penerima dengan private key yang dapat membukanya.
