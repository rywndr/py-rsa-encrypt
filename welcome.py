import os

import pyfiglet
from termcolor import colored

"""
hanya script sederhana untuk estetika
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Clear the screen for better effect
clear_screen()

# Banner text with color
text = "H&M GROUP"
ascii_art = pyfiglet.figlet_format(text, font="doom")
colored_ascii_art = colored(ascii_art, "cyan", attrs=["bold"])
print(colored_ascii_art)

# Add some decorative separators
print(colored("★" * 60, "yellow"))
print(
    colored(
        "   🔐 Selamat Datang! Mari belajar tentang Kriptografi. 🔐",
        "green",
        attrs=["bold"],
    )
)
print(colored("★" * 60, "yellow"))

# Topic list with emojis and spacing
topics = [
    "1. 📜 Apa itu Asymmetric Encryption?",
    "2. 🔑 Apa itu RSA",
    "3. 📦 Pengenalan Pycryptodome",
    "4. 🏷️ Apa itu PKCS#1",
    "5. 📂 Apa itu PKCS#1 OAEP",
    "6. 🛠️ Cara RSA mengenerate keypair dan enkripsi/dekripsi pesan",
    "7. 💻 Demo",
]

print("\n" + colored("Topik yang akan dibahas:", "cyan", attrs=["bold"]) + "\n")
for topic in topics:
    print(colored(f"   {topic}", "white"))

# Closing remark
print(colored("★" * 60, "yellow"))
