from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class RSAHandler:
    """
    Class untuk menangani operasi RSA, seperti:
    - Membuat keypair (public dan private key)
    - Enkripsi dan dekripsi pesan
    - Menyimpan dan memuat key ke/dari file
    """

    def __init__(self, key_size=2048):
        """
        Inisialisasi RSAHandler.
        key_size: Ukuran key RSA dalam bit (default: 2048, cukup aman untuk banyak keperluan).
        """
        self.key_size = key_size
        self.public_key = None  # Key public yang akan dihasilkan
        self.private_key = None  # Key private yang akan dihasilkan

    def generate_keypair(self):
        """
        Membuat keypair RSA (public dan private key).

        - public_key: Kunci publik untuk enkripsi.
        - private_key: Kunci privat untuk dekripsi.

        Return:
        Tuple (public_key, private_key).
        """
        key = RSA.generate(self.key_size)  # Membuat kunci dengan ukuran yang ditentukan
        self.public_key = key.publickey()  # Ekstrak kunci public dari key
        self.private_key = key  # Simpan kunci private
        return self.public_key, self.private_key

    @staticmethod
    def encrypt(public_key, message):
        """
        Mengenkripsi pesan dengan kunci public.

        Parameter:
        - public_key: Kunci public untuk enkripsi.
        - message: Pesan teks biasa yang ingin dienkripsi (string).

        Return:
        - Pesan terenkripsi dalam bentuk byte.
        """
        cipher = PKCS1_OAEP.new(public_key)  # Gunakan cipher OAEP untuk enkripsi
        encrypted_message = cipher.encrypt(
            message.encode()
        )  # Encode pesan ke byte, lalu enkripsi
        return encrypted_message

    @staticmethod
    def decrypt(private_key, encrypted_message):
        """
        dekripsi pesan terenkripsi dengan kunci private.

        Parameter:
        - private_key: Kunci private untuk dekripsi.
        - encrypted_message: Pesan yang telah terenkripsi (byte).

        Return:
        - Pesan asli yang telah didekripsi (string).
        """
        cipher = PKCS1_OAEP.new(private_key)  # Gunakan cipher OAEP untuk dekripsi
        decrypted_message = cipher.decrypt(
            encrypted_message
        ).decode()  # Dekripsi dan decode kembali ke string
        return decrypted_message

    @staticmethod
    def save_key(key, filename):
        """
        simpan kunci RSA (publik atau private) ke file.

        Parameter:
        - key: Kunci yang ingin disimpan.
        - filename: Nama file tempat kunci akan disimpan.
        """
        with open(filename, "wb") as f:
            f.write(key.export_key())  # Ekspor kunci ke format byte dan simpan di file

    @staticmethod
    def load_key(filename):
        """
        Memuat kunci RSA dari file.

        Parameter:
        - filename: Nama file tempat kunci disimpan.

        Return:
        - Kunci RSA yang telah dimuat (publik atau privat).
        """
        with open(filename, "rb") as f:
            return RSA.import_key(f.read())  # Baca file dan impor kembali ke format RSA
