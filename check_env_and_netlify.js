// Vérification des variables d'environnement Netlify
const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');

// Charger les variables d'environnement
dotenv.config();

console.log('🔍 Vérification des variables d\'environnement pour Netlify...\n');

// Variables critiques à vérifier
const requiredVars = [
  'SUPABASE_URL',
  'SUPABASE_ANON_KEY',
  'VITE_API_URL'
];

// Vérifier les variables d'environnement
console.log('1️⃣ Variables d\'environnement:');
let missingVars = 0;

requiredVars.forEach(varName => {
  if (process.env[varName]) {
    console.log(`✅ ${varName}: ${varName.includes('KEY') ? '***[HIDDEN]***' : process.env[varName]}`);
  } else {
    console.log(`❌ ${varName}: Non défini`);
    missingVars++;
  }
});

// Vérifier si netlify.toml existe et contient les bonnes configurations
console.log('\n2️⃣ Configuration Netlify:');
const netlifyTomlPath = path.resolve(__dirname, 'netlify.toml');
let netlifyTomlContent = '';

try {
  netlifyTomlContent = fs.readFileSync(netlifyTomlPath, 'utf8');
  console.log('✅ netlify.toml trouvé');
  
  // Vérifier la configuration des fonctions
  if (netlifyTomlContent.includes('[functions]')) {
    console.log('✅ Configuration des fonctions trouvée');
  } else {
    console.log('❌ Configuration des fonctions manquante dans netlify.toml');
  }
  
  // Vérifier les redirections
  if (netlifyTomlContent.includes('from = "/api/*"') && 
      netlifyTomlContent.includes('to = "/.netlify/functions/api/:splat"')) {
    console.log('✅ Redirection API configurée correctement');
  } else {
    console.log('❌ Redirection API mal configurée ou manquante');
  }
  
  // Vérifier les variables d'environnement de contexte
  if (netlifyTomlContent.includes('VITE_API_URL = "/.netlify/functions"')) {
    console.log('✅ Variable VITE_API_URL configurée correctement dans netlify.toml');
  } else {
    console.log('❌ Variable VITE_API_URL mal configurée ou manquante dans netlify.toml');
  }
  
} catch (error) {
  console.log(`❌ Erreur lors de la lecture de netlify.toml: ${error.message}`);
}

// Vérifier si api.js existe
console.log('\n3️⃣ Fonction API:');
const apiFunctionPath = path.resolve(__dirname, 'netlify', 'functions', 'api.js');

try {
  fs.accessSync(apiFunctionPath);
  console.log('✅ api.js trouvé dans netlify/functions/');
  
  // Vérifier le contenu de api.js
  const apiContent = fs.readFileSync(apiFunctionPath, 'utf8');
  
  if (apiContent.includes('supabaseUrl') && apiContent.includes('supabaseKey')) {
    console.log('✅ Configuration Supabase trouvée dans api.js');
  } else {
    console.log('❌ Configuration Supabase manquante dans api.js');
  }
  
  if (apiContent.includes('/products') && apiContent.includes('from(\'products_product\')')) {
    console.log('✅ Endpoint des produits trouvé dans api.js');
  } else {
    console.log('❌ Endpoint des produits manquant dans api.js');
  }
  
} catch (error) {
  console.log(`❌ api.js non trouvé: ${error.message}`);
}

// Résumé et recommandations
console.log('\n📋 Résumé:');
if (missingVars > 0) {
  console.log(`❌ ${missingVars} variable(s) d'environnement manquante(s)`);
  console.log('⚠️ Assurez-vous de définir toutes les variables d\'environnement requises dans Netlify et dans votre fichier .env local');
} else {
  console.log('✅ Toutes les variables d\'environnement requises sont définies');
}

console.log('\n📌 Recommandations pour la production:');
console.log('1. Vérifiez que toutes les variables d\'environnement sont configurées dans le dashboard Netlify');
console.log('2. Vérifiez que la base de données Supabase est accessible depuis la fonction Netlify');
console.log('3. Vérifiez les journaux de déploiement Netlify pour tout message d\'erreur');
console.log('4. Vérifiez que les tables "products_product" et "products_category" existent dans Supabase et contiennent des données');
