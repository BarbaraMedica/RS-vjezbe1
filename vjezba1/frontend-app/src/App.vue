<template>
  <div id="app" class="container">
    <header>
      <h1>🚀 Vue.js + Express.js Todo App</h1>
      <p class="subtitle">Svaki gumb gađa jedan endpoint Express API-ja</p>
    </header>

    <main>
      <!-- POST: dodaj zadatak -->
      <div class="input-group">
        <input
          v-model="noviZadatakNaslov"
          @keyup.enter="dodajZadatak"
          type="text"
          placeholder="Unesi novi zadatak..."
          :disabled="ucitava"
        />
        <button @click="dodajZadatak" :disabled="ucitava || !noviZadatakNaslov.trim()">
          Dodaj
        </button>
      </div>

      <!-- GET: osvježi + brojači + masovno brisanje -->
      <div class="toolbar">
        <button class="btn-sekundarni" @click="dohvatiZadatke" :disabled="ucitava">
          🔄 Osvježi (GET)
        </button>
        <button
          class="btn-sekundarni"
          @click="obrisiZavrsene"
          :disabled="ucitava || brojZavrsenih === 0"
        >
          🧹 Obriši završene ({{ brojZavrsenih }})
        </button>
      </div>
      <p class="brojac">Ukupno: {{ zadaci.length }} | Završeno: {{ brojZavrsenih }}</p>

      <div v-if="ucitava" class="loading">Učitavam podatke s API-ja...</div>

      <ul v-else class="todo-list">
        <li v-for="zadatak in zadaci" :key="zadatak.id" :class="{ zavrseno: zadatak.zavrseno }">
          <!-- PATCH: završeno / nije završeno -->
          <input
            type="checkbox"
            class="checkbox"
            :checked="zadatak.zavrseno"
            @change="promijeniStatus(zadatak)"
            title="Označi kao završeno"
          />

          <!-- PATCH: uređivanje naslova -->
          <input
            v-if="uredivanjeId === zadatak.id"
            v-model="uredivanjeNaslov"
            class="uredi-input"
            @keyup.enter="spremiNaslov(zadatak)"
            @keyup.esc="uredivanjeId = null"
            autofocus
          />
          <span v-else class="zadatak-tekst" @dblclick="zapocniUredivanje(zadatak)">
            {{ zadatak.naslov }}
          </span>

          <div class="akcije">
            <button
              v-if="uredivanjeId === zadatak.id"
              class="btn-ikona"
              @click="spremiNaslov(zadatak)"
              title="Spremi"
            >
              💾
            </button>
            <button v-else class="btn-ikona" @click="zapocniUredivanje(zadatak)" title="Uredi">
              ✏️
            </button>

            <!-- DELETE: obriši zadatak -->
            <button class="btn-ikona btn-obrisi" @click="obrisiZadatak(zadatak.id)" title="Obriši">
              ❌
            </button>
          </div>
        </li>
        <li v-if="zadaci.length === 0" class="empty-state">
          Nema aktivnih zadataka. Dodaj novi iznad!
        </li>
      </ul>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Dev: backend na portu 3000. Produkcija (Render): isti server, relativni URL.
const API_URL = import.meta.env.DEV
  ? 'http://localhost:3000/api/zadaci'
  : '/api/zadaci'

const zadaci = ref([])
const noviZadatakNaslov = ref('')
const ucitava = ref(false)
const uredivanjeId = ref(null)
const uredivanjeNaslov = ref('')

const brojZavrsenih = computed(() => zadaci.value.filter(z => z.zavrseno).length)

// GET - dohvati sve zadatke
const dohvatiZadatke = async () => {
  ucitava.value = true
  try {
    const odgovor = await fetch(API_URL)
    if (!odgovor.ok) throw new Error('Greška pri dohvaćanju')
    zadaci.value = await odgovor.json()
  } catch (error) {
    console.error(error)
    alert('Nije moguće komunicirati s backendom!')
  } finally {
    ucitava.value = false
  }
}

