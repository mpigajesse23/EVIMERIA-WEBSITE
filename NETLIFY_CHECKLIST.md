# Liste de contrôle pour le déploiement EVIMERIA sur Netlify

## 1. Importation des variables d'environnement

- [ ] Naviguer vers la page de configuration de votre site Netlify
- [ ] Aller à "Site settings" > "Environment variables"
- [ ] Cliquer sur "Add a variable" ou "Import"
- [ ] Importer le fichier `netlify-env.json` généré
- [ ] Vérifier que toutes les variables suivantes sont présentes :
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_ANON_KEY
  - [ ] SUPABASE_SERVICE_ROLE_KEY
  - [ ] VITE_API_URL
  - [ ] VITE_SUPABASE_URL
  - [ ] VITE_SUPABASE_ANON_KEY

## 2. Déploiement et vérification

- [ ] Déclencher un nouveau déploiement via "Deploys" > "Trigger deploy"
- [ ] Une fois le déploiement terminé, vérifier le site : https://evimeria.netlify.app/
- [ ] Vérifier que les produits apparaissent correctement
- [ ] Vérifier les journaux de déploiement pour tout message d'erreur

## 3. Dépannage si les produits n'apparaissent pas

- [ ] Vérifier que les tables Supabase contiennent des données
  ```
  node test_db.py
  ```
- [ ] S'assurer que la fonction API peut accéder à Supabase
  ```
  netlify functions:invoke api
  ```
- [ ] Vérifier les journaux de fonctions Netlify dans le dashboard
- [ ] Vérifier la console du navigateur pour tout message d'erreur

## 4. Vérification finale

- [ ] Site accessible : https://evimeria.netlify.app/
- [ ] API accessible : https://evimeria.netlify.app/.netlify/functions/api
- [ ] Produits visibles sur la page d'accueil
- [ ] Navigation fonctionnelle entre les pages
- [ ] Images des produits correctement chargées

## Notes importantes

- Les variables d'environnement sont sensibles et ne doivent pas être partagées
- Le fichier `netlify-env.json` contient des clés API - ne pas le pousser sur GitHub
- Après avoir terminé l'importation, supprimez ces fichiers de votre système :
  ```
  rm netlify-env.json netlify-env-commands.txt
  ```
