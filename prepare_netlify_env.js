// Script pour générer un fichier d'environnement Netlify
const fs = require('fs');
const dotenv = require('dotenv');
const path = require('path');

console.log('🔧 Préparation des variables d\'environnement pour Netlify...');

// Charger les variables d'environnement depuis le fichier .env
const envConfig = dotenv.config();

if (envConfig.error) {
  console.error('❌ Erreur lors du chargement du fichier .env:', envConfig.error);
  process.exit(1);
}

// Variables critiques pour le déploiement Netlify
const criticalVars = [
  'SUPABASE_URL',
  'SUPABASE_ANON_KEY',
  'SUPABASE_SERVICE_ROLE_KEY',
  'VITE_API_URL',
  'VITE_SUPABASE_URL',
  'VITE_SUPABASE_ANON_KEY',
  'CLOUDINARY_CLOUD_NAME',
  'CLOUDINARY_API_KEY',
  'CLOUDINARY_API_SECRET'
];

// Création d'un objet pour le format Netlify
const netlifyEnv = {};
let missingVars = [];

// Filtrer les variables critiques
criticalVars.forEach(varName => {
  if (process.env[varName]) {
    netlifyEnv[varName] = process.env[varName];
    console.log(`✅ ${varName}: ${varName.includes('KEY') || varName.includes('SECRET') ? '***[SECRET]***' : process.env[varName]}`);
  } else {
    missingVars.push(varName);
    console.log(`❌ ${varName}: Non défini`);
  }
});

// Vérifier s'il y a des variables manquantes
if (missingVars.length > 0) {
  console.warn(`⚠️ Attention: ${missingVars.length} variable(s) critique(s) manquante(s): ${missingVars.join(', ')}`);
  console.warn('Ces variables sont importantes pour le bon fonctionnement de l\'application.');
}

// Créer un fichier JSON pour l'importation Netlify
const outputFile = path.join(__dirname, 'netlify-env.json');

try {
  fs.writeFileSync(outputFile, JSON.stringify(netlifyEnv, null, 2));
  console.log(`\n✅ Fichier de variables d'environnement créé: ${outputFile}`);
  
  // Générer un fichier texte avec les commandes pour l'interface CLI de Netlify
  const cliCommands = Object.entries(netlifyEnv)
    .map(([key, value]) => `netlify env:set ${key} "${value}"`)
    .join('\n');
  
  const cliFile = path.join(__dirname, 'netlify-env-commands.txt');
  fs.writeFileSync(cliFile, cliCommands);
  console.log(`✅ Commandes CLI générées dans: ${cliFile}`);
  
  console.log('\n📋 Instructions:');
  console.log('1. Pour importer via l\'interface web de Netlify:');
  console.log('   - Allez à: Site settings > Environment variables > Import from .env');
  console.log('   - Sélectionnez le fichier "netlify-env.json"');
  console.log('\n2. Pour importer via CLI (alternativement):');
  console.log('   - Utilisez les commandes générées dans "netlify-env-commands.txt"');
  console.log('   - Ou exécutez: netlify env:import .env');
  
} catch (error) {
  console.error(`❌ Erreur lors de la création du fichier: ${error.message}`);
}
