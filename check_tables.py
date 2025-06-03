import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion de l'environnement
database_url = os.environ.get('DATABASE_URL', '')

if not database_url:
    print("❌ Aucune URL de base de données trouvée dans les variables d'environnement.")
    exit(1)

print(f"🔧 Utilisation de la connexion: {database_url[:20]}...")

try:
    # Analyser l'URL de connexion
    url = urlparse(database_url)
    
    # Se connecter à la base de données
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Exécuter la requête pour lister toutes les tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print(f"📋 Tables disponibles dans la base de données ({len(tables)}):")
    for i, table in enumerate(tables, 1):
        print(f"  {i}. {table[0]}")
    
    # Vérifier les tables spécifiques pour les produits et catégories
    product_tables = [t for t, in tables if 'product' in t]
    category_tables = [t for t, in tables if 'category' in t]
    
    if product_tables:
        print(f"\n✅ Tables de produits trouvées: {', '.join(product_tables)}")
        
        # Compter les produits
        for table in product_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table}: {count} enregistrements")
    else:
        print("\n❌ Aucune table de produits trouvée!")
    
    if category_tables:
        print(f"\n✅ Tables de catégories trouvées: {', '.join(category_tables)}")
        
        # Compter les catégories
        for table in category_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table}: {count} enregistrements")
    else:
        print("\n❌ Aucune table de catégories trouvée!")
    
    # Fermer la connexion
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des tables: {e}")
