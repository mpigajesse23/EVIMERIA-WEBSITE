// Fonction Netlify principale pour l'API EVIMERIA
// Architecture serverless avec Supabase

const { createClient } = require('@supabase/supabase-js');

// Configuration Supabase
const supabaseUrl = process.env.SUPABASE_URL || 'https://jbxyihenvutqwkknlelh.supabase.co';
const supabaseKey = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpieHlpaGVudnV0cXdra25sZWxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5MzcwNDgsImV4cCI6MjA2NDUxMzA0OH0.KfohW3qnKM-2MH2i4c5xaIbvwLHePVadplCNMiy4U5E';
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
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: 'healthy',
          database: 'connected',
          timestamp: new Date().toISOString()
        })
      };
    }

    // Route pour les produits
    if (path.startsWith('/products')) {
      if (method === 'GET') {
        // Récupérer tous les produits depuis Supabase
        const { data, error } = await supabase
          .from('products_product')
          .select('*')
          .eq('is_published', true);

        if (error) {
          console.error('Erreur Supabase:', error);
          return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Erreur base de données' })
          };
        }

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
        const { data, error } = await supabase
          .from('products_category')
          .select('*')
          .eq('is_published', true);

        if (error) {
          console.error('Erreur Supabase:', error);
          return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Erreur base de données' })
          };
        }

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
        message: error.message
      })
    };
  }
};
