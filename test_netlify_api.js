// Test local de l'API Netlify Functions
// Script pour valider la connexion à Supabase et les endpoints

const { createClient } = require('@supabase/supabase-js');

// Configuration Supabase (même que dans api.js)
const supabaseUrl = 'https://jbxyihenvutqwkknlelh.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpienlpaGVudnV0cXdra25sZWxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI1NzQwOTAsImV4cCI6MjA0ODE1MDA5MH0.yU-VJNnfJAQ2MhzYOJZrmAJdpj5gOBnRkE9t_XJd_6s';

async function testSupabaseConnection() {
  console.log('🔌 Test de connexion à Supabase...\n');
  
  try {
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Test 1: Lecture des produits (test de connexion indirect)
    console.log('1️⃣ Test lecture des produits...');
    const { data: products, error: prodError, count: prodCount } = await supabase
      .from('products_product')
      .select('id, name, price, is_published', { count: 'exact' })
      .limit(5);
    
    if (prodError) {
      console.error('❌ Erreur produits:', prodError);
      throw prodError;
    } else {
      console.log(`✅ ${prodCount} produits trouvés`);
      console.log('📦 Échantillon:', products.slice(0, 3));
      console.log('');
    }
    
    // Test 2: Lecture des catégories
    console.log('2️⃣ Test lecture des catégories...');
    const { data: categories, error: catError, count: catCount } = await supabase
      .from('products_category')
      .select('id, name, is_published', { count: 'exact' });
    
    if (catError) {
      console.error('❌ Erreur catégories:', catError);
      throw catError;
    } else {
      console.log(`✅ ${catCount} catégories trouvées`);
      console.log('📁 Catégories:', categories.map(c => c.name));
      console.log('');
    }
    
    console.log('✅ Connexion Supabase fonctionnelle !');
    console.log('🎉 Tests terminés avec succès !');
    console.log('🚀 L\'API Netlify devrait fonctionner correctement.');
    
  } catch (error) {
    console.error('❌ Erreur lors des tests:', error.message);
    process.exit(1);
  }
}

// Simulation d'un appel à l'API Netlify
function simulateApiCall() {
  console.log('\n📡 Simulation d\'appels API Netlify...\n');
  
  const endpoints = [
    { path: '/', method: 'GET', desc: 'API Info' },
    { path: '/health', method: 'GET', desc: 'Health Check' },
    { path: '/products', method: 'GET', desc: 'Liste des produits' },
    { path: '/categories', method: 'GET', desc: 'Liste des catégories' }
  ];
  
  endpoints.forEach(endpoint => {
    console.log(`${endpoint.method} /.netlify/functions/api${endpoint.path} -> ${endpoint.desc}`);
  });
  
  console.log('\n✅ Tous ces endpoints seront disponibles après déploiement Netlify');
}

// Exécution des tests
async function runTests() {
  console.log('🧪 Test de l\'API EVIMERIA pour Netlify Functions\n');
  console.log('=' .repeat(60));
  
  await testSupabaseConnection();
  simulateApiCall();
  
  console.log('\n' + '=' .repeat(60));
  console.log('📋 Étapes suivantes:');
  console.log('1. Pousser le code vers GitHub');
  console.log('2. Connecter le dépôt à Netlify');
  console.log('3. Configurer les variables d\'environnement');
  console.log('4. Déployer automatiquement 🚀');
}

runTests().catch(console.error);
