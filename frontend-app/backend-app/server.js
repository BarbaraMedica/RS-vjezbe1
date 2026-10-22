import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const PORT = process.env.PORT || 3000;

// Rješavanje putanja za ES Module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Middleware
app.use(cors());
app.use(express.json()); // Omogućuje čitanje JSON podataka u req.body

// Lažna baza podataka u memoriji
let zadaci = [
  { id: 1, naslov: 'Kupiti mlijeko', zavrseno: false },
  { id: 2, naslov: 'Popraviti Render deploy', zavrseno: true },
  { id: 3, naslov: 'Naučiti Express.js', zavrseno: false }
];

// --- REST API ENDPOINTS ---

// 1. GET: Dohvati sve zadatke
app.get('/api/zadaci', (req, res) => {
  res.json(zadaci);
});

// 2. POST: Dodaj novi zadatak
app.post('/api/zadaci', (req, res) => {
  const noviZadatak = {
    id: zadaci.length + 1,
    naslov: req.body.naslov,
    zavrseno: false
  };
  
  if (!noviZadatak.naslov) {
    return res.status(400).json({ poruka: 'Naslov je obavezan!' });
  }

  zadaci.push(noviZadatak);
  res.status(201).json(noviZadatak);
});

// 3. DELETE: Obriši zadatak prema ID-u
app.delete('/api/zadaci/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const duljinaPrije = zadaci.length;
  
  zadaci = zadaci.filter(z => z.id !== id);

  if (zadaci.length === duljinaPrije) {
    return res.status(404).json({ poruka: 'Zadatak nije pronađen!' });
  }

  res.json({ poruka: `Zadatak s ID-em ${id} je uspješno obrisan.` });
});


// --- POSLUŽIVANJE VUE.JS FRONTENDA (PRODUKCIJA) ---
// Govorimo Expressu da poslužuje statične datoteke iz Vue dist mape
// Pretpostavka je da se u produkciji 'dist' nalazi unutar backend mape ili relativno pokraj nje
app.use(express.static(path.join(__dirname, '../frontend-app/dist')));

// Bilo koji drugi zahtjev koji nije API vraća index.html (važno za Vue Router)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend-app/dist/index.html'));
});


// Pokretanje servera
app.listen(PORT, () => {
  console.log(`🚀 Server radi na http://localhost:${PORT}`);
});
