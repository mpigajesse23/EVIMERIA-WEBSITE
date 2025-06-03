#!/usr/bin/env bash

echo "🔍 Vérification des fichiers nécessaires pour le déploiement sur Render..."

# Vérification des fichiers obligatoires
required_files=(
    "build.sh"
    "start.sh" 
    ".env.render"
    "backend/requirements.txt"
    "backend/manage.py"
    "frontend/package.json"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ Tous les fichiers nécessaires sont présents"
    
    # Rendre les scripts exécutables
    chmod +x build.sh
    chmod +x start.sh
    
    echo "✅ Scripts rendus exécutables"
    echo ""
    echo "🚀 Votre projet est prêt pour le déploiement sur Render !"
    echo ""
    echo "Prochaines étapes :"
    echo "1. Commitez et pushez votre code sur GitHub"
    echo "2. Créez un compte sur render.com"
    echo "3. Suivez les instructions dans le README.md"
    
else
    echo "❌ Fichiers manquants :"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Veuillez créer ces fichiers avant de continuer."
    exit 1
fi
