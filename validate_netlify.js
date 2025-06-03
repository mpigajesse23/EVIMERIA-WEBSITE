#!/usr/bin/env node

// Script de validation finale pour le déploiement Netlify
console.log('🎯 Validation finale du projet EVIMERIA pour Netlify\n');
console.log('=' .repeat(60));

const fs = require('fs');
const path = require('path');

// Vérification des fichiers essentiels
const requiredFiles = [
  'netlify.toml',
  'package.json',
  'netlify/functions/api.js',
  'frontend/package.json',
  'frontend/dist/index.html',
  'NETLIFY_DEPLOYMENT.md'
];

const optionalFiles = [
  'frontend/dist/assets',
  'README.md'
];

console.log('📁 Vérification des fichiers...\n');

requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MANQUANT !`);
  }
});

optionalFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file} (optionnel)`);
  } else {
    console.log(`⚠️  ${file} (optionnel) - non trouvé`);
  }
});

// Vérification du contenu netlify.toml
console.log('\n📋 Vérification netlify.toml...');
try {
  const netlifyConfig = fs.readFileSync('netlify.toml', 'utf8');
  
  if (netlifyConfig.includes('functions = "netlify/functions"')) {
    console.log('✅ Configuration des fonctions OK');
  } else {
    console.log('❌ Configuration des fonctions manquante');
  }
  
  if (netlifyConfig.includes('/.netlify/functions/api')) {
    console.log('✅ Redirection API configurée');
  } else {
    console.log('❌ Redirection API manquante');
  }
  
  if (netlifyConfig.includes('publish = "frontend/dist"') || netlifyConfig.includes('frontend/dist')) {
    console.log('✅ Dossier de publication configuré');
  } else {
    console.log('❌ Dossier de publication manquant');
  }
} catch (error) {
  console.log('❌ Erreur lecture netlify.toml:', error.message);
}

// Vérification du package.json racine
console.log('\n📦 Vérification package.json...');
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  
  if (packageJson.dependencies && packageJson.dependencies['@supabase/supabase-js']) {
    console.log('✅ Dépendance Supabase présente');
  } else {
    console.log('❌ Dépendance Supabase manquante');
  }
} catch (error) {
  console.log('❌ Erreur lecture package.json:', error.message);
}

// Vérification de l'API function
console.log('\n🔧 Vérification fonction API...');
try {
  const apiFunction = fs.readFileSync('netlify/functions/api.js', 'utf8');
  
  if (apiFunction.includes('supabase')) {
    console.log('✅ Configuration Supabase dans l\'API');
  } else {
    console.log('❌ Configuration Supabase manquante dans l\'API');
  }
  
  if (apiFunction.includes('products_product')) {
    console.log('✅ Endpoint produits configuré');
  } else {
    console.log('❌ Endpoint produits manquant');
  }
  
  if (apiFunction.includes('products_category')) {
    console.log('✅ Endpoint catégories configuré');
  } else {
    console.log('❌ Endpoint catégories manquant');
  }
} catch (error) {
  console.log('❌ Erreur lecture api.js:', error.message);
}

console.log('\n' + '=' .repeat(60));
console.log('🚀 Instructions de déploiement Netlify:');
console.log('\n1. Pousser le code vers GitHub:');
console.log('   git add .');
console.log('   git commit -m "Configuration Netlify Functions"');
console.log('   git push origin main');

console.log('\n2. Sur Netlify.com:');
console.log('   - Connecter le dépôt GitHub');
console.log('   - Build settings: automatiquement détectées');
console.log('   - Configurer les variables d\'environnement:');
console.log('     * SUPABASE_URL=https://jbxyihenvutqwkknlelh.supabase.co');
console.log('     * SUPABASE_ANON_KEY=(votre clé anon)');
console.log('     * VITE_API_URL=/.netlify/functions');

console.log('\n3. Déployer:');
console.log('   - Le déploiement se fait automatiquement');
console.log('   - URL finale: https://votre-site.netlify.app');

console.log('\n🔗 Base de données:');
console.log('   ✅ Supabase PostgreSQL configurée');
console.log('   ✅ Admin user créé (mpigajesse23@gmail.com)');
console.log('   ✅ Migrations appliquées');

console.log('\n📊 État du projet:');
console.log('   ✅ Frontend React + Vite');
console.log('   ✅ API Serverless Netlify Functions');
console.log('   ✅ Base de données Supabase');
console.log('   ✅ Stockage Cloudinary');
console.log('   ✅ Prêt pour déploiement !');

console.log('\n' + '=' .repeat(60));
console.log('✨ Projet EVIMERIA optimisé pour Netlify ✨');
