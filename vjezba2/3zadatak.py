import asyncio

baza_korisnika = [
    {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
    {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
    {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
    {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]

baza_lozinka = [
    {'korisnicko_ime': 'mirko123', 'lozinka': 'lozinka123'},
    {'korisnicko_ime': 'ana_anic', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'maja_0x', 'lozinka': 's324SDFfdsj234'},
    {'korisnicko_ime': 'zdeslav032', 'lozinka': 'deso123'}
]

async def autorizacija(korisnik_iz_baze, lozinka):
    await asyncio.sleep(2)  # simulacija dekripcije
    ime = korisnik_iz_baze['korisnicko_ime']
    spremljena = next(k['lozinka'] for k in baza_lozinka if k['korisnicko_ime'] == ime)
    if spremljena == lozinka:
        return f"Korisnik {ime}: Autorizacija uspješna."
    return f"Korisnik {ime}: Autorizacija neuspješna."

async def autentifikacija(korisnik):
    await asyncio.sleep(3)  # simulacija upita prema bazi
    nadjen = next(
        (k for k in baza_korisnika
         if k['korisnicko_ime'] == korisnik['korisnicko_ime'] and k['email'] == korisnik['email']),
        None
    )
    if nadjen is None:
        return f"Korisnik {korisnik['korisnicko_ime']} nije pronađen."
    return await autorizacija(nadjen, korisnik['lozinka'])

async def main():
    korisnik = {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com', 'lozinka': 'super_teska_lozinka'}
    print(await autentifikacija(korisnik))

asyncio.run(main())