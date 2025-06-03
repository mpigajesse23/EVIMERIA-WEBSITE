# Script PowerShell pour déployer les fonctions Netlify
Write-Host "🚀 Déploiement des fonctions Netlify pour EVIMERIA..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Créer un répertoire temporaire pour les fonctions
$tempDir = "temp_functions"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Copier les fonctions dans le répertoire temporaire
Write-Host "📦 Copie des fonctions depuis netlify/functions..." -ForegroundColor Yellow
Copy-Item -Path "netlify/functions/*" -Destination $tempDir -Recurse

# Copier les dépendances nécessaires
Write-Host "📦 Copie des dépendances..." -ForegroundColor Yellow
Copy-Item -Path "package.json" -Destination $tempDir
Set-Location $tempDir
npm install --production

# Déployer les fonctions
Write-Host "🚀 Déploiement des fonctions..." -ForegroundColor Green
netlify functions:deploy

# Retourner au répertoire d'origine et nettoyer
Set-Location ..
Write-Host "🧹 Nettoyage..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $tempDir

Write-Host "`n✅ Déploiement des fonctions terminé!" -ForegroundColor Green
Write-Host "Pour tester les fonctions, visitez:"
Write-Host "- API: https://evimeria.netlify.app/.netlify/functions/api"
Write-Host "- Test DB: https://evimeria.netlify.app/.netlify/functions/db_test"
