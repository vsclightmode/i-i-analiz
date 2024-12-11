import tkinter as tk
from tkinter import messagebox
import datetime
import os

def calisan_verilerini_kaydet(isim, soyisim, giris_saati, cikis_saati):
    bugun_tarihi = datetime.datetime.now().strftime("%Y-%m-%d")
    mesai_suresi = mesai_suresi_hesapla(giris_saati, cikis_saati)
    dosya_yolu = r"C:\Users\İndirilenler\işçi-analiz"
    dosya_adi = os.path.join(dosya_yolu, f"{isim}_{soyisim}.txt")

    if not os.access(dosya_yolu, os.W_OK):
        messagebox.showerror("Hata", f"Dosya yazma izniniz yok: {dosya_yolu}")
        return
    
    try:
        with open(dosya_adi, "a") as dosya:
            dosya.write("\n\n")
            dosya.write(f"Tarih: {bugun_tarihi}\n")
            dosya.write(f"Giriş Saati: {giris_saati.strftime('%H:%M')}\n")
            dosya.write(f"Çıkış Saati: {cikis_saati.strftime('%H:%M')}\n")
            dosya.write(f"Toplam Mesai Süresi: {mesai_suresi:.2f} saat\n")
        
        messagebox.showinfo("Başarılı", f"{isim.capitalize()} {soyisim.capitalize()} için mesai verileri kaydedildi.")
    
    except PermissionError:
        messagebox.showerror("Hata", f"Dosyaya yazma sırasında izin hatası: {dosya_adi}")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {str(e)}")

def mesai_suresi_hesapla(giris_saati, cikis_saati):
    mesai_suresi = cikis_saati - giris_saati
    return mesai_suresi.total_seconds() / 3600

def saat_formatlarini_kontrol_et(saat_str):
    saat_str = saat_str.replace(".", ":").replace(" ", ":")
    saat_formatlari = ["%H:%M", "%H:%M", "%H %M", "%H.%M", "%I:%M", "%I %M", "%I.%M"]
    
    for format in saat_formatlari:
        try:
            saat = datetime.datetime.strptime(saat_str, format)
            return saat
        except ValueError:
            continue
    return None

def isim_soyisim_gir(isim, soyisim):
    return isim.strip().capitalize(), soyisim.strip().capitalize()

def mesai_saati_gir(entry_saat):
    giris_saati_str = entry_saat.get()
    giris_saati = saat_formatlarini_kontrol_et(giris_saati_str)
    if giris_saati is None:
        messagebox.showerror("Hata", "Hatalı giriş saati formatı! Lütfen saati belirtilen formatlarda girin.")
        return None
    return giris_saati

def mesai_cikis_saati_gir(entry_saat):
    cikis_saati_str = entry_saat.get()
    cikis_saati = saat_formatlarini_kontrol_et(cikis_saati_str)
    if cikis_saati is None:
        messagebox.showerror("Hata", "Hatalı çıkış saati formatı! Lütfen saati belirtilen formatlarda girin.")
        return None
    return cikis_saati

def ana_menu():
    root = tk.Tk()
    root.title("Mesai Yönetim Sistemi")
    root.geometry("450x500")
    root.minsize(450, 500)
    
    frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Mesai Kayıt Sistemi", font=('Helvetica', 16, 'bold'), bg="#f0f0f0", fg="#007BFF").grid(row=0, column=0, columnspan=2, pady=15)

    tk.Label(frame, text="İsim:", font=('Helvetica', 12), bg="#f0f0f0", anchor="w").grid(row=1, column=0, pady=5, padx=10, sticky='w')
    entry_isim = tk.Entry(frame, font=('Helvetica', 12), bd=2, relief="solid", width=25)
    entry_isim.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(frame, text="Soyisim:", font=('Helvetica', 12), bg="#f0f0f0", anchor="w").grid(row=2, column=0, pady=5, padx=10, sticky='w')
    entry_soyisim = tk.Entry(frame, font=('Helvetica', 12), bd=2, relief="solid", width=25)
    entry_soyisim.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(frame, text="Giriş Saati (HH:MM):", font=('Helvetica', 12), bg="#f0f0f0", anchor="w").grid(row=3, column=0, pady=5, padx=10, sticky='w')
    entry_saat_giris = tk.Entry(frame, font=('Helvetica', 12), bd=2, relief="solid", width=25)
    entry_saat_giris.grid(row=3, column=1, pady=5, padx=10)

    tk.Label(frame, text="Çıkış Saati (HH:MM):", font=('Helvetica', 12), bg="#f0f0f0", anchor="w").grid(row=4, column=0, pady=5, padx=10, sticky='w')
    entry_saat_cikis = tk.Entry(frame, font=('Helvetica', 12), bd=2, relief="solid", width=25)
    entry_saat_cikis.grid(row=4, column=1, pady=5, padx=10)

    def move_focus(event, next_widget):
        next_widget.focus_set()

    entry_isim.bind("<Return>", lambda event: move_focus(event, entry_soyisim))
    entry_soyisim.bind("<Return>", lambda event: move_focus(event, entry_saat_giris))
    entry_saat_giris.bind("<Return>", lambda event: move_focus(event, entry_saat_cikis))
    entry_saat_cikis.bind("<Return>", lambda event: move_focus(event, save_button))

    def mesai_kaydet():
        isim = entry_isim.get()
        soyisim = entry_soyisim.get()
        
        if not isim or not soyisim:
            messagebox.showerror("Hata", "İsim ve soyisim alanları boş olamaz!")
            return

        isim, soyisim = isim_soyisim_gir(isim, soyisim)

        giris_saati = mesai_saati_gir(entry_saat_giris)
        if giris_saati is None:
            return

        cikis_saati = mesai_cikis_saati_gir(entry_saat_cikis)
        if cikis_saati is None:
            return

        calisan_verilerini_kaydet(isim, soyisim, giris_saati, cikis_saati)

    save_button = tk.Button(frame, text="Mesai Kaydet", command=mesai_kaydet, font=('Helvetica', 14), fg="white", bg="#007BFF", bd=2, relief="solid", width=20)
    save_button.grid(row=5, column=0, columnspan=2, pady=15)

    root.mainloop()

if __name__ == "__main__":
    ana_menu()
