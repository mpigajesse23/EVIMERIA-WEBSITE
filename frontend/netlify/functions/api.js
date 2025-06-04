// Fonction Netlify principale pour l'API EVIMERIA
// Architecture serverless avec Supabase

const { createClient } = require('@supabase/supabase-js');

// Configuration Supabase
const supabaseUrl = process.env.SUPABASE_URL;
// Utiliser la clé de service pour les fonctions Netlify
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

console.log('Variables d\'environnement lues:');
console.log('SUPABASE_URL:', supabaseUrl ? 'Présente' : 'Manquante');
console.log('SUPABASE_SERVICE_ROLE_KEY:', supabaseKey ? 'Présente et a une longueur de' : 'Manquante', supabaseKey ? supabaseKey.length : '');

if (!supabaseUrl || !supabaseKey) {
  console.error('Variables d\'environnement manquantes:', {
    SUPABASE_URL: !!supabaseUrl,
    SUPABASE_SERVICE_ROLE_KEY: !!supabaseKey
  });
  throw new Error('Variables d\'environnement Supabase manquantes');
}

console.log('Initialisation du client Supabase avec:', {
  url: supabaseUrl,
  keyLength: supabaseKey.length,
  keyType: 'SERVICE_ROLE'
});

const supabase = createClient(supabaseUrl, supabaseKey);

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
    const path = event.path.replace('/.netlify/functions/api', '');
    const method = event.httpMethod;
    
    console.log(`API Call: ${method} ${path}`);

    // Route de base pour tester l'API
    if (path === '' || path === '/') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          message: '🚀 API EVIMERIA avec Netlify Functions + Supabase',
          version: '1.0.0',
          timestamp: new Date().toISOString(),
          endpoints: [
            '/api/products',
            '/api/categories',
            '/api/health'
          ]
        })
      };
    }

    // Route de santé
    if (path === '/health') {
      const { data: healthCheck, error: healthError } = await supabase
        .from('products_category')
        .select('count')
        .limit(1);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: 'healthy',
          database: healthError ? 'disconnected' : 'connected',
          error: healthError ? healthError.message : null,
          timestamp: new Date().toISOString()
        })
      };
    }

    // Route pour les produits
    if (path.startsWith('/products')) {
      if (method === 'GET') {
        console.log('Récupération des produits...');
        // Récupérer tous les produits depuis Supabase
        const { data, error } = await supabase
          .from('products_product')
          .select('*, category:products_category(name)')
          .eq('is_published', true);

        if (error) {
          console.error('Erreur Supabase lors de la récupération des produits:', error);
          return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
              error: 'Erreur base de données',
              details: error.message,
              code: error.code
            })
          };
        }

        console.log(`${data ? data.length : 0} produits trouvés`);
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            count: data.length,
            results: data
          })
        };
      }
    }

    // Route pour les catégories
    if (path.startsWith('/categories')) {
      if (method === 'GET') {
        console.log('Récupération des catégories...');
        const { data, error } = await supabase
          .from('products_category')
          .select('*')
          .eq('is_published', true);

        if (error) {
          console.error('Erreur Supabase lors de la récupération des catégories:', error);
          return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
              error: 'Erreur base de données',
              details: error.message,
              code: error.code
            })
          };
        }

        console.log(`${data ? data.length : 0} catégories trouvées`);
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            count: data.length,
            results: data
          })
        };
      }
    }

    // Route non trouvée
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({
        error: 'Route non trouvée',
        path: path,
        method: method
      })
    };

  } catch (error) {
    console.error('Erreur API:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Erreur serveur interne',
        message: error.message,
        stack: error.stack
      })
    };
  }
};
