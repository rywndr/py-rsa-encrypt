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
