// Script pour tester l'API Netlify depuis le navigateur
document.addEventListener('DOMContentLoaded', function() {
  const apiUrl = '/.netlify/functions/api';
  
  // Fonction pour afficher les résultats
  function displayResults(title, data) {
    const container = document.getElementById('results');
    
    const section = document.createElement('div');
    section.className = 'result-section';
    
    const heading = document.createElement('h2');
    heading.textContent = title;
    section.appendChild(heading);
    
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(data, null, 2);
    section.appendChild(pre);
    
    container.appendChild(section);
  }
  
  // Fonction pour les appels API
  async function callAPI(endpoint, title) {
    try {
      const response = await fetch(endpoint);
      const data = await response.json();
      displayResults(title, data);
      return data;
    } catch (error) {
      displayResults(`${title} (Erreur)`, { error: error.message });
      return null;
    }
  }
  
  // Tester l'endpoint principal
  callAPI(apiUrl, "Endpoint principal");
  
  // Tester l'endpoint des produits
  callAPI(`${apiUrl}/products`, "Produits");
  
  // Tester l'endpoint des catégories
  callAPI(`${apiUrl}/categories`, "Catégories");
  
  // Tester l'endpoint de santé
  callAPI(`${apiUrl}/health`, "État de santé");
});
