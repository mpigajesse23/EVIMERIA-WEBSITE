// Script de vérification du déploiement Netlify après configuration des variables d'environnement
const axios = require('axios');

// URL de base de l'API déployée sur Netlify
const NETLIFY_API_URL = 'https://evimeria.netlify.app/.netlify/functions/api';

// Fonction pour tester les endpoints API
async function testNetlifyAPI() {
  console.log('🔍 Test de l\'API EVIMERIA déployée sur Netlify...\n');
  console.log(`URL de base: ${NETLIFY_API_URL}`);

  try {
    // Test 1: Point d'entrée principal
    console.log('\n1️⃣ Test du point d\'entrée principal...');
    const rootResponse = await axios.get(NETLIFY_API_URL);
    console.log('✅ Statut:', rootResponse.status);
    console.log('📄 Réponse:', rootResponse.data);

    // Test 2: Endpoint des produits
    console.log('\n2️⃣ Test de l\'endpoint des produits...');
    const productsResponse = await axios.get(`${NETLIFY_API_URL}/products`);
    console.log('✅ Statut:', productsResponse.status);
    console.log(`📊 Nombre de produits: ${productsResponse.data.count}`);
    
    if (productsResponse.data.results && productsResponse.data.results.length > 0) {
      console.log('📦 Premier produit:', {
        id: productsResponse.data.results[0].id,
        name: productsResponse.data.results[0].name,
        price: productsResponse.data.results[0].price
      });
    } else {
      console.log('⚠️ Aucun produit trouvé!');
    }

    // Test 3: Endpoint des catégories
    console.log('\n3️⃣ Test de l\'endpoint des catégories...');
    const categoriesResponse = await axios.get(`${NETLIFY_API_URL}/categories`);
    console.log('✅ Statut:', categoriesResponse.status);
    console.log(`📊 Nombre de catégories: ${categoriesResponse.data.count}`);
    
    if (categoriesResponse.data.results && categoriesResponse.data.results.length > 0) {
      console.log('📁 Premières catégories:', categoriesResponse.data.results.slice(0, 3).map(cat => cat.name));
    } else {
      console.log('⚠️ Aucune catégorie trouvée!');
    }

    // Test 4: Endpoint de santé
    console.log('\n4️⃣ Test de l\'endpoint de santé...');
    const healthResponse = await axios.get(`${NETLIFY_API_URL}/health`);
    console.log('✅ Statut:', healthResponse.status);
    console.log('📄 Réponse:', healthResponse.data);

    console.log('\n✅ Tests terminés avec succès!');
    
  } catch (error) {
    console.log('\n❌ Erreur lors des tests:');
    
    if (error.response) {
      // La requête a été faite et le serveur a répondu avec un code d'erreur
      console.log(`Status: ${error.response.status}`);
      console.log('Headers:', error.response.headers);
      console.log('Data:', error.response.data);
      
      console.log('\n⚠️ Suggestions:');
      if (error.response.status === 404) {
        console.log('- Vérifiez que les redirections sont correctement configurées dans netlify.toml');
        console.log('- Vérifiez que la fonction api.js est bien déployée');
      } else if (error.response.status === 500) {
        console.log('- Vérifiez les journaux de fonctions dans le dashboard Netlify');
        console.log('- Vérifiez que les variables d\'environnement de Supabase sont correctes');
      }
    } else if (error.request) {
      // La requête a été faite mais aucune réponse n'a été reçue
      console.log('Aucune réponse reçue du serveur');
      console.log('\n⚠️ Suggestions:');
      console.log('- Vérifiez que le site est bien déployé sur Netlify');
      console.log('- Vérifiez que l\'URL est correcte');
    } else {
      // Une erreur s'est produite lors de la configuration de la requête
      console.log('Erreur:', error.message);
    }
    
    console.log('\n📋 Vérifications à faire:');
    console.log('1. Les variables d\'environnement sont-elles correctement définies dans Netlify?');
    console.log('2. Le déploiement a-t-il été déclenché après l\'ajout des variables?');
    console.log('3. Le fichier netlify.toml est-il correctement configuré?');
    console.log('4. La base de données Supabase est-elle accessible et contient-elle des données?');
  }
}

// Exécuter les tests
testNetlifyAPI();
