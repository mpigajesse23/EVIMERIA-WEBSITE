# Script de vérification finale avant déploiement
Write-Host "🔍 Vérification finale EVIMERIA - Netlify + Render + Supabase" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

$DATABASE_URL = "postgresql://postgres.jbxyihenvutqwkknlelh:MPIGAjes%24e2025%40%40@aws-0-eu-west-3.pooler.supabase.com:6543/postgres"

# Vérification des fichiers nécessaires
$files = @(
    "backend\build.sh",
    "backend\start.sh", 
    "backend\requirements.txt",
    "backend\manage.py",
    "netlify.toml",
    "render.yaml",
    "test_supabase.py"
)

Write-Host "`n📁 Vérification des fichiers..." -ForegroundColor Yellow
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file MANQUANT" -ForegroundColor Red
    }
}

# Test de connexion Supabase
Write-Host "`n🔗 Test de connexion Supabase..." -ForegroundColor Yellow
$env:DATABASE_URL = $DATABASE_URL
python test_supabase.py

# Vérification frontend
Write-Host "`n🎨 Vérification frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\package.json") {
    Set-Location frontend
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    if ($packageJson.scripts.build) {
        Write-Host "✅ Script build configuré" -ForegroundColor Green
    } else {
        Write-Host "❌ Script build manquant" -ForegroundColor Red
    }
    Set-Location ..
} else {
    Write-Host "❌ Frontend non configuré" -ForegroundColor Red
}

Write-Host "`n📋 Checklist finale:" -ForegroundColor Cyan
Write-Host "[ ] Code pushé sur GitHub" -ForegroundColor White
Write-Host "[ ] Compte Render créé (render.com)" -ForegroundColor White
Write-Host "[ ] Compte Netlify créé (netlify.com)" -ForegroundColor White
Write-Host "[ ] Identifiants Cloudinary prêts" -ForegroundColor White

Write-Host "`n🚀 Prêt pour le déploiement!" -ForegroundColor Green
Write-Host "📖 Suivez maintenant le DEPLOYMENT_GUIDE.md" -ForegroundColor Yellow
