from rsa import RSAHandler


def main():
    """
    Fungsi utama untuk menjalankan program RSA Cryptography.
    Program ini akan:
    1. Membuat keypair RSA (public dan private).
    2. Menyimpan kunci ke file.
    3. Memuat kembali kunci dari file.
    4. Mengenkripsi pesan dengan kunci public.
    5. Mendekripsi pesan dengan kunci private.
    """
    rsa_handler = RSAHandler()
    print("RSA Cryptography Program")
    print("-------------------------")

    # 1. Generate keypair RSA
    """
    Membuat keypair public dan private.
    Public key digunakan untuk enkripsi, dan private key digunakan untuk dekripsi.
    """
    public_key, private_key = rsa_handler.generate_keypair()
    print("Public Key:")
    print(
        public_key.export_key().decode()
    )  # Menampilkan kunci public dalam format string
    print("Private Key:")
    print(
        private_key.export_key().decode()
    )  # Menampilkan kunci private dalam format string

    # 2. Simpan kunci ke file
    """
    Menyimpan kunci ke file dengan format:
    - "rsa_pkcs1_oaep.pub" untuk kunci public.
    - "rsa_pkcs1_oaep" untuk kunci private.
    """
    rsa_handler.save_key(public_key, "rsa_pkcs1_oaep.pub")
    rsa_handler.save_key(private_key, "rsa_pkcs1_oaep")

    # 3. Muat kembali kunci dari file
    """
    Memuat kunci public dan private dari file.
    Pastikan file sudah ada di direktori yang sama dengan program ini.
    """
    loaded_public_key = rsa_handler.load_key("rsa_pkcs1_oaep.pub")
    loaded_private_key = rsa_handler.load_key("rsa_pkcs1_oaep")
    print("Loaded Public Key:")
    print(
        loaded_public_key.export_key().decode()
    )  # Menampilkan kunci public yang dimuat
    print("Loaded Private Key:")
    print(
        loaded_private_key.export_key().decode()
    )  # Menampilkan kunci private yang dimuat

    # 4. Enkripsi pesan
    """
    Mengenkripsi pesan "Hello, World!" menggunakan kunci public.
    Hasil enkripsi ditampilkan dalam format hexadecimal untuk memudahkan pembacaan.
    """
    message = "Hello, World!"  # Pesan asli yang akan dienkripsi
    encrypted_message = rsa_handler.encrypt(public_key, message)
    print(
        "Encrypted Message:", encrypted_message.hex()
    )  # Konversi hasil enkripsi ke hexadecimal

    # 5. Dekripsi pesan
    """
    Mendekripsi pesan terenkripsi menggunakan kunci private.
    Hasil dekripsi harus sesuai dengan pesan asli.
    """
    decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
    print("Decrypted Message:", decrypted_message)  # Menampilkan pesan yang didekripsi


if __name__ == "__main__":
    """
    Entry point program.
    Program akan menjalankan fungsi main() saat file ini dijalankan langsung.
    """
    main()
