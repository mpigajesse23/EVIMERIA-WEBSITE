import os
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion de l'environnement
database_url = os.environ.get('DATABASE_URL', '')

if not database_url:
    print("❌ Aucune URL de base de données trouvée dans les variables d'environnement.")
    exit(1)

print(f"🔧 Connexion à la base de données: {database_url[:20]}...")

try:
    # Se connecter à la base de données
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Tester une requête simple
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"✅ Connexion réussie! Test: {result[0]}")
    
    # Vérifier si les tables existent
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    """)
    
    tables = cursor.fetchall()
    print(f"\n📊 Tables trouvées ({len(tables)}):")
    for i, (table_name,) in enumerate(tables, 1):
        print(f"  {i}. {table_name}")
    
    # Fermer la connexion
    cursor.close()
    conn.close()
    print("\n✅ Test terminé avec succès!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    
print("\nPour ajouter des données à la base, créez une nouvelle requête INSERT appropriée.")
