<template>
  <div id="app" class="container">
    <header>
      <h1>🚀 Vue.js + Express.js Todo App</h1>
      <p class="subtitle">Aplikacija komunicira s Express REST API-jem</p>
    </header>

    <!-- Forma za dodavanje novog zadatka -->
    <main>
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

      <!-- Stanje učitavanja -->
      <div v-if="ucitava" class="loading">Učitavam podatke s API-ja...</div>

      <!-- Popis zadataka -->
      <ul v-else class="todo-list">
        <li v-for="zadatak in zadaci" :key="zadatak.id" :class="{ 'zavrseno': zadatak.zavrseno }">
          <span class="zadatak-tekst">{{ zadatak.naslov }}</span>
          <button @click="obrisiZadatak(zadatak.id)" class="btn-obrisi" title="Obriši zadatak">
            ❌
          </button>
        </li>
        <li v-if="zadaci.length === 0" class="empty-state">
          Nema aktivnih zadataka. Dodaj novi iznad!
        </li>
      </ul>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Automatski prepoznaje radi li na localhostu ili na Renderu (produkciji)
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:3000/api/zadaci' 
  : '/api/zadaci'

const zadaci = ref([])
const noviZadatakNaslov = ref('')
const ucitava = ref(false)

// 1. GET - Dohvati sve zadatke s backenda
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

// 2. POST - Pošalji novi zadatak na backend
const dodajZadatak = async () => {
  if (!noviZadatakNaslov.value.trim()) return

  try {
    const odgovor = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ naslov: noviZadatakNaslov.value })
    })

    if (!odgovor.ok) throw new Error('Greška pri dodavanju')
    
    const kreiraniZadatak = await odgovor.json()
    zadaci.value.push(kreiraniZadatak) // Osvježi UI bez ponovnog reloadanja
    noviZadatakNaslov.value = '' // Isprazni input polje
  } catch (error) {
    console.error(error)
    alert('Dodavanje zadatka nije uspjelo.')
  }
}

// 3. DELETE - Obriši zadatak na backendu prema ID-u
const obrisiZadatak = async (id) => {
  try {
    const odgovor = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE'
    })

    if (!odgovor.ok) throw new Error('Greška pri brisanju')

    // Ukloni iz lokalnog stanja kako bi UI odmah reagirao
    zadaci.value = zadaci.value.filter(z => z.id !== id)
  } catch (error) {
    console.error(error)
    alert('Brisanje zadatka nije uspjelo.')
  }
}

// Pokreni dohvaćanje čim se komponenta učita na ekranu
onMounted(() => {
  dohvatiZadatke()
})
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

header {
  text-align: center;
  margin-bottom: 30px;
}

h1 {
  color: #35495e;
  font-size: 24px;
  margin-bottom: 5px;
}

.subtitle {
  color: #41b883;
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #41b883;
}

button {
  padding: 0 20px;
  font-size: 16px;
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #35495e;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.todo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 6px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.zadatak-tekst {
  font-size: 16px;
  color: #333;
}

li.zavrseno .zadatak-tekst {
  text-decoration: line-through;
  color: #888;
}

.btn-obrisi {
  background: none;
  padding: 5px;
  font-size: 14px;
}
.btn-obrisi:hover {
  background: #fee2e2;
  border-radius: 4px;
}

.loading, .empty-state {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px 0;
}
</style>
