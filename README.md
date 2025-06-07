# EVIMERIA (anciennement JaelleShop)

Boutique e-commerce moderne avec architecture serverless : **Netlify Functions + Supabase + React**.

## 🚀 Architecture Serverless

- **Frontend** : React + Vite (hébergé sur Netlify)
- **Backend** : Netlify Functions (serverless)
- **Base de données** : Supabase PostgreSQL
- **Stockage médias** : Cloudinary
- **Déploiement** : Netlify (automatique depuis GitHub)

## ⚡ Déploiement Rapide

### Option 1: Déploiement sur Netlify (Recommandé)

1. **Fork ce dépôt** sur GitHub
2. **Connectez-le à Netlify** (connexion automatique)
3. **Configurez les variables d'environnement** dans Netlify
4. **Déployez automatiquement** 🎉

📖 **Guide détaillé** : [NETLIFY_DEPLOYMENT.md](./NETLIFY_DEPLOYMENT.md)

### Option 2: Développement Local

```bash
# Installer les dépendances
npm install
cd frontend && npm install && cd ..

# Démarrer le développement local
npm run dev
# ou
netlify dev
```

## 🗂️ Structure du Projet

```
evimeria/
├── frontend/              # Application React + Vite
├── netlify/functions/     # API Serverless (remplace Django)
├── backend/              # Code Django (pour référence/migration)
├── netlify.toml          # Configuration Netlify
├── package.json          # Dépendances serverless
└── NETLIFY_DEPLOYMENT.md # Guide de déploiement
## 📊 Configuration

### Variables d'Environnement Netlify

```bash
# Supabase
SUPABASE_URL=https://jbxyihenvutqwkknlelh.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Frontend
VITE_API_URL=/.netlify/functions
VITE_CLOUDINARY_CLOUD_NAME=dmcaguchx
```

### Base de Données Configurée

✅ **Supabase PostgreSQL** déjà configuré et fonctionnel
- URL: `postgresql://postgres.jbxyihenvutqwkknlelh:MPIGAjes$e2025@@aws-0-eu-west-3.pooler.supabase.com:6543/postgres`
- Admin créé: `mpigajesse23@gmail.com`
- Toutes les migrations appliquées

## 🔧 Développement Local (Optionnel)

Si vous voulez développer localement avec Docker :

```bash
# Créer un fichier .env à partir de .env.example
cp .env.example .env

# Démarrer l'application en mode développement
docker-compose up

# Exécuter des commandes dans le conteneur backend
docker-compose exec backend python manage.py createsuperuser
```
   - PGUSER

## Déploiement sur Render (Gratuit - Sans carte bancaire)

### 1. Préparation

