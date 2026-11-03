#objasnjenje ponašanja event loopa na primjeru:
import asyncio

async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f'{name}: {i} sekundi preostalo...')
        await asyncio.sleep(1)
    print(f'{name}: Vrijeme je isteklo!')

async def main():
    timers = [
        asyncio.create_task(timer('Timer 1', 3)),
        asyncio.create_task(timer('Timer 2', 5)),
        asyncio.create_task(timer('Timer 3', 7))
    ]

    await asyncio.gather(*timers)

asyncio.run(main())
#Na početku (t = 0 s)

#Program pokrene event loop, a main napravi tri timera (Timer 1, 2, 3) i rece: “čekam da svi završe” (gather). Nakon toga main miruje.
#Loop pokrene svaki timer. Svaki ispiše prvu poruku (3 sekundi preostalo, 5 sekundi preostalo, 7 sekundi preostalo) i zatim čeka 1 sekundu (await asyncio.sleep(1)).
#Dok svi čekaju, loop nema što raditi pa i on čeka.

#Svake sekunde (t = 1, 2, 3, ...)prođe sekunda, loop probudi timere koji su spremni.
#Svaki ispiše novi broj (npr. Timer 1: 2, Timer 2: 4, Timer 3: 6) i opet čeka 1 sekundu.

#Kad timer završi
#t = 3 s: Timer 1 ispiše Vrijeme je isteklo! i gotov je. Ostala dva nastavljaju.
#t = 5 s: Timer 2 je gotov.
#t = 7 s: Timer 3 je gotov.

#Na kraju (t = 7 s) - Kad su sva tri gotova, main se probudi, završi, a program se zatvori.

#Timeri ne čekaju jedan drugoga, nego čekaju istovremeno tj. paralelno se izvršavaju sva tri, prvi završi timer jedan dok su drugi već 3 sekunde svog vremena odradili. 
# Ukupno vrijeme zato je vrijeme najduljeg timera (7 s).