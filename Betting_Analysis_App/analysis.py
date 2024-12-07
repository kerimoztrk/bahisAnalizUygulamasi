import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Varsayılan değer
DEFAULT_MAC_SAYISI = 7
init(autoreset=True)

def takimBilgileriniCek(takim, takimDurumu):
    clear_screen()
    # İç saha veya deplasman URL'si
    if takimDurumu == 'home':
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari#home"
    elif takimDurumu == 'away':
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari#away"
    else:
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"  # Bu URL kısmını değiştirebilirsiniz.

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Maç sonuçlarını bulma
    maclar = soup.find_all("tr")
    galibiyetSayisi = 0
    toplamGol = 0
    sonMacSkoru = None
    for mac in maclar:
        skorElement = mac.find("a", class_="d-block rounded bg-secondary text-white fw-bolder py-1 px-1 text-nowrap")
        if skorElement:
            skor = skorElement.get_text(strip=True)
            golSayisi = skor.split("-")
            if len(golSayisi) == 2 and golSayisi[0].strip() and golSayisi[1].strip():
                try:
                    attigiGol = int(golSayisi[0])
                    golSayisiG2 = int(golSayisi[1])
                except ValueError:
                    continue
                evSahibi = mac.find("td", class_="text-start w-25").find("a").get_text(strip=True)
                deplasman = mac.find("td", class_="text-end w-25").find("a").get_text(strip=True)
                if takim.lower() == turkceKarakterDegistir(evSahibi.lower()):
                    toplamGol += attigiGol
                    if attigiGol > golSayisiG2:
                        galibiyetSayisi += 1
                    sonMacSkoru = f" {evSahibi} {skor} {deplasman}\n"
                elif takim.lower() == turkceKarakterDegistir(deplasman.lower()):
                    toplamGol += golSayisiG2
                    if attigiGol < golSayisiG2:
                        galibiyetSayisi += 1
                        sonMacSkoru = f" {evSahibi} {skor} {deplasman}\n"
    if galibiyetSayisi == 0:
        print(Fore.RED + f"{takim.capitalize()} Takımının galibiyeti yok.")
        return None, None, None
    else:
        return galibiyetSayisi, toplamGol, sonMacSkoru


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def turkceKarakterDegistir(takimAdi):
    takimAdi = takimAdi.replace("ı", "i")
    takimAdi = takimAdi.replace("ç", "c")
    takimAdi = takimAdi.replace("ş", "s")
    takimAdi = takimAdi.replace("ğ", "g")
    takimAdi = takimAdi.replace("ü", "u")
    takimAdi = takimAdi.replace("ö", "o")
    return takimAdi.replace(" ", "-")  # Boşlukları '-' ile değiştir


def tahminiMacSonucu(golTahmini):
    takim1Gol = int(golTahmini)
    takim2Gol = takim1Gol - 1 if takim1Gol > 0 else 0  # Takım2'nin gol sayısını belirle
    takim1 = turkceKarakterDegistir(takim1Entry.get())
    takim2 = turkceKarakterDegistir(takim2Entry.get())
    return f"Tahmini maç sonucu: {takim1.capitalize()} {takim1Gol} - {takim2Gol} {takim2.capitalize()} "


def sonMacBilgileriniCek(takim, macSayisi, takimDurumu):
    if takimDurumu == 'home':
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari#home"
    elif takimDurumu == 'away':
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari#away"
    else:
        url = f"https://m.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"  # Bu URL kısmını değiştirebilirsiniz.
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    maclar = soup.find_all("tr")
    sonMacGolSayilari = []
    macSayaci = 0

    for mac in maclar:
        skorElement = mac.find("a", class_= "d-block rounded bg-secondary text-white fw-bolder py-1 px-1 text-nowrap")
        if skorElement:
            skor = skorElement.get_text(strip=True)
            golSayisi = skor.split("-")
            if len(golSayisi) == 2 and golSayisi[0].strip() and golSayisi[1].strip():
                try:
                    golSayisiG1 = int(golSayisi[0])
                    golSayisiG2 = int(golSayisi[1])
                    sonMacGolSayilari.append(golSayisiG1)
                    sonMacGolSayilari.append(golSayisiG2)
                    macSayaci += 1
                except ValueError:
                    continue
                if macSayaci >= macSayisi:
                    break
    return sonMacGolSayilari