1. Assurez-vous que votre code est sur GitHub
2. Créez un compte gratuit sur [Render.com](https://render.com)
3. Obtenez vos identifiants Cloudinary

### 2. Déploiement du Backend (Django)

1. Sur Render, cliquez sur "New +" → "Web Service"
2. Connectez votre repository GitHub
3. Configurez le service :
   - **Name**: `evimeria-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`
   - **Instance Type**: `Free`

4. Ajoutez les variables d'environnement :
   ```
   SECRET_KEY=généré-automatiquement-par-render
   DEBUG=False
   ALLOWED_HOSTS=evimeria-backend.onrender.com
   CLOUDINARY_CLOUD_NAME=votre-cloud-name
   CLOUDINARY_API_KEY=votre-api-key
   CLOUDINARY_API_SECRET=votre-api-secret
   ```

### 3. Déploiement de la Base de Données

1. Sur Render, cliquez sur "New +" → "PostgreSQL"
2. Configurez :
   - **Name**: `evimeria-db`
   - **Database Name**: `evimeria`
   - **User**: `evimeria_user`
   - **Plan**: `Free`

3. Une fois créée, copiez la `DATABASE_URL` et ajoutez-la aux variables d'environnement du backend

### 4. Déploiement du Frontend (React)

1. Sur Render, cliquez sur "New +" → "Static Site"
2. Connectez votre repository GitHub
3. Configurez :
   - **Name**: `evimeria-frontend`
   - **Build Command**: `cd frontend && npm ci --legacy-peer-deps && npm run build`
   - **Publish Directory**: `frontend/dist`

4. Ajoutez la variable d'environnement :
   ```
   VITE_API_URL=https://evimeria-backend.onrender.com
   ```

### 5. Configuration finale

Une fois les services déployés :
1. Mettez à jour `ALLOWED_HOSTS` dans le backend avec l'URL de votre frontend
2. Configurez CORS dans Django pour autoriser votre frontend
3. Testez votre application

### 6. URLs de votre application

- **Frontend**: `https://evimeria-frontend.onrender.com`
- **Backend API**: `https://evimeria-backend.onrender.com`
- **Admin Django**: `https://evimeria-backend.onrender.com/admin`

### Limitations du plan gratuit Render

- Les services "s'endorment" après 15 minutes d'inactivité
- Premier chargement peut être lent (cold start)
- 750h d'utilisation par mois
- Base de données PostgreSQL limitée à 1GB

## Alternatives d'hébergement gratuit

### Vercel + PlanetScale
- **Vercel** pour le frontend React
- **PlanetScale** pour la base de données MySQL (gratuit)
- **Vercel Functions** pour quelques endpoints backend

### Netlify + Supabase
- **Netlify** pour le frontend
- **Supabase** pour la base de données PostgreSQL + API backend

## Déploiement avec Netlify + Supabase (Recommandé - 100% Gratuit)

Cette solution combine **Netlify** pour le frontend et **Render** pour le backend Django, avec **Supabase** comme base de données PostgreSQL.

### 1. Configuration de la base de données Supabase

Votre base de données Supabase est déjà configurée :
- **Hôte** : db.jbxyihenvutqwkknlelh.supabase.co
- **Port** : 5432
- **Base de données** : postgres
- **URL de connexion** : `postgresql://postgres.jbxyihenvutqwkknlelh:MPIGAjes%24e2025%40%40@aws-0-eu-west-3.pooler.supabase.com:6543/postgres`

### 2. Déploiement du Backend sur Render

1. **Créer un compte Render gratuit** : [render.com](https://render.com)

2. **Déployer le backend** :
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre repository GitHub
   - Configurez le service :
     - **Name** : `evimeria-backend`
     - **Environment** : `Python 3`
     - **Build Command** : `./build.sh`
     - **Start Command** : `./start.sh`
     - **Instance Type** : `Free`

3. **Variables d'environnement Render** :
   ```
   SECRET_KEY=your-django-secret-key
   DEBUG=False
   ALLOWED_HOSTS=evimeria-backend.onrender.com,evimeria-frontend.netlify.app
   DATABASE_URL=postgresql://postgres.jbxyihenvutqwkknlelh:MPIGAjes%24e2025%40%40@aws-0-eu-west-3.pooler.supabase.com:6543/postgres
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   CORS_ALLOWED_ORIGINS=https://evimeria-frontend.netlify.app
   ```

### 3. Déploiement du Frontend sur Netlify

1. **Créer un compte Netlify gratuit** : [netlify.com](https://netlify.com)

2. **Déployer le frontend** :
   - Connectez votre repository GitHub
   - Netlify détectera automatiquement la configuration `netlify.toml`
   - Le build se lancera automatiquement

3. **Variables d'environnement Netlify** :
   ```
   VITE_API_URL=https://evimeria-backend.onrender.com
   ```

### 4. Configuration finale

Une fois les deux services déployés :

1. **Mettre à jour les URLs** :
   - Notez l'URL de votre backend Render (ex: `evimeria-backend.onrender.com`)
   - Notez l'URL de votre frontend Netlify (ex: `evimeria-frontend.netlify.app`)

2. **Mettre à jour les variables d'environnement** :
   - Sur Render : Ajoutez l'URL Netlify dans `ALLOWED_HOSTS` et `CORS_ALLOWED_ORIGINS`
   - Sur Netlify : Vérifiez que `VITE_API_URL` pointe vers votre backend Render

3. **Tester l'application** :
   - Frontend : `https://votre-app.netlify.app`
   - Backend API : `https://votre-backend.onrender.com/api/`
   - Admin Django : `https://votre-backend.onrender.com/admin/`

### 5. Avantages de cette solution

✅ **100% Gratuit** - Aucune carte bancaire requise
✅ **Déploiement automatique** - Push sur GitHub = déploiement automatique
✅ **SSL inclus** - HTTPS par défaut
✅ **Scalable** - Peut gérer un trafic modéré
✅ **Base de données robuste** - PostgreSQL via Supabase

### 6. Limitations

- **Render** : Cold start après 15min d'inactivité
- **Netlify** : 100GB de bande passante/mois
- **Supabase** : 500MB de stockage, 2 projets max

### 7. Commandes de test en local avec Supabase

```bash
# Tester la connexion Supabase en local
cd backend
export DATABASE_URL="postgresql://postgres.jbxyihenvutqwkknlelh:MPIGAjes%24e2025%40%40@aws-0-eu-west-3.pooler.supabase.com:6543/postgres"
python manage.py migrate
python manage.py runserver
```