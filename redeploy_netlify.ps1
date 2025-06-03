# Script PowerShell pour redéployer le site Netlify
Write-Host "🚀 Déclenchement d'un redéploiement Netlify pour EVIMERIA..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Vérifier si netlify CLI est installé
try {
    $netlifyVersion = netlify --version
    Write-Host "✅ Netlify CLI détecté : $netlifyVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Netlify CLI n'est pas installé." -ForegroundColor Red
    Write-Host "Installation en cours..." -ForegroundColor Yellow
    npm install -g netlify-cli
}

# Déclencher un redéploiement
Write-Host "`n🔄 Déclenchement du redéploiement..." -ForegroundColor Yellow
netlify deploy --prod

Write-Host "`n📝 Notes importantes:" -ForegroundColor Cyan
Write-Host "1. Si le déploiement échoue, vérifiez les journaux dans le dashboard Netlify"
Write-Host "2. Assurez-vous que toutes les variables d'environnement sont configurées dans Netlify"
Write-Host "3. La mise à jour peut prendre quelques minutes pour se propager"

Write-Host "`n🌐 Une fois le déploiement terminé, vérifiez:" -ForegroundColor Green
Write-Host "- Site web: https://evimeria.netlify.app"
Write-Host "- API: https://evimeria.netlify.app/.netlify/functions/api"
Write-Host "- Test DB: https://evimeria.netlify.app/.netlify/functions/db_test"
