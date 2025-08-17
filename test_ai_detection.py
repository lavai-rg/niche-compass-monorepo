#!/usr/bin/env python3

def test_detection(url):
    url_lower = url.lower()
    print(f"Testing URL: {url}")
    print(f"URL lower: {url_lower}")
    
    category_patterns = {
        'jewelry': ['jewelry', 'necklace', 'bracelet', 'ring', 'earring', 'pendant', 'silver', 'gold'],
        'pet_accessories': ['pet', 'dog', 'cat', 'collar', 'leash', 'toy'],
        'home_decor': ['decor', 'home', 'wall', 'furniture', 'vintage', 'rustic'],
        'art': ['art', 'print', 'poster', 'painting', 'canvas', 'illustration'],
        'crafts': ['craft', 'diy', 'knit', 'fabric', 'paper', 'handmade']
    }
    
    for category, patterns in category_patterns.items():
        matches = [pattern for pattern in patterns if pattern in url_lower]
        if matches:
            print(f"✅ Category: {category}, Matches: {matches}")
            return category
        else:
            print(f"❌ Category: {category}, No matches")
    
    print("No matches found")
    return "unknown"

# Test different URLs
test_urls = [
    "https://etsy.com/listing/jewelry123",
    "https://etsy.com/listing/silver-jewelry-necklace-456", 
    "https://etsy.com/listing/handmade-jewelry-ring-123",
    "https://etsy.com/listing/pet-collar-dog-456",
    "https://etsy.com/listing/home-decor-wall-art-789"
]

for url in test_urls:
    print("="*50)
    test_detection(url)
    print()