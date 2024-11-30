import os
import platform

from lib.rsa import RSAHandler


def clear_screen():
    """
    Fungsi untuk membersihkan terminal sesuai os.
    """
    # get curr os
    system = platform.system().lower()

    # clear terminal sesuai os
    if system == "windows":
        os.system("cls")
    else:
        os.system("clear")


def display_ascii_art():
    """
    Fungsi untuk menampilkan ASCII Art pada awal program.
    Hanya untuk estetika.
    """
    print(r"""
  ___ ___   ____     _____                                                                              
 /   |   \ /  _ \   /     \                                                                             
/    ~    \>  _ </\/  \ /  \                                                                            
\    Y    /  <_\ \/    Y    \                                                                           
 \___|_  /\_____\ \____|__  /                                                                           
       \/        \/       \/                                                                            
__________  _________   _____    ___________ _______  ________________________.___._____________________
\______   \/   _____/  /  _  \   \_   _____/ \      \ \_   ___ \______   \__  |   |\______   \__    ___/
 |       _/\_____  \  /  /_\  \   |    __)_  /   |   \/    \  \/|       _//   |   | |     ___/ |    |   
 |    |   \/        \/    |    \  |        \/    |    \     \___|    |   \\____   | |    |     |    |   
 |____|_  /_______  /\____|__  / /_______  /\____|__  /\______  /____|_  // ______| |____|     |____|   
        \/        \/         \/          \/         \/        \/       \/ \/                            
""")


def main():
    """
    Fungsi utama untuk menjalankan program interaktif RSA Cryptography.
    Program ini memberikan opsi seperti:
    - Membuat kunci RSA.
    - Mengenkripsi dan mendekripsi pesan.
    - Mengenkripsi dan mendekripsi file.
    """
    clear_screen()
    rsa_handler = RSAHandler()
    display_ascii_art()
    print("Selamat datang di program RSA Cryptography!")
    print("===========================================")

    keys_folder = None  # Variabel untuk menyimpan lokasi folder kunci.

    while True:
        """
        Menampilkan menu interaktif dengan opsi untuk pengguna.
        Pengguna dapat memilih tindakan yang ingin dilakukan.
        """
        print(r"""
╔══════════════════════════════╗
║ Option                       ║
║ 1. Generate RSA keypairs     ║
║ 2. Encrypt message           ║
║ 3. Decrypt message           ║
║ 4. Encrypt file              ║
║ 5. Decrypt file              ║
║ 6. (Q)uit                    ║
╚══════════════════════════════╝
        """)

        choice = input(
            "Input pilihan Anda: "
        ).strip()  # Meminta input pilihan dari pengguna.

        if choice == "1":
            """
            Opsi untuk membuat kunci RSA.
            Pengguna akan diminta untuk menentukan lokasi folder tempat menyimpan kunci.
            """
            save_path = input(
                "Input path dimana Anda ingin menyimpan folder .keys (default: direktori saat ini): "
            )
            if save_path == "":
                save_path = (
                    os.getcwd()
                )  # Gunakan direktori yang kini jika user tidak menyediakan input
            else:
                if not os.path.exists(save_path):
                    os.makedirs(save_path)  # Buat direktori jika belum ada.

            # Membuat folder .keys untuk menyimpan kunci.
            keys_folder = os.path.join(save_path, ".keys")
            if not os.path.exists(keys_folder):
                os.makedirs(keys_folder)

            # Generate kunci RSA.
            public_key, private_key = rsa_handler.generate_keypair()
            print("Public Key:")
            print(public_key.export_key().decode())  # Tampilkan kunci public.
            print("Private Key:")
            print(private_key.export_key().decode())  # Tampilkan kunci private.
            rsa_handler.save_key(
                public_key, os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
            )
            rsa_handler.save_key(
                private_key, os.path.join(keys_folder, "rsa_pkcs1_oaep")
            )
            print("Keypair berhasil di generate dan di simpan di: ", keys_folder)

        elif choice in ["2", "3", "4", "5"]:
            """
            Opsi untuk enkripsi/dekripsi pesan atau file.
            Jika folder kunci belum ditentukan, pengguna akan diminta untuk memasukkan lokasinya.
            """
            if keys_folder is None:
                keys_folder = input(
                    "Input path folder .keys atau ketik (R)etry jika Anda belum men-generate keypair : "
                )

                if keys_folder.lower() == "r" or keys_folder.lower() == "retry":
                    keys_folder = None
                    continue

                if not os.path.exists(keys_folder):
                    keys_folder = None
                    print("Folder tidak ditemukan. Silakan coba lagi.")
                    continue

            if choice == "2":
                # Mengenkripsi pesan.
                message = input("Input pesan yang ingin dienkripsi: ")
                public_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
                )
                encrypted_message = rsa_handler.encrypt(public_key, message)
                print("Encrypted Message:", encrypted_message.hex())

            elif choice == "3":
                # Mendekripsi pesan.
                encrypted_message = bytes.fromhex(
                    input("Input pesan yang ingin didekripsi (hex): ")
                )
                private_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep")
                )
                decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
                print("Decrypted Message:", decrypted_message)

            elif choice == "4":
                # Mengenkripsi file.
                filename = input("Input nama file yang ingin dienkripsi: ")
                public_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep.pub")
                )
                with open(filename, "r") as f:
                    message = f.read()
                encrypted_message = rsa_handler.encrypt(public_key, message)
                with open(filename + ".enc", "wb") as f:
                    f.write(encrypted_message)
                print("File berhasil dienkripsi dan dengan nama", filename + ".enc")

            elif choice == "5":
                # Mendekripsi file.
                filename = input("Input nama file yang ingin didekripsi: ")
                private_key = rsa_handler.load_key(
                    os.path.join(keys_folder, "rsa_pkcs1_oaep")
                )
                with open(filename, "rb") as f:
                    encrypted_message = f.read()
                decrypted_message = rsa_handler.decrypt(private_key, encrypted_message)
                with open(filename + ".dec", "w") as f:
                    f.write(decrypted_message)
                print("File berhasil didekripsi!")

        elif choice == "6" or choice.lower() == "q" or choice.lower() == "quit":
            # Keluar dari program.
            user_name = input("siapa namamu tuan? ")
            print(f"bye bye c u la8r {user_name} muah")
            break
        else:
            # Opsi tidak valid.
            print(f"Pilihan {choice} tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    """
    Entry point program.
    Program akan menjalankan fungsi main() saat file ini dijalankan langsung.
    """
    main()
