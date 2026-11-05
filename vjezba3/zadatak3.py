import asyncio
import json
import random
import time
from pathlib import Path


async def fetch_zadatke(cekanje):
    await asyncio.sleep(cekanje)
    return [
        {"id": 1, "naslov": "Zadatak 1"},
        {"id": 2, "naslov": "Zadatak 2"},
        {"id": 3, "naslov": "Zadatak 3"},
    ]


async def fetch_zadatak_id(zadatak_id, cekanje):
    await asyncio.sleep(cekanje)
    return {"zadatak_id": zadatak_id, "naslov": "Naslov zadatka"}


async def dohvati_korisnike(cekanje):
    await asyncio.sleep(cekanje)
    return [
        {"id": 1, "ime": "Ana Horvat"},
        {"id": 2, "ime": "Marko Kovač"},
    ]


async def sekvencijalno(c):
    t1 = time.perf_counter()
    zadaci = await fetch_zadatke(c["zadaci"])
    zadatak = await fetch_zadatak_id(1, c["zadatak"])
    korisnici = await dohvati_korisnike(c["korisnici"])
    return {"zadaci": zadaci, "zadatak": zadatak, "korisnici": korisnici,
            "vrijeme": round(time.perf_counter() - t1, 2)}


async def istovremeno(c):
    t1 = time.perf_counter()
    zadaci, zadatak, korisnici = await asyncio.gather(
        fetch_zadatke(c["zadaci"]),
        fetch_zadatak_id(1, c["zadatak"]),
        dohvati_korisnike(c["korisnici"]),
    )
    return {"zadaci": zadaci, "zadatak": zadatak, "korisnici": korisnici,
            "vrijeme": round(time.perf_counter() - t1, 2)}


async def main():
    # vremena se generiraju jednom i koriste u obje verzije
    cekanja = {
        "zadaci": random.uniform(1, 3),
        "zadatak": random.uniform(1, 3),
        "korisnici": random.uniform(1, 3),
    }

    podaci = {
        "sekvencijalno": await sekvencijalno(cekanja),
        "istovremeno": await istovremeno(cekanja),
    }

    print(f"Sekvencijalno: {podaci['sekvencijalno']['vrijeme']} s")
    print(f"Istovremeno: {podaci['istovremeno']['vrijeme']} s")

    # spremi u public mapu frontenda (prilagodi putanju svojoj strukturi)
    izlaz = Path(__file__).parent.parent / "vjezba1" / "frontend-app" / "public" / "podaci.json"
    izlaz.parent.mkdir(parents=True, exist_ok=True)
    izlaz.write_text(json.dumps(podaci, ensure_ascii=False, indent=2), encoding="utf-8")


asyncio.run(main())