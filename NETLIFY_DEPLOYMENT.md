# Guide de Déploiement EVIMERIA sur Netlify

## Architecture Choisie
✅ **Netlify Functions + Supabase** (Architecture serverless complète)

## Prérequis

1. **Compte Netlify** (gratuit)
2. **Base de données Supabase** configurée
3. **Dépôt GitHub** avec le code source

## Configuration des Variables d'Environnement

Dans le panneau Netlify, configurez les variables suivantes :

### Variables Supabase
```
SUPABASE_URL=https://jbxyihenvutqwkknlelh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpienlpaGVudnV0cXdra25sZWxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI1NzQwOTAsImV4cCI6MjA0ODE1MDA5MH0.yU-VJNnfJAQ2MhzYOJZrmAJdpj5gOBnRkE9t_XJd_6s
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
```

### Variables Frontend
```
VITE_API_URL=/.netlify/functions
VITE_CLOUDINARY_CLOUD_NAME=dmcaguchx
```

## Étapes de Déploiement

### 1. Préparation du Projet

```bash
# Installer les dépendances serverless
npm install

# Installer les dépendances frontend
cd frontend
npm install
cd ..
```

### 2. Configuration Netlify

1. **Connecter le dépôt GitHub** à Netlify
2. **Build settings** :
   - Build command: `cd frontend && npm ci --legacy-peer-deps && npm run build`
   - Publish directory: `frontend/dist`
   - Functions directory: `netlify/functions`

### 3. Déploiement

Le déploiement se fait automatiquement à chaque push sur la branche `main`.

## Structure des Endpoints API

### API Base
- `GET /.netlify/functions/api` - Informations sur l'API

### Produits
- `GET /.netlify/functions/api/products` - Liste des produits
- `GET /.netlify/functions/api/products/{id}` - Détail d'un produit

### Catégories
- `GET /.netlify/functions/api/categories` - Liste des catégories

### Santé
- `GET /.netlify/functions/api/health` - Status de l'API

## Avantages de cette Architecture

### ✅ Avantages
- **Gratuit** : Netlify offre 125k appels de fonctions par mois gratuitement
- **Scalabilité automatique** : Les fonctions s'adaptent à la charge
- **Pas de serveur à gérer** : Architecture entièrement serverless
- **Déploiement continu** : Automatique depuis GitHub
- **CDN global** : Livraison rapide du frontend
- **HTTPS automatique** : Certificat SSL gratuit

### 🔧 Limitations
- **Cold start** : Légère latence sur les premières requêtes
- **Timeout** : 10 secondes maximum par fonction
- **Taille** : 50MB maximum par fonction

## URLs après déploiement

- **Frontend** : `https://votre-site.netlify.app`
- **API** : `https://votre-site.netlify.app/.netlify/functions/api`

## Monitoring et Debug

1. **Netlify Dashboard** : Logs en temps réel
2. **Supabase Dashboard** : Monitoring de la base de données
3. **Analytics** : Statistiques Netlify intégrées

## Tests Locaux

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Démarrer en local
netlify dev

# Tester les fonctions
netlify functions:serve
```

## Maintenance

### Mise à jour des dépendances
```bash
npm update
cd frontend && npm update
```

### Sauvegarde Supabase
- Automatique dans le plan gratuit Supabase
- Export SQL disponible dans le dashboard

## Support

- **Documentation Netlify** : https://docs.netlify.com/
- **Documentation Supabase** : https://supabase.com/docs
- **Support** : Communautés Discord respectives