// POST - dodaj zadatak
const dodajZadatak = async () => {
  if (!noviZadatakNaslov.value.trim()) return
  try {
    const odgovor = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ naslov: noviZadatakNaslov.value.trim() })
    })
    if (!odgovor.ok) throw new Error('Greška pri dodavanju')
    zadaci.value.push(await odgovor.json())
    noviZadatakNaslov.value = ''
  } catch (error) {
    console.error(error)
    alert('Dodavanje zadatka nije uspjelo.')
  }
}

// PATCH - pošalje izmjene (zavrseno i/ili naslov) i zamijeni zadatak odgovorom servera
const azurirajZadatak = async (id, izmjene) => {
  const odgovor = await fetch(`${API_URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(izmjene)
  })
  if (!odgovor.ok) throw new Error('Greška pri izmjeni')
  const azuriran = await odgovor.json()
  const index = zadaci.value.findIndex(z => z.id === id)
  if (index !== -1) zadaci.value[index] = azuriran
}

const promijeniStatus = async (zadatak) => {
  try {
    await azurirajZadatak(zadatak.id, { zavrseno: !zadatak.zavrseno })
  } catch (error) {
    console.error(error)
    alert('Izmjena statusa nije uspjela.')
    await dohvatiZadatke() // vrati checkbox u stanje s servera
  }
}

const zapocniUredivanje = (zadatak) => {
  uredivanjeId.value = zadatak.id
  uredivanjeNaslov.value = zadatak.naslov
}

const spremiNaslov = async (zadatak) => {
  const naslov = uredivanjeNaslov.value.trim()
  if (!naslov) return
  try {
    await azurirajZadatak(zadatak.id, { naslov })
    uredivanjeId.value = null
  } catch (error) {
    console.error(error)
    alert('Spremanje naslova nije uspjelo.')
  }
}

// DELETE - obriši jedan zadatak
const obrisiZadatak = async (id) => {
  try {
    const odgovor = await fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    if (!odgovor.ok) throw new Error('Greška pri brisanju')
    zadaci.value = zadaci.value.filter(z => z.id !== id)
  } catch (error) {
    console.error(error)
    alert('Brisanje zadatka nije uspjelo.')
  }
}

// DELETE - obriši sve završene (više DELETE poziva)
const obrisiZavrsene = async () => {
  const zavrseni = zadaci.value.filter(z => z.zavrseno)
  await Promise.all(zavrseni.map(z => obrisiZadatak(z.id)))
}

onMounted(dohvatiZadatke)
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

header { text-align: center; margin-bottom: 30px; }
h1 { color: #35495e; font-size: 24px; margin-bottom: 5px; }
.subtitle { color: #41b883; margin: 0; font-size: 14px; font-weight: 600; }

.input-group { display: flex; gap: 10px; margin-bottom: 15px; }

input[type='text'] {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.2s;
}
input[type='text']:focus { border-color: #41b883; }

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}
button:hover:not(:disabled) { background-color: #35495e; }
button:disabled { background-color: #ccc; cursor: not-allowed; }

.toolbar { display: flex; gap: 10px; margin-bottom: 8px; }
.btn-sekundarni { flex: 1; font-size: 13px; padding: 8px 10px; background-color: #35495e; }
.btn-sekundarni:hover:not(:disabled) { background-color: #41b883; }
.brojac { font-size: 13px; color: #666; margin: 0 0 15px; text-align: center; }

.todo-list { list-style: none; padding: 0; margin: 0; }

li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #41b883; }

.zadatak-tekst { flex: 1; font-size: 16px; color: #333; cursor: text; }
li.zavrseno .zadatak-tekst { text-decoration: line-through; color: #888; }

.uredi-input { flex: 1; padding: 6px 8px !important; font-size: 15px !important; }

.akcije { display: flex; gap: 4px; }
.btn-ikona { background: none; padding: 5px 8px; font-size: 14px; }
.btn-ikona:hover:not(:disabled) { background: #e8f5ef; border-radius: 4px; }
.btn-obrisi:hover:not(:disabled) { background: #fee2e2; }

.loading, .empty-state {
  justify-content: center;
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px 0;
}
li.empty-state { background: none; box-shadow: none; }
</style>