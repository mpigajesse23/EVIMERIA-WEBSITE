#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à Supabase
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire backend au path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaelleshop.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_supabase_connection():
    """Teste la connexion à la base de données Supabase"""
    print("🔗 Test de connexion à Supabase...")
    
    try:
        # Test de connexion basique
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connexion réussie à PostgreSQL")
            print(f"📊 Version: {version[0]}")
            
            # Test des tables Django
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name LIKE 'django_%'
                LIMIT 5;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"🗃️  Tables Django trouvées: {len(tables)}")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("⚠️  Aucune table Django trouvée - migrations nécessaires")
                
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def run_migrations():
    """Exécute les migrations Django"""
    print("\n🔧 Application des migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations appliquées avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de déploiement EVIMERIA avec Supabase")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Variable DATABASE_URL non définie")
        print("💡 Exécutez: export DATABASE_URL='postgresql://postgres.jbxy...'")
        sys.exit(1)
    
    print(f"🔧 Base de données: {database_url[:50]}...")
    
    # Test de connexion
    if test_supabase_connection():
        print("\n🎉 Connexion Supabase réussie !")
        
        # Proposer d'appliquer les migrations
        response = input("\n🤔 Voulez-vous appliquer les migrations ? (y/N): ")
        if response.lower() in ['y', 'yes', 'oui']:
            run_migrations()
    else:
        print("\n💥 Échec de la connexion à Supabase")
        print("🔍 Vérifiez votre DATABASE_URL et votre connexion internet")
        sys.exit(1)
