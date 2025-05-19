import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from Mang_16_21 import (
    kontrolli_kasutaja,
    lae_kasutajad,
    loe_kaart,
    salvesta_tulemus,
    uuenda_fiske,
    loe_ajalugu,
    registreeri_kasutaja
)
import random

# --- SETUP ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1440x900")
app.title("Mäng 21")

font_header = ("Segoe UI", 24)
font_normal = ("Segoe UI", 16)

# --- Global state ---
kasutaja_nimi = None
kasutajad = {}
kaardid = []
skoor = 0
arvuti_skoor = 0
panus = 0

SUITS = ["spades", "hearts", "diamonds", "clubs"]

# --- Frames ---
main_menu = ctk.CTkFrame(app)
login_frame = ctk.CTkFrame(app)
register_frame = ctk.CTkFrame(app)
game_menu = ctk.CTkFrame(app)
result_frame = ctk.CTkFrame(app)

card_display_frame = ctk.CTkFrame(game_menu, fg_color="transparent")

def clear_frames():
    for frame in [main_menu, login_frame, register_frame, game_menu, result_frame]:
        frame.pack_forget()

def clear_cards():
    for widget in card_display_frame.winfo_children():
        widget.destroy()

def get_card_graphic(value):
    suit = random.choice(SUITS)
    suit_img = Image.open(f"assets/suits/{suit}.png").resize((20, 20))
    return value, ImageTk.PhotoImage(suit_img), suit

def show_card(value):
    number, icon, suit = get_card_graphic(value)
    frame = ctk.CTkFrame(card_display_frame, width=60, height=90, fg_color="#2b2d42", corner_radius=8)
    frame.pack_propagate(False)

    label_num = ctk.CTkLabel(frame, text=str(number), font=("Segoe UI", 16))
    label_suit = ctk.CTkLabel(frame, image=icon, text="", width=20, height=20)
    label_suit.image = icon
    label_num.pack(pady=(5, 0))
    label_suit.pack(pady=(0, 5))
    frame.pack(side="left", padx=5)

# --- Main Menu ---
def show_main_menu():
    clear_frames()
    main_menu.pack(expand=True)

def go_to_login():
    entry_login.delete(0, 'end')
    clear_frames()
    login_frame.pack(expand=True)

def go_to_register():
    entry_register.delete(0, 'end')
    clear_frames()
    register_frame.pack(expand=True)

main_label = ctk.CTkLabel(main_menu, text="Tere tulemast mängu 21!", font=font_header)
btn_login = ctk.CTkButton(main_menu, text="Logi sisse", command=go_to_login, width=300, height=40)
btn_register = ctk.CTkButton(main_menu, text="Registreeri", command=go_to_register, width=300, height=40)
btn_exit = ctk.CTkButton(main_menu, text="Välju", command=app.destroy, width=300, height=40)

main_label.pack(pady=30)
btn_login.pack(pady=10)
btn_register.pack(pady=10)
btn_exit.pack(pady=10)

# --- Registration ---
def register():
    name = entry_register.get().strip()
    if not name:
        messagebox.showwarning("Viga", "Sisesta kasutajanimi!")
    elif not name.isalnum():
        messagebox.showerror("Viga", "Lubatud on ainult tähed ja numbrid.")
    elif not registreeri_kasutaja(name):
        messagebox.showerror("Viga", "Kasutajanimi on juba olemas.")
    else:
        messagebox.showinfo("Valmis", "Registreeritud edukalt!")
        show_main_menu()

register_label = ctk.CTkLabel(register_frame, text="Registreeri", font=font_header)
entry_register = ctk.CTkEntry(register_frame, placeholder_text="Uus kasutajanimi", width=250)
btn_do_register = ctk.CTkButton(register_frame, text="Registreeri", command=register, width=300, height=40)
btn_back1 = ctk.CTkButton(register_frame, text="Tagasi", command=show_main_menu, width=300, height=40)

register_label.pack(pady=20)
entry_register.pack(pady=10)
btn_do_register.pack(pady=10)
btn_back1.pack(pady=10)

