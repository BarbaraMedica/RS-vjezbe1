import asyncio, random

async def provjeri_parnost(broj):
    await asyncio.sleep(2)
    if broj % 2 == 0:
        return f"Broj {broj} je paran."
    return f"Broj {broj} je neparan."

async def main():
    brojevi = [random.randint(1, 100) for _ in range(10)]
    zadaci = [asyncio.create_task(provjeri_parnost(b)) for b in brojevi]
    rezultati = await asyncio.gather(*zadaci)
    for r in rezultati:
        print(r)

asyncio.run(main())  # traje priblizno 2 s ukupno
#rezultat:
# Broj 30 je paran.
# Broj 55 je neparan.
# Broj 92 je paran.
# Broj 23 je neparan.
# Broj 3 je neparan.
#Broj 40 je paran.
# Broj 75 je neparan.
# Broj 88 je paran.
# Broj 66 je paran.
# Broj 99 je neparan.
