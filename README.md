# 🎓 Program RSA Cryptography menggunakan standar PKCS1_OAEP dengan Python🛡️

## 🛠️ [Asymmetric Encryption](https://id.wikipedia.org/wiki/Kriptografi_kunci_publik): Apa Itu dan Mengapa Penting?

Asymmetric encryption adalah metode enkripsi yang menggunakan dua kunci berbeda:

    - Public key (untuk enkripsi).
    - Private key (untuk dekripsi).

Berbeda dengan enkripsi simetris, di mana satu kunci yang sama digunakan untuk enkripsi dan dekripsi, enkripsi asimetris lebih aman karena private key hanya diketahui oleh penerimanya.

---

## 🔐 Apa Itu [RSA](https://id.wikipedia.org/wiki/RSA)?

RSA (Rivest–Shamir–Adleman) adalah salah satu algoritma enkripsi asimetris paling populer. RSA digunakan karena:

    - Aman (asalkan menggunakan ukuran kunci yang cukup besar, seperti 2048-bit).
    - Mendukung berbagai skenario, seperti key exchange, tanda tangan digital, dan enkripsi pesan.

---

## 🛠️ [PyCryptodome](https://www.pycryptodome.org): Library Python untuk Kriptografi

PyCryptodome adalah library Python yang mendukung operasi kriptografi modern, termasuk RSA. library ini menyediakan:

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

### Cara RSA mengenerate public key dan private key

RSA mengenerate keypair nya dengan rumus berikut:

$$
n = p \times q
$$

$$
\phi(n) = (p-1) \times (q-1)
$$

$$
e \times d \equiv 1 \mod \phi(n)
$$

- $n$ adalah modulus.
- $\phi(n)$ adalah fungsi Euler.
- $e$ adalah public exponent.
- $d$ adalah private exponent.

### Contoh penerapan

Dalam real world use, bilangan prima $p$ dan $q$ sangat besar dengan size yang terjangkau dari 512-bit hingga 4096-bit. untuk key RSA dengan size 2048-bit, $p$ dan $q$ yang masing masing memiliki 1024-bit contohnya seperti berikut:

- $p = 17976931348623159077083915679378745319786029604875601170644442368419718021615851936894783379586492554150218056548598050364644054819923910005079287700335581663922955313623907650873575991482257488503244106244568377487935765733613030598998494747701675311447958994840391119450181891351603588225485726099365070673

- $q = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171

contoh n =

$$
n = p \times q = 17976931348623159077083915679378745319786029604875601170644442368419718021615851936894783379586492554150218056548598050364644054819923910005079287700335581663922955313623907650873575991482257488503244106244568377487935765733613030598998494747701675311447958994840391119450181891351603588225485726099365070673 \times 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
$$

$$
n = 240780832282852088714762452107475009764837884210889828532945737721821616841386662315456478622572214179904415981624198491748169116366234088098682073116410114015825545098019366303244116682682
$$

maka dari itu, public key mengandung $n$ dan $e$ yaitu $e = 65537$ dan private key mengandung $n$ dan $d$, dimana d di hitung dari $e \times d \equiv 1 \mod \phi(n)$

#### Kenapa ini aman?

- Karena faktorisasi dari $n$ yang besar sangat sulit dihitung. Seseorang harus memecahkan faktorisasi dari $n$ untuk mendapatkan $p$ dan $q$ yang dimana secara komputasi sangat sulit dihitung untuk $n$ 2048-bit.

---

### Setelah mengetahui cara RSA mengenerate keypair nya, kita akan melihat bagaimana RSA mengenkripsi dan mendekripsi pesan

### Enkripsi

Saat mengenkripsi pesan, tiap karakter diubah menjadi bilangan bulat berdasarkan representasi ASCII nya masing masing.

Contoh:

Plaintext = "HELLO"
Konversi ASCII: [72, 69, 76, 76, 79]
Digabung menjadi satu bilangan: 7269767679

Setelah itu, bilangan tersebut dienkripsi menggunakan public key.

Untuk mengenkrisi pesan menggunakan public key ($n$, $e$), kita menggunakan rumus berikut:

$$
C = M^e \mod n
$$

- $C$ adalah ciphertext.
- $M$ adalah pesan yang dienkripsi.
- $e$ adalah public exponent.
- $n$ adalah modulus.

Contoh:

e = 65537 (public exponent yang biasa digunakan)
m = 7269767679
n = 240780832282852088714762452107475009764837884210889828532945737721821616841386662315456478622572214179904415981624198491748169116366234088098682073116410114015825545098019366303244116682682

c di kalkulasi menggunakan modular exponentiation

#### Tambahan = contoh enkripsi menggunakan PKCS#1 OAEP

OAEP = Optimal Asymmetric Encryption Padding. Sebuah skema padding

Contoh:

$m = 7269767679$

dengan padding menggunakan OAEP, m diubah menjadi:

$$
m = 0002...(random data)...7269767679
$$

Setelah itu, m dienkripsi menggunakan public key.

### Dekripsi

Saat mendekripsi pesan, ciphertext diubah kembali menjadi pesan asli menggunakan private key ($n$, $d$).

Untuk mendekripsi pesan menggunakan private key ($n$, $d$), kita menggunakan rumus berikut:

$$
M = C^d \mod n
$$

- $M$ adalah pesan yang didekripsi.
- $C$ adalah ciphertext.
- $d$ adalah private exponent.
- $n$ adalah modulus.

Contoh:

d = 152415787532388367504953515625666819450083828733760097552251181223112635269100888108037780593788270666394008965907259977997488977697537484345973954308188067
c = 7269767679
n = 240780832282852088714762452107475009764837884210889828532945737721821616841386662315456478622572214179904415981624198491748169116366234088098682073116410114015825545098019366303244116682682

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

## Untuk penjelasan kode yang lebih lengkap ada di module [example.py](https://github.com/rywndr/rsa/blob/main/src/example.py) dilengkapi dengan komentar tiap baris kode.

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
8. [The RSA Encryption Algorithm (1 of 2: Computing an Example)](https://www.youtube.com/watch?v=4zahvcJ9glg)
9. [The RSA Encryption Algorithm (2 of 2: Key Generation)](https://www.youtube.com/watch?v=oOcTVTpUsPQ&t=445s)
10. [How RSA Encryption Works](https://www.youtube.com/watch?v=ZPXVSJnDA_A)
11. [RSA Algorithm How does it work?](https://www.youtube.com/watch?v=Pq8gNbvfaoM)
12. [Crptography Standards explained.](https://www.youtube.com/watch?v=aao12RxwuiM&t=673s)
13. [OAEP - Applied Cryptography](https://www.youtube.com/watch?v=ZwPGE5GgG_E)

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