# --- Login ---
def login():
    global kasutaja_nimi, kasutajad
    name = entry_login.get().strip()
    kasutajad = lae_kasutajad()
    if not name:
        messagebox.showwarning("Viga", "Sisesta kasutajanimi!")
    elif name not in kasutajad:
        messagebox.showerror("Viga", "Kasutajat ei leitud.")
    else:
        kasutaja_nimi = name
        if kasutajad[kasutaja_nimi] == 0:
            messagebox.showinfo("Teade", "Sul on 0 fische. Palun lisa või loo uus kasutaja.")
        update_game_ui()
        clear_frames()
        game_menu.pack(expand=True)

login_label = ctk.CTkLabel(login_frame, text="Logi sisse", font=font_header)
entry_login = ctk.CTkEntry(login_frame, placeholder_text="Kasutajanimi", width=250)
btn_do_login = ctk.CTkButton(login_frame, text="Sisene", command=login, width=300, height=40)
btn_back2 = ctk.CTkButton(login_frame, text="Tagasi", command=show_main_menu, width=300, height=40)

login_label.pack(pady=20)
entry_login.pack(pady=10)
btn_do_login.pack(pady=10)
btn_back2.pack(pady=10)

# --- Game Menu ---
def update_game_ui():
    game_label.configure(text=f"Tere, {kasutaja_nimi}")
    fiske = lae_kasutajad().get(kasutaja_nimi, 0)
    fiske_label.configure(text=f"Fische: {fiske}")
    score_label.configure(text="Kaardid: - | Skoor: -")
    clear_cards()

def set_panustamine(mitmes):
    global panus
    fiske = lae_kasutajad().get(kasutaja_nimi, 0)
    if mitmes == "all":
        panus = fiske
    else:
        panus = int(fiske * mitmes)
    entry_panus.delete(0, "end")
    entry_panus.insert(0, str(panus))

def alusta_mang_panusega():
    global panus, kaardid, skoor, arvuti_skoor
    try:
        panus = int(entry_panus.get())
        fiske = lae_kasutajad().get(kasutaja_nimi, 0)
        if panus <= 0 or panus > fiske:
            raise ValueError
        kaardid = [loe_kaart(), loe_kaart()]
        skoor = sum(kaardid)
        arvuti_skoor = 0
        update_game_ui()
        score_label.configure(text=f"Kaardid: {kaardid} | Skoor: {skoor}")
        for kaart in kaardid:
            show_card(kaart)
    except:
        messagebox.showerror("Viga", "Sisesta kehtiv panus!")

def vota_kaart():
    global skoor
    kaart = loe_kaart()
    kaardid.append(kaart)
    skoor += kaart
    update_game_ui()
    score_label.configure(text=f"Kaardid: {kaardid} | Skoor: {skoor}")
    show_card(kaart)
    if skoor > 21:
        kaotus()

def kustuta_ajalugu():
    if not os.path.exists("tulemused.txt"):
        return
    with open("tulemused.txt", "r", encoding="utf-8") as f:
        uued = [r for r in f if not r.startswith(kasutaja_nimi)]
    with open("tulemused.txt", "w", encoding="utf-8") as f:
        f.writelines(uued)
    import os
    messagebox.showinfo("Ajalugu kustutatud", "Sinu mänguajalugu on kustutatud.")

def peatu():
    global arvuti_skoor
    while arvuti_skoor < 17:
        arvuti_skoor += loe_kaart()
    if arvuti_skoor > 21 or skoor > arvuti_skoor:
        voit()
    else:
        kaotus()

def voit():
    uuenda_fiske(kasutaja_nimi, panus)
    salvesta_tulemus(kasutaja_nimi, True, skoor, lae_kasutajad()[kasutaja_nimi], panus)
    show_result("Võitsid!", f"+{panus} fische")

