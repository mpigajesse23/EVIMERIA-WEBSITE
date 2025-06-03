#!/usr/bin/env pwsh
# Validation script for Netlify deployment readiness

Write-Host "🔍 Validating EVIMERIA Netlify deployment readiness..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if netlify.toml exists
if (Test-Path -Path "netlify.toml") {
    Write-Host "✅ netlify.toml found" -ForegroundColor Green
} else {
    Write-Host "❌ netlify.toml not found!" -ForegroundColor Red
    exit 1
}

# Check if netlify/functions/api.js exists
if (Test-Path -Path "netlify/functions/api.js") {
    Write-Host "✅ netlify/functions/api.js found" -ForegroundColor Green
} else {
    Write-Host "❌ netlify/functions/api.js not found!" -ForegroundColor Red
    exit 1
}

# Check if .env exists
if (Test-Path -Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
    
    # Check for required environment variables in .env
    $envContent = Get-Content -Path ".env" -Raw
    $required_vars = @(
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "VITE_API_URL"
    )
    
    foreach ($var in $required_vars) {
        if ($envContent -match "$var=") {
            Write-Host "  ✅ $var is configured" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $var is missing in .env" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
}

# Check frontend directory structure
if (Test-Path -Path "frontend/package.json") {
    Write-Host "✅ frontend/package.json found" -ForegroundColor Green
} else {
    Write-Host "❌ frontend/package.json not found!" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists in frontend
if (Test-Path -Path "frontend/node_modules") {
    Write-Host "✅ frontend/node_modules found" -ForegroundColor Green
} else {
    Write-Host "⚠️ frontend/node_modules not found, will be installed during build" -ForegroundColor Yellow
}

# Check if Supabase JavaScript client is installed
if (Test-Path -Path "node_modules/@supabase") {
    Write-Host "✅ Supabase client installed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Supabase client not installed locally, will be installed during build" -ForegroundColor Yellow
}

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "✅ Validation completed" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Push changes to GitHub repository"
Write-Host "2. Connect repository to Netlify"
Write-Host "3. Set environment variables on Netlify:"
Write-Host "   - SUPABASE_URL=https://jbxyihenvutqwkknlelh.supabase.co" 
Write-Host "   - SUPABASE_ANON_KEY=[Supabase anon key]"
Write-Host "   - VITE_API_URL=/.netlify/functions"
Write-Host ""
Write-Host "💻 Run this command locally to test:" -ForegroundColor Cyan
Write-Host "npm install -g netlify-cli && netlify dev" -ForegroundColor Yellow