def ikiTakimliAnaliz():
    takim1 = turkceKarakterDegistir(takim1Entry.get())
    takim2 = turkceKarakterDegistir(takim2Entry.get())
    macSayisi = int(macSayisiEntry.get())

    if not takim1 or not takim2:
        messagebox.showerror("Hata", "Lütfen takımları girin.")
        return
    sonuc = ""
    takim1BilgileriniCek = takimBilgileriniCek(takim1, 'home')  # İç saha URL'si
    if takim1BilgileriniCek is None:
        return
    galibiyetSayisiG1, golSayisiG1, sonMacSkoruG1 = takim1BilgileriniCek

    takim2BilgileriniCek = takimBilgileriniCek(takim2, 'away')  # Deplasman URL'si
    if takim2BilgileriniCek is None:
        return
    galibiyetSayisiG2, golSayisiG2, sonMacSkoruG2 = takim2BilgileriniCek

    # Ev sahibi ve deplasman farkı
    if galibiyetSayisiG1 > galibiyetSayisiG2:
        evSahibiDurumu = "Ev sahibi takım daha güçlü."
    elif galibiyetSayisiG1 < galibiyetSayisiG2:
        evSahibiDurumu = "Deplasman takım daha güçlü."
    else:
        evSahibiDurumu = "İki takım da dengeyi sağlıyor."

    sonuc += f"{takim1.capitalize()}\nGalibiyet Sayısı: {galibiyetSayisiG1}\nGol Sayısı: {golSayisiG1}\n{sonMacSkoruG1}\n"
    sonuc += f"{takim2.capitalize()}\nGalibiyet Sayısı: {galibiyetSayisiG2}\nGol Sayısı: {golSayisiG2}\n{sonMacSkoruG2}\n"
    sonuc += f"Ev Sahibi Durumu: {evSahibiDurumu}\n"

    if galibiyetSayisiG1 is not None and galibiyetSayisiG2 is not None:
        if galibiyetSayisiG1 > galibiyetSayisiG2:
            sonuc += f"{takim1.capitalize()} Takımı {takim2.capitalize()}'yı simülasyona göre yenecek!\n"
        elif galibiyetSayisiG1 < galibiyetSayisiG2:
            sonuc += f"{takim2.capitalize()} Takımı {takim1.capitalize()}'ı simülasyona göre yenecek!\n"
        else:
            sonuc += f"İki takım arasındaki maç simülasyona göre berabere biter.\n"

    # Gol sayısı tahmini
    if galibiyetSayisiG1 is not None and galibiyetSayisiG2 is not None:
        takim1SonMacGol = sonMacBilgileriniCek(takim1, macSayisi, 'home')  # İç saha
        takim2SonMacGol = sonMacBilgileriniCek(takim2, macSayisi, 'away')  # Deplasman

        if len(takim1SonMacGol) < macSayisi or len(takim2SonMacGol) < macSayisi:
            messagebox.showerror("Hata", "Gol tahmini yapmak için yeterli veri bulunamadı.")
            return

        ortalamaGolTakim1 = sum(takim1SonMacGol) / len(takim1SonMacGol)
        ortalamaGolTakim2 = sum(takim2SonMacGol) / len(takim2SonMacGol)

        # Tahmin edilen gol sayısını hesapla
        ortalama_gol = (ortalamaGolTakim1 + ortalamaGolTakim2) / 2
        golTahmini = ortalama_gol + 0.25 if takim1SonMacGol[-1] > takim2SonMacGol[-1] else ortalama_gol

        sonuc += f"Maçta Muhtemelen {golTahmini:.2f} gol olacak.\n"

        # Maç sonucunu tahmin et
        tahminiSonuc = tahminiMacSonucu(golTahmini)
        sonuc += tahminiSonuc

    sonucLabel.config(text=sonuc)


# Arayüz
root = tk.Tk()
root.title("Futbol Analiz Programı")

frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

# Ev Sahibi Takım Label ve Entry
takim1Label = ttk.Label(frame, text="Ev Sahibi Takım:")
takim1Label.grid(row=0, column=0, sticky="w")

takim1Entry = ttk.Entry(frame)
takim1Entry.grid(row=0, column=1, padx=5, pady=5)

# Deplasman Takım Label ve Entry
takim2Label = ttk.Label(frame, text="Deplasman Takım:")
takim2Label.grid(row=1, column=0, sticky="w")

takim2Entry = ttk.Entry(frame)
takim2Entry.grid(row=1, column=1, padx=5, pady=5)

# Maç Sayısı Label ve Entry
macSayisiLabel = ttk.Label(frame, text="Maç Sayısı:")
macSayisiLabel.grid(row=2, column=0, sticky="w")

macSayisiEntry = ttk.Entry(frame)
macSayisiEntry.grid(row=2, column=1, padx=5, pady=5)

# Sonuç Button
sonucButton = ttk.Button(frame, text="Sonuçları Göster", command=ikiTakimliAnaliz)
sonucButton.grid(row=3, column=0, columnspan=2, pady=10)

# Sonuç Label
sonucLabel = ttk.Label(frame, text="", justify="left")
sonucLabel.grid(row=4, column=0, columnspan=2)

root.mainloop()
