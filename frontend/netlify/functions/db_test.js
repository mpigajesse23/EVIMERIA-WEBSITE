// Fonction Netlify pour tester la connexion Supabase
const { createClient } = require('@supabase/supabase-js');

exports.handler = async (event, context) => {
  // Configuration CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Gestion des requêtes OPTIONS (CORS preflight)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Configuration Supabase avec les variables d'environnement
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_ANON_KEY;
    
    // Information sur les variables d'environnement
    const envInfo = {
      supabaseUrl: supabaseUrl ? 'Défini' : 'Non défini',
      supabaseKey: supabaseKey ? 'Défini (secret)' : 'Non défini',
      nodeEnv: process.env.NODE_ENV || 'Non défini',
      viteApiUrl: process.env.VITE_API_URL || 'Non défini'
    };
    
    // Si les variables d'environnement ne sont pas définies
    if (!supabaseUrl || !supabaseKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          error: 'Configuration Supabase incomplète',
          message: 'Les variables d\'environnement nécessaires ne sont pas définies',
          environmentInfo: envInfo
        })
      };
    }
    
    // Création du client Supabase
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Test de connexion: récupérer le nombre de produits et catégories
    const [productsResult, categoriesResult] = await Promise.allSettled([
      supabase.from('products_product').select('id', { count: 'exact' }),
      supabase.from('products_category').select('id', { count: 'exact' })
    ]);
    
    const productCount = productsResult.value?.count || 0;
    const categoryCount = categoriesResult.value?.count || 0;
    
    // Vérifier s'il y a des erreurs
    const productError = productsResult.status === 'rejected' ? productsResult.reason : null;
    const categoryError = categoriesResult.status === 'rejected' ? categoriesResult.reason : null;
    
    // Créer la réponse
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        status: 'success',
        message: 'Vérification de la connexion Supabase',
        database: {
          connected: !productError && !categoryError,
          products: {
            count: productCount,
            error: productError ? productError.message : null
          },
          categories: {
            count: categoryCount,
            error: categoryError ? categoryError.message : null
          }
        },
        environmentInfo: envInfo,
        timestamp: new Date().toISOString()
      })
    };
    
  } catch (error) {
    console.error('Erreur lors du test de connexion:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Erreur de connexion Supabase',
        message: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
