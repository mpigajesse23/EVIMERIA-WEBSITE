// Test local des endpoints de l'API Netlify
const axios = require('axios');

const apiUrl = 'http://localhost:8888/.netlify/functions/api';

async function testEndpoints() {
  console.log('🔍 Test des endpoints de l\'API Netlify locale...\n');
  
  try {
    // Test de l'endpoint racine
    console.log('1️⃣ Test de l\'endpoint racine...');
    const rootResponse = await axios.get(apiUrl);
    console.log('✅ Endpoint racine fonctionnel:');
    console.log(rootResponse.data);
    console.log('');
    
    // Test de l'endpoint health
    console.log('2️⃣ Test de l\'endpoint health...');
    const healthResponse = await axios.get(`${apiUrl}/health`);
    console.log('✅ Endpoint health fonctionnel:');
    console.log(healthResponse.data);
    console.log('');
    
    // Test de l'endpoint produits
    console.log('3️⃣ Test de l\'endpoint produits...');
    const productsResponse = await axios.get(`${apiUrl}/products`);
    console.log(`✅ Endpoint produits fonctionnel: ${productsResponse.data.count} produits trouvés`);
    if (productsResponse.data.results && productsResponse.data.results.length > 0) {
      console.log('Premier produit:');
      console.log(JSON.stringify(productsResponse.data.results[0], null, 2));
    }
    console.log('');
    
    // Test de l'endpoint catégories
    console.log('4️⃣ Test de l\'endpoint catégories...');
    const categoriesResponse = await axios.get(`${apiUrl}/categories`);
    console.log(`✅ Endpoint catégories fonctionnel: ${categoriesResponse.data.count} catégories trouvées`);
    if (categoriesResponse.data.results && categoriesResponse.data.results.length > 0) {
      console.log('Catégories:');
      categoriesResponse.data.results.forEach(cat => {
        console.log(`- ${cat.name}`);
      });
    }
    
    console.log('\n✅ Tous les endpoints fonctionnent correctement!');
    
  } catch (error) {
    console.error('❌ Erreur lors du test des endpoints:');
    if (error.response) {
      // La requête a été faite et le serveur a répondu avec un code d'état différent de 2xx
      console.error(`Statut: ${error.response.status}`);
      console.error('Réponse:', error.response.data);
    } else if (error.request) {
      // La requête a été faite mais aucune réponse n'a été reçue
      console.error('Aucune réponse reçue du serveur');
    } else {
      // Une erreur s'est produite lors de la configuration de la requête
      console.error('Erreur:', error.message);
    }
  }
}

testEndpoints();
