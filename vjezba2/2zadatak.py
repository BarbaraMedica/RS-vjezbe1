import asyncio, time

async def dohvati_korisnike():
    await asyncio.sleep(3)
    return [{'id': 1, 'ime': 'Ana'}, {'id': 2, 'ime': 'Marko'}]

async def dohvati_proizvode():
    await asyncio.sleep(5)
    return [{'id': 1, 'naziv': 'Laptop'}, {'id': 2, 'naziv': 'Miš'}]

async def main():
    korisnici, proizvodi = await asyncio.gather(dohvati_korisnike(), dohvati_proizvode())
    print(korisnici)
    print(proizvodi)

t1 = time.perf_counter()
asyncio.run(main())
print(f"Vrijeme izvođenja: {time.perf_counter() - t1:.2f} s")  # ~5 s