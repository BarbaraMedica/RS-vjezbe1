##Korutine iz prethodnog zadatka izvršite na dva različita načina:

#Za obje verzije izmjerite ukupno vrijeme izvođenja. Mjerenje mora obuhvatiti dohvaćanje svih skupina podataka.
#Za usporedbu koristite ista vremena čekanja za odgovarajuće korutine u obje verzije. Nasumična vremena možete
#generirati jednom prije mjerenja i proslijediti ih korutinama.
#Rezultate svake verzije objedinite u rječnik iste strukture

import asyncio
import random
import time

async def fetch_zadatke(): # primjer jednostavne korutine koja simulira dohvaćanje podataka
    print('Dohvaćam podatke s aplikacije...')
    data = [
        {"id": 1, "naslov": "Zadatak 1"},
        {"id": 2, "naslov": "Zadatak 2"},
        {"id": 3, "naslov": "Zadatak 3"}
    ]
    await asyncio.sleep(random.uniform(1, 3))
    return data

async def dohvati_korisnike():
    await asyncio.sleep(random.uniform(1, 3))
    return [
        {"id": 1, "ime": "Ana Horvat"},
        {"id": 2, "ime": "Marko Kovač"},
    ]


async def fetch_zadatakId(zadatak_id): # primjer jednostavne korutine koja simulira dohvaćanje podataka
    print(f'Dohvaćam podatke o id-u {zadatak_id}...')
    data = {'zadatak_id': zadatak_id, 'naslov': 'Naslov zadatka'}
    await asyncio.sleep(random.uniform(1, 3))
    return data
    
async def istovremeno(cekanja):
    t1 = time.perf_counter()
    zadaci, zadatak, korisnici = await asyncio.gather(
        fetch_zadatke(cekanja["zadaci"]),
        fetch_zadatakId(1, cekanja["zadatak"]),
        dohvati_korisnike(cekanja["korisnici"]),
    )
    t2 = time.perf_counter()
    return {
        "zadaci": zadaci,
        "zadatak": zadatak,
        "korisnici": korisnici,
        "vrijeme": t2 - t1,
    }   # ispisuje se prvo dio prve korutine, zatim dio druge i treće korutine, a ukupno vrijeme je vrijeme najdulje korutine

async def sekvencijalno(cekanja):
    t1 = time.perf_counter()
    zadaci = await fetch_zadatke(cekanja["zadaci"])
    zadatak = await fetch_zadatakId(1, cekanja["zadatak"])
    korisnici = await dohvati_korisnike(cekanja["korisnici"])
    t2 = time.perf_counter()
    return {
        "zadaci": zadaci,
        "zadatak": zadatak,
        "korisnici": korisnici,
        "vrijeme": t2 - t1,
    } # ispisuje se redom prva pa druga pa treća korutina, a ukupno vrijeme je zbroj vremena svih korutina


async def main():
    t1 = time.perf_counter()
    data = await asyncio.gather(
        fetch_zadatke(),
        fetch_zadatakId(1),
        dohvati_korisnike()
    )
    t2 = time.perf_counter()
    print(f'Podaci: {data}')
    print(f'Ukupno vrijeme izvođenja: {t2 - t1:.2f} s.')

  
asyncio.run(main())





   