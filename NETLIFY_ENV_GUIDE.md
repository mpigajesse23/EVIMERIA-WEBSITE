# Guide d'ajout des variables d'environnement à Netlify

## Option 1 : Via l'interface web de Netlify (Recommandé)

1. **Générer le fichier d'environnement**
   
   Exécutez d'abord le script de préparation :
   ```bash
   node prepare_netlify_env.js
   ```

2. **Accéder aux paramètres de votre site Netlify**
   - Connectez-vous à votre compte Netlify
   - Sélectionnez votre site EVIMERIA
   - Cliquez sur "Site settings" dans le menu

3. **Accéder à la section des variables d'environnement**
   - Dans le menu de gauche, cliquez sur "Environment variables"
   - Vous devriez voir une page similaire à celle de la capture d'écran que vous avez partagée

4. **Importez les variables**
   - Cliquez sur "Import from .env" ou un bouton équivalent
   - Sélectionnez le fichier `netlify-env.json` qui a été généré
   - Vérifiez que toutes les variables sont correctement importées

## Option 2 : Via la ligne de commande Netlify CLI

Si vous préférez utiliser la ligne de commande :

1. **Assurez-vous que Netlify CLI est installé et connecté à votre compte**
   ```bash
   netlify login
   ```

2. **Utilisez les commandes générées**
   Le script de préparation a créé un fichier avec toutes les commandes nécessaires :
   ```bash
   # Visualiser les commandes
   cat netlify-env-commands.txt
   
   # Exécuter les commandes (sous Windows avec PowerShell)
   Get-Content netlify-env-commands.txt | ForEach-Object { Invoke-Expression $_ }
   ```

3. **Ou importez directement depuis le fichier .env**
   ```bash
   netlify env:import .env
   ```

## Vérification

Après avoir importé les variables :

1. **Rafraîchissez la page des variables d'environnement** sur Netlify
2. **Vérifiez que toutes les variables nécessaires sont présentes** :
   - SUPABASE_URL
   - SUPABASE_ANON_KEY
   - SUPABASE_SERVICE_ROLE_KEY
   - VITE_API_URL
   - VITE_SUPABASE_URL
   - VITE_SUPABASE_ANON_KEY

3. **Déclenchez un nouveau déploiement** pour appliquer ces variables
   - Allez dans "Deploys" 
   - Cliquez sur "Trigger deploy" > "Deploy site"

## Variables essentielles

Assurez-vous que ces variables sont correctement configurées :

- `SUPABASE_URL` : URL de votre base de données Supabase
- `SUPABASE_ANON_KEY` : Clé anonyme pour l'accès public
- `VITE_API_URL` : Doit être définie à `/.netlify/functions` pour le frontend
