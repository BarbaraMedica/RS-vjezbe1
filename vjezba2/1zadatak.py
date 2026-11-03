import asyncio

async def fetch_data():
    await asyncio.sleep(3)

    podaci = [i for i in range(1, 11)]

    print("Podaci dohvaćeni.")

    return podaci


async def main():
    rezultat = await fetch_data()
    print(rezultat)


asyncio.run(main())