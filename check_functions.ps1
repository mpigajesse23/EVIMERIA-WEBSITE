#!/usr/bin/env pwsh
# Script pour vérifier la configuration des fonctions Netlify

Write-Host "🔍 Vérification de la configuration des fonctions Netlify..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Vérifier le fichier netlify.toml
Write-Host "`n📄 Vérification du fichier netlify.toml..." -ForegroundColor Yellow
$netlifyToml = Get-Content -Path "netlify.toml" -Raw

# Vérifier les chemins des fonctions
$functionsPath = $null
if ($netlifyToml -match 'functions\s*=\s*"([^"]+)"') {
    $functionsPath = $matches[1]
    Write-Host "✅ Chemin des fonctions défini: $functionsPath" -ForegroundColor Green
} else {
    Write-Host "❌ Chemin des fonctions non défini dans netlify.toml" -ForegroundColor Red
}

# Vérifier le répertoire des fonctions
if ($functionsPath -and (Test-Path $functionsPath)) {
    Write-Host "✅ Le répertoire des fonctions existe: $functionsPath" -ForegroundColor Green
    
    # Vérifier les fichiers de fonctions
    $functionFiles = Get-ChildItem -Path $functionsPath -Filter "*.js"
    Write-Host "🔍 Fonctions trouvées: $($functionFiles.Count)" -ForegroundColor Yellow
    
    foreach ($file in $functionFiles) {
        Write-Host "  - $($file.Name)"
    }
    
    # Vérifier package.json des fonctions
    $packageJsonPath = Join-Path -Path $functionsPath -ChildPath "package.json"
    if (Test-Path $packageJsonPath) {
        Write-Host "✅ package.json trouvé dans le répertoire des fonctions" -ForegroundColor Green
        
        # Vérifier les dépendances
        $packageJson = Get-Content -Path $packageJsonPath | ConvertFrom-Json
        $supabaseDep = $packageJson.dependencies.'@supabase/supabase-js'
        if ($supabaseDep) {
            Write-Host "✅ Dépendance Supabase trouvée: $supabaseDep" -ForegroundColor Green
        } else {
            Write-Host "❌ Dépendance Supabase non trouvée dans package.json" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️ Pas de package.json dans le répertoire des fonctions" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Le répertoire des fonctions n'existe pas: $functionsPath" -ForegroundColor Red
}

# Vérifier les redirections
if ($netlifyToml -match 'from\s*=\s*"/api/\*".*to\s*=\s*"/\.netlify/functions/api') {
    Write-Host "✅ Redirection d'API correctement configurée" -ForegroundColor Green
} else {
    Write-Host "❌ Redirection d'API incorrecte ou manquante" -ForegroundColor Red
}

# Vérifier les variables d'environnement
if ($netlifyToml -match 'VITE_API_URL\s*=\s*"/\.netlify/functions"') {
    Write-Host "✅ Variable d'environnement VITE_API_URL correctement configurée" -ForegroundColor Green
} else {
    Write-Host "❌ Variable d'environnement VITE_API_URL incorrecte ou manquante" -ForegroundColor Red
}

Write-Host "`n📋 Étapes suivantes:" -ForegroundColor Cyan
Write-Host "1. Déployez avec: netlify deploy --prod"
Write-Host "2. Vérifiez les journaux de fonctions dans le tableau de bord Netlify"
Write-Host "3. Testez l'API à: https://evimeria.netlify.app/.netlify/functions/api"
