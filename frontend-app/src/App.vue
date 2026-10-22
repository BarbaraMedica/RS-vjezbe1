<template>
  <div id="app">
    <header>
      <h1>🚀 Moja Jednostavna Vue Aplikacija</h1>
    </header>
    <main>
      <p>Ovo je statični sadržaj generiran iz Vue.js-a.</p>
      <button @click="povecajBrojac">Klikni me: {{ brojac }}</button>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const brojac = ref(0)
const povecajBrojac = () => {
  brojac.value++
}
</script>

<style scoped>
#app {
  font-family: sans-serif;
  text-align: center;
  margin-top: 50px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
