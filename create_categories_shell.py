#!/usr/bin/env python
"""
Script pour exécuter dans le shell Django
Utilisation: docker-compose exec backend python manage.py shell
Puis copier-coller ce script
"""

from django.utils.text import slugify
from products.models import Category, SubCategory

# Données des catégories et sous-catégories
categories_data = {
    'Hommes': {
        'description': 'Mode et accessoires pour hommes',
        'subcategories': [
            'Vêtements',
            'Chaussures',
            'Accessoires',
            'Montres',
            'Casquettes',
            'Produits cosmétiques'
        ]
    },
    'Femmes': {
        'description': 'Mode et accessoires pour femmes',
        'subcategories': [
            'Vêtements',
            'Chaussures',
            'Accessoires',
            'Montres',
            'Sacs',
            'Produits cosmétiques'
        ]
    },
    'Enfants': {
        'description': 'Mode et accessoires pour enfants',
        'subcategories': [
            'Vêtements garçons',
            'Vêtements filles',
            'Chaussures',
            'Accessoires',
            'Jouets'
        ]
    }
}

print('=== Création des catégories et sous-catégories ===\n')

# Création des catégories principales et leurs sous-catégories
for category_name, category_info in categories_data.items():
    # Créer la catégorie principale
    category_slug = slugify(category_name)
    category, created = Category.objects.get_or_create(
        name=category_name,
        slug=category_slug,
        defaults={
            'description': category_info['description'],
            'is_published': True,
            'meta_title': f'{category_name} - EVIMERIA',
            'meta_description': f'Découvrez notre collection {category_name.lower()} sur EVIMERIA'
        }
    )
    
    if created:
        print(f'✓ Catégorie créée : {category_name}')
    else:
        print(f'→ La catégorie {category_name} existe déjà')

    # Créer les sous-catégories
    subcategories_created = 0
    subcategories_existing = 0
    
    for subcategory_name in category_info['subcategories']:
        subcategory_slug = slugify(subcategory_name)
        subcategory, sub_created = SubCategory.objects.get_or_create(
            category=category,
            name=subcategory_name,
            slug=subcategory_slug,
            defaults={
                'description': f'{subcategory_name} pour {category_name.lower()}',
                'is_published': True,
                'meta_title': f'{subcategory_name} {category_name} - EVIMERIA',
                'meta_description': f'Collection {subcategory_name.lower()} pour {category_name.lower()}'
            }
        )
        
        if sub_created:
            subcategories_created += 1
            print(f'  ✓ Sous-catégorie créée : {subcategory_name}')
        else:
            subcategories_existing += 1
            print(f'  → Sous-catégorie existante : {subcategory_name}')
    
    print(f'  Résumé pour {category_name}: {subcategories_created} créées, {subcategories_existing} existantes\n')

# Afficher un résumé final
total_categories = Category.objects.count()
total_subcategories = SubCategory.objects.count()

print(f'\n=== Résumé final ===')
print(f'Total catégories : {total_categories}')
print(f'Total sous-catégories : {total_subcategories}')
print(f'\n✓ Configuration terminée avec succès !')
