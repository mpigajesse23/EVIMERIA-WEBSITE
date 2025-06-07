#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaelleshop.settings')
django.setup()

from products.models import Category, SubCategory, Product, ProductImage
import random

print("=== Mise à jour des images avec Unsplash ===")

# Mapping des mots-clés Unsplash pour chaque type de produit
unsplash_keywords = {
    # Vêtements
    'T-shirt': ['tshirt', 'casual-wear', 'cotton-shirt'],
    'Chemise': ['dress-shirt', 'formal-shirt', 'business-shirt'],
    'Pantalon': ['trousers', 'pants', 'formal-pants'],
    'Veste': ['jacket', 'blazer', 'outerwear'],
    'Pull': ['sweater', 'pullover', 'knitwear'],
    'Sweat': ['hoodie', 'sweatshirt', 'casual-wear'],
    'Jean': ['jeans', 'denim', 'casual-pants'],
    'Polo': ['polo-shirt', 'casual-shirt', 'sport-shirt'],
    'Robe': ['dress', 'woman-dress', 'elegant-dress'],
    'Jupe': ['skirt', 'woman-skirt', 'fashion'],
    'Legging': ['leggings', 'sport-wear', 'activewear'],
    'Blouse': ['blouse', 'woman-shirt', 'elegant-top'],
    'Short': ['shorts', 'summer-wear', 'casual-shorts'],
    'Pyjama': ['pajamas', 'sleepwear', 'nightwear'],
    'Bermuda': ['bermuda-shorts', 'summer-shorts', 'casual-wear'],
    
    # Chaussures
    'Sneakers': ['sneakers', 'sport-shoes', 'casual-shoes'],
    'Bottes': ['boots', 'leather-boots', 'winter-boots'],
    'Mocassins': ['loafers', 'dress-shoes', 'leather-shoes'],
    'Sandales': ['sandals', 'summer-shoes', 'beach-shoes'],
    'Baskets': ['basketball-shoes', 'sport-sneakers', 'athletic-shoes'],
    'Escarpins': ['high-heels', 'pumps', 'formal-shoes'],
    'Derbies': ['oxford-shoes', 'dress-shoes', 'formal-footwear'],
    
    # Accessoires
    'Ceinture': ['leather-belt', 'belt', 'fashion-accessory'],
    'Écharpe': ['scarf', 'winter-scarf', 'fashion-scarf'],
    'Gants': ['gloves', 'winter-gloves', 'leather-gloves'],
    'Bracelet': ['bracelet', 'jewelry', 'wrist-accessory'],
    'Collier': ['necklace', 'jewelry', 'fashion-jewelry'],
    'Boucles': ['earrings', 'jewelry', 'fashion-accessory'],
    'Portefeuille': ['wallet', 'leather-wallet', 'accessories'],
    
    # Montres
    'Montre': ['watch', 'wristwatch', 'timepiece'],
    'Smartwatch': ['smartwatch', 'apple-watch', 'digital-watch'],
    
    # Sacs et casquettes
    'Casquette': ['cap', 'baseball-cap', 'hat'],
    'Sac': ['bag', 'backpack', 'handbag'],
    'Sacoche': ['messenger-bag', 'laptop-bag', 'work-bag'],
    'Bob': ['bucket-hat', 'summer-hat', 'casual-hat'],
    
    # Cosmétiques
    'Parfum': ['perfume', 'fragrance', 'cologne'],
    'Crème': ['skincare', 'moisturizer', 'beauty-cream'],
    'Lotion': ['body-lotion', 'skincare', 'cosmetics'],
    'Gel': ['shower-gel', 'body-wash', 'bath-products'],
    'Déodorant': ['deodorant', 'antiperspirant', 'personal-care'],
    'Shampoing': ['shampoo', 'hair-care', 'beauty-products'],
    
    # Jouets
    'Peluche': ['teddy-bear', 'plush-toy', 'stuffed-animal'],
    'Puzzle': ['jigsaw-puzzle', 'puzzle-game', 'brain-game'],
    'Poupée': ['doll', 'toy-doll', 'kids-toy'],
    'Voiture': ['toy-car', 'model-car', 'kids-vehicle'],
    'LEGO': ['lego', 'building-blocks', 'construction-toy'],
    'Figurine': ['action-figure', 'collectible', 'toy-figure'],
    'Jeu': ['board-game', 'family-game', 'table-game']
}

def get_unsplash_url(product_name, product_type, index=1):
    """Génère une URL Unsplash cohérente pour un produit"""
    
    # Trouver le mot-clé approprié
    keyword = 'fashion'  # mot-clé par défaut
    
    for key, keywords in unsplash_keywords.items():
        if key.lower() in product_type.lower() or key.lower() in product_name.lower():
            keyword = random.choice(keywords)
            break
    
    # Ajouter une variation pour éviter les doublons
    seed = f"{product_name.replace(' ', '-').lower()}-{index}"
    
    return f"https://source.unsplash.com/800x600/?{keyword}&sig={abs(hash(seed)) % 10000}"

# Récupérer tous les produits
products = Product.objects.all()
print(f"Produits trouvés: {products.count()}")

total_updated = 0

for product in products:
    print(f"\nMise à jour des images pour: {product.name}")
    
    # Supprimer les anciennes images
    old_images = ProductImage.objects.filter(product=product)
    old_count = old_images.count()
    old_images.delete()
    print(f"  - Supprimé {old_count} anciennes images")
    
    # Déterminer le type de produit pour les mots-clés
    product_type = ""
    for word in product.name.split():
        if word in ['T-shirt', 'Chemise', 'Pantalon', 'Veste', 'Pull', 'Sweat', 'Jean', 'Polo', 
                   'Robe', 'Jupe', 'Legging', 'Blouse', 'Short', 'Pyjama', 'Bermuda',
                   'Sneakers', 'Bottes', 'Mocassins', 'Sandales', 'Baskets', 'Escarpins', 'Derbies',
                   'Ceinture', 'Écharpe', 'Gants', 'Bracelet', 'Collier', 'Portefeuille',
                   'Montre', 'Smartwatch', 'Casquette', 'Sac', 'Sacoche', 'Bob',
                   'Parfum', 'Crème', 'Lotion', 'Gel', 'Déodorant', 'Shampoing',
                   'Peluche', 'Puzzle', 'Poupée', 'Voiture', 'LEGO', 'Figurine', 'Jeu']:
            product_type = word
            break
    
    if not product_type:
        product_type = product.subcategory.name if product.subcategory else "fashion"
    
    # Créer 2-3 nouvelles images avec Unsplash
    num_images = random.randint(2, 3)
    for i in range(1, num_images + 1):
        image_url = get_unsplash_url(product.name, product_type, i)
        
        ProductImage.objects.create(
            product=product,
            image=image_url,
            is_main=(i == 1)
        )
        
        print(f"  + Image {i}: {image_url}")
    
    total_updated += 1

print(f"\n=== RÉSUMÉ ===")
print(f"✅ {total_updated} produits mis à jour avec de nouvelles images Unsplash")
print(f"📸 Images cohérentes basées sur le type de produit")
print(f"🔗 URLs Unsplash fonctionnelles avec mots-clés appropriés")
print("\nTerminé!")
