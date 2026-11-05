U ovoj vježbi napravila sam Python program zadatak3.py koji priprema sintetičke podatke za Todo aplikaciju iz prve vježbe (Vue + Express). Podaci se spremaju u podaci.json i prikazuju na frontendu.


Program ima tri korutine koje simuliraju dohvaćanje podataka iz vanjskih izvora:

fetch_zadatke simulira upit prema bazi zadataka i vraća popis zadataka (id i naslov).
fetch_zadatak_id simulira dohvat jednog zadatka prema njegovom ID-u.
dohvati_korisnike simulira upit prema bazi korisnika i vraća popis korisnika (id i ime).

Svaka korutina čeka nasumično vrijeme između 1 i 3 sekunde pomoću asyncio.sleep.

Korutine sam izvršila na dva načina. U sekvencijalnoj verziji svaka korutina se čeka s await jedna za drugom, pa se sljedeća pokreće tek kad prethodna završi. U konkurentnoj verziji sve tri korutine pokreću se odjednom pomoću asyncio.gather, pa se njihova čekanja odvijaju istovremeno.

Vremena čekanja generirana su samo jednom, prije mjerenja, i proslijeđena su objema verzijama kako bi usporedba bila poštena. Obje verzije vraćaju rječnik iste strukture sa zadacima, zadatkom, korisnicima i ukupnim vremenom. Vrijeme se mjeri pomoću time.perf_counter() i obuhvaća dohvaćanje sve tri skupine podataka.


Izmjereno vrijeme sekvencijalnog izvođenja bilo je <upiši> s, a konkurentnog <upiši> s.

Sekvencijalno vrijeme je otprilike zbroj sva tri čekanja, jer se korutine izvršavaju jedna nakon druge. Konkurentno vrijeme je otprilike jednako najdužem čekanju, jer se sva tri čekanja odvijaju istovremeno.

Odgovori na pitanja iz drugog zadatka
**1. Koliko traje izvođenje programa pri sekvencijalnoj obradi? Zašto?**

Trajalo je <7,07> s, otprilike zbroj sva tri čekanja. Svaka korutina čeka završetak prethodne, pa se vremena zbrajaju.

**2. Koliko traje izvođenje programa pri konkurentnoj jednodretvenoj obradi? Zašto?**

Trajalo je <2,95> s, otprilike koliko i najdulje čekanje. `asyncio.gather` pokreće sve korutine odjednom, pa se njihova čekanja preklapaju.

**3. Koja je glavna razlika između ovih dvaju načina izvođenja? Kako se korutine izvršavaju unutar event loopa?**

Kod sekvencijalnog izvođenja korutine čekaju jedna drugu, a kod konkurentnog se čekanja preklapaju. Event loop izvršava korutinu do `await`, a dok ona čeka, pokreće drugu. Kad čekanje istekne, nastavlja prvu od mjesta gdje je stala. Sve se događa u jednoj dretvi.

**4. Što se događa ako zamijenimo `asyncio.sleep` s `time.sleep`? Koja je tehnička razlika?**

Konkurentna verzija trajala bi koliko i sekvencijalna. `time.sleep` blokira cijelu dretvu pa event loop ne može pokrenuti druge korutine, dok `asyncio.sleep` s `await` vraća kontrolu event loopu i omogućuje izvršavanje drugih korutina.


Frontend sam nadogradila na postojećoj lokaciji iz prve vježbe (vjezba1/frontend-app). U App.vue učitava se podaci.json i prikazuju se izmjerena vremena, korisnici, zadaci i zadatak prema ID-u.

Javni URL aplikacije: https://rs-vjezbe1-frontend.onrender.com/

Pokretanje

Program se pokreće iz mape vjezba3 naredbom:

python zadatak3.py

Program sprema podaci.json u mapu vjezba3, a kopiju i u vjezba1/frontend-app/public, odakle ga frontend učitava.