def lisa_fische():
    global kasutaja_nimi
    fiske = lae_kasutajad().get(kasutaja_nimi, 0)
    if fiske >= 1000:
        messagebox.showinfo("Täis", "Sul on juba 1000 või rohkem fische.")
        return
    uuenda_fiske(kasutaja_nimi, 1000 - fiske)
    messagebox.showinfo("Lisatud", f"Sinu fiske täiendati kuni 1000-ni.")
    update_game_ui()

def kaotus():
    uuenda_fiske(kasutaja_nimi, -panus)
    salvesta_tulemus(kasutaja_nimi, False, skoor, lae_kasutajad()[kasutaja_nimi], panus)
    show_result("Kaotasid.", f"-{panus} fische")
    
    if lae_kasutajad()[kasutaja_nimi] == 0:
            messagebox.showinfo("Teade", "Sul on nüüd 0 fische. Palun lisa uusi või registreeri uuesti.")

def logout():
    global kasutaja_nimi
    kasutaja_nimi = None
    show_main_menu()

game_label = ctk.CTkLabel(game_menu, text="", font=font_header)
fiske_label = ctk.CTkLabel(game_menu, text="Fische: -", font=font_normal)
score_label = ctk.CTkLabel(game_menu, text="Skoor: -", font=font_normal)

entry_panus = ctk.CTkEntry(game_menu, placeholder_text="Sisesta panus", width=200)
btn_25 = ctk.CTkButton(game_menu, text="1/4", command=lambda: set_panustamine(0.25), width=120, height=35)
btn_50 = ctk.CTkButton(game_menu, text="1/2", command=lambda: set_panustamine(0.5), width=120, height=35)
btn_all = ctk.CTkButton(game_menu, text="All in", command=lambda: set_panustamine("all"), width=120, height=35)
btn_panus_start = ctk.CTkButton(game_menu, text="Alusta panusega", command=alusta_mang_panusega, width=250, height=35)

btn_vota = ctk.CTkButton(game_menu, text="Võta kaart", command=vota_kaart, width=250, height=35)
btn_peatu = ctk.CTkButton(game_menu, text="Peatu", command=peatu, width=250, height=35)
btn_ajalugu = ctk.CTkButton(game_menu, text="Vaata ajalugu", command=lambda: messagebox.showinfo("Sinu ajalugu", loe_ajalugu(kasutaja_nimi)), width=250, height=35)
btn_kustuta_ajalugu = ctk.CTkButton(game_menu, text="Kustuta ajalugu", command=kustuta_ajalugu, width=250, height=35)
btn_lisa_fiske = ctk.CTkButton(game_menu, text="Lisa fische", command=lisa_fische, width=250, height=35)
btn_logout = ctk.CTkButton(game_menu, text="Logi välja", command=logout, width=250, height=35)

# --- Pack layout ---
game_label.pack(pady=10)
fiske_label.pack(pady=5)
score_label.pack(pady=5)
card_display_frame.pack(pady=10)

entry_panus.pack(pady=5)
btn_25.pack(pady=2)
btn_50.pack(pady=2)
btn_all.pack(pady=2)
btn_panus_start.pack(pady=5)

btn_vota.pack(pady=4)
btn_peatu.pack(pady=4)
btn_ajalugu.pack(pady=10)
btn_kustuta_ajalugu.pack(pady=4)
btn_lisa_fiske.pack(pady=4)
btn_logout.pack(pady=4)


# --- Result ---
result_label = ctk.CTkLabel(result_frame, text="TULEMUS", font=font_header)
summary_label = ctk.CTkLabel(result_frame, text="", font=font_normal)
btn_back = ctk.CTkButton(result_frame, text="Tagasi menüüsse", command=lambda: (result_frame.pack_forget(), game_menu.pack(expand=True), update_game_ui()))

def show_result(status, info):
    result_label.configure(text=status)
    summary_label.configure(text=info)
    game_menu.pack_forget()
    result_frame.pack(expand=True)

result_label.pack(pady=20)
summary_label.pack(pady=10)
btn_back.pack(pady=10)

# Start
show_main_menu()
app.mainloop()
