import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url'; // Potrebno za simulaciju __dirname u ESM-u

const app = express();
const PORT = process.env.PORT || 3000;

// Popravak za __dirname u Module JS-u
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Omogućuje CORS kako bi frontend mogao komunicirati s backendom tijekom lokalnog razvoja
app.use(cors());
app.use(express.json());

// Privremena baza podataka u memoriji
let zadaci = [
  { id: 1, naslov: "Naučiti Express.js", zavrseno: false },
  { id: 2, naslov: "Deployati aplikaciju na Render", zavrseno: false }
];

// 1. GET - Dohvati sve zadatke
app.get('/api/zadaci', (req, res) => {
  res.json(zadaci);
});

// 2. POST - Dodaj novi zadatak
app.post('/api/zadaci', (req, res) => {
  const { naslov } = req.body;
  if (!naslov) {
    return res.status(400).json({ error: 'Naslov je obavezan' });
  }
  
  const noviZadatak = {
    id: Date.now(),
    naslov: naslov,
    zavrseno: false
  };
  
  zadaci.push(noviZadatak);
  res.status(201).json(noviZadatak);
});

// 3. DELETE - Obriši zadatak prema ID-u
app.delete('/api/zadaci/:id', (req, res) => {
  const id = parseInt(req.params.id);
  zadaci = zadaci.filter(z => z.id !== id);
  res.status(200).json({ message: 'Zadatak uspješno obrisan' });
});
// --- POSLUŽIVANJE VUE FRONTENDA (Za produkciju na Renderu) ---
app.use(express.static(path.join(__dirname, 'public')));

// Korištenje čistog regularnog izraza /(.*)/ rješava sve probleme s Express v5 i path-to-regexp alatom
app.get(/(.*)/, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});



app.listen(PORT, () => {
  console.log(`Server radi na portu ${PORT}`);
});
