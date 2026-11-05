# Zadatak koji će pripremati sintetičke podatke povezane s temom vaše aplikacije iz prethodne vježbe.


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
    print('Podaci dohvaćeni.')
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
    

async def main():
    data = await asyncio.gather(
        fetch_zadatke(),
        fetch_zadatakId(1),
        dohvati_korisnike()
    )
    print(f'Podaci: {data}') 



asyncio.run(main())





   