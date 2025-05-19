import random
import os

KASUTAJAD_FILE = "mangijad.txt"
TULEMUSED_FILE = "tulemused.txt"

def loe_kaart():
    return random.randint(2, 11)

def lae_kasutajad():
    kasutajad = {}
    if os.path.exists(KASUTAJAD_FILE):
        with open(KASUTAJAD_FILE, "r", encoding="utf-8") as f:
            for rida in f:
                osad = rida.strip().split(":")
                if len(osad) == 2:
                    kasutajad[osad[0]] = int(osad[1])
    return kasutajad

def salvesta_kasutajad(kasutajad):
    with open(KASUTAJAD_FILE, "w", encoding="utf-8") as f:
        for nimi, fiske in kasutajad.items():
            f.write(f"{nimi}:{fiske}\n")

def kontrolli_kasutaja(nimi):
    kasutajad = lae_kasutajad()
    if nimi not in kasutajad:
        kasutajad[nimi] = 1000
        salvesta_kasutajad(kasutajad)
    return kasutajad

def registreeri_kasutaja(nimi):
    kasutajad = lae_kasutajad()
    if nimi not in kasutajad:
        kasutajad[nimi] = 1000
        salvesta_kasutajad(kasutajad)
        return True
    return False  # kasutaja on juba olemas

def uuenda_fiske(nimi, summa):
    kasutajad = lae_kasutajad()
    if nimi in kasutajad:
        kasutajad[nimi] += summa
        salvesta_kasutajad(kasutajad)

def salvesta_tulemus(nimi, tulemus, summa, fiske_jaak, muutus):
    with open(TULEMUSED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{nimi} - {'V\u00f5it' if tulemus else 'Kaotus'} - {summa} punkti - {'+' if tulemus else '-'}{muutus} fische - J\u00e4\u00e4k: {fiske_jaak}\n")

def loe_ajalugu(nimi):
    if not os.path.exists(TULEMUSED_FILE):
        return "Ajalugu puudub."
    with open(TULEMUSED_FILE, "r", encoding="utf-8") as f:
        return "\n".join([r for r in f if r.startswith(nimi)])

