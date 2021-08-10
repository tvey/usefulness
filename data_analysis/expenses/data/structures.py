import json

PRODUCTS = [
    {
        "product": "rent",
        "price": 40000,
        "category": "bills"
    },
    {
        "product": "electricity",
        "price": 800,
        "category": "bills"
    },
    {
        "product": "water",
        "price": 1500,
        "category": "bills"
    },
    {
        "product": "internet",
        "price": 500,
        "category": "bills"
    },
    {
        "product": "mobile",
        "price": 1000,
        "category": "bills"
    },
    {
        "product": "metro",
        "price": 1500,
        "category": "bills"
    },
    {
        "product": "bus",
        "price": 2200,
        "category": "bills"
    },
    {
        "product": "bread",
        "price": 60,
        "category": "food"
    },
    {
        "product": "milk",
        "price": 60,
        "category": "food"
    },
    {
        "product": "eggs",
        "price": 100,
        "category": "food"
    },
    {
        "product": "cheese",
        "price": 300,
        "category": "food"
    },
    {
        "product": "another cheese",
        "price": 300,
        "category": "food"
    },
    {
        "product": "cream cheese",
        "price": 100,
        "category": "food"
    },
    {
        "product": "cottage cheese",
        "price": 100,
        "category": "food"
    },
    {
        "product": "yogurt",
        "price": 50,
        "category": "food"
    },
    {
        "product": "butter",
        "price": 150,
        "category": "food"
    },
    {
        "product": "olive oil",
        "price": 350,
        "category": "food"
    },
    {
        "product": "chicken",
        "price": 300,
        "category": "food"
    },
    {
        "product": "fish",
        "price": 300,
        "category": "food"
    },
    {
        "product": "buckwheat",
        "price": 80,
        "category": "food"
    },
    {
        "product": "rice",
        "price": 80,
        "category": "food"
    },
    {
        "product": "millet",
        "price": 80,
        "category": "food"
    },
    {
        "product": "oats",
        "price": 60,
        "category": "food"
    },
    {
        "product": "beans",
        "price": 120,
        "category": "food"
    },
    {
        "product": "potatoes",
        "price": 60,
        "category": "food"
    },
    {
        "product": "apples",
        "price": 80,
        "category": "food"
    },
    {
        "product": "oranges",
        "price": 80,
        "category": "food"
    },
    {
        "product": "lemons",
        "price": 80,
        "category": "food"
    },
    {
        "product": "bananas",
        "price": 80,
        "category": "food"
    },
    {
        "product": "tomatoes",
        "price": 80,
        "category": "food"
    },
    {
        "product": "cucumbers",
        "price": 80,
        "category": "food"
    },
    {
        "product": "peppers",
        "price": 80,
        "category": "food"
    },
    {
        "product": "carrots",
        "price": 50,
        "category": "food"
    },
    {
        "product": "onions",
        "price": 50,
        "category": "food"
    },
    {
        "product": "nuts",
        "price": 300,
        "category": "food"
    },
    {
        "product": "coffee",
        "price": 400,
        "category": "food"
    },
    {
        "product": "tea",
        "price": 200,
        "category": "food"
    },
    {
        "product": "coffee",
        "price": 110,
        "category": "junk"
    },
    {
        "product": "latte",
        "price": 110,
        "category": "junk"
    },
    {
        "product": "americano",
        "price": 90,
        "category": "junk"
    },
    {
        "product": "takeaway coffee",
        "price": 110,
        "category": "junk"
    },
    {
        "product": "chocolate",
        "price": 120,
        "category": "junk"
    },
    {
        "product": "dark chocolate",
        "price": 120,
        "category": "junk"
    },
    {
        "product": "white chocolate",
        "price": 100,
        "category": "junk"
    },
    {
        "product": "ice cream",
        "price": 100,
        "category": "junk"
    },
    {
        "product": "another ice cream",
        "price": 80,
        "category": "junk"
    },
    {
        "product": "yet another ice cream",
        "price": 60,
        "category": "junk"
    },
    {
        "product": "cookies",
        "price": 80,
        "category": "junk"
    },
    {
        "product": "another cookies",
        "price": 80,
        "category": "junk"
    },
    {
        "product": "candy bar",
        "price": 50,
        "category": "junk"
    },
    {
        "product": "chips",
        "price": 100,
        "category": "junk"
    },
    {
        "product": "bepis",
        "price": 60,
        "category": "junk"
    },
    {
        "product": "chewing gum",
        "price": 40,
        "category": "junk"
    },
    {
        "product": "cake",
        "price": 100,
        "category": "junk"
    },
    {
        "product": "toothpaste",
        "price": 200,
        "category": "household"
    },
    {
        "product": "toothbrushes",
        "price": 200,
        "category": "household"
    },
    {
        "product": "floss",
        "price": 200,
        "category": "household"
    },
    {
        "product": "shampoo",
        "price": 200,
        "category": "household"
    },
    {
        "product": "washing liquid",
        "price": 200,
        "category": "household"
    },
    {
        "product": "washing powder",
        "price": 200,
        "category": "household"
    },
    {
        "product": "dish wash gel",
        "price": 100,
        "category": "household"
    },
    {
        "product": "dish sponges",
        "price": 50,
        "category": "household"
    },
    {
        "product": "paper towels",
        "price": 100,
        "category": "household"
    },
    {
        "product": "garbage bags",
        "price": 100,
        "category": "household"
    },
    {
        "product": "cleaner",
        "price": 150,
        "category": "household"
    },
    {
        "product": "soap",
        "price": 70,
        "category": "household"
    },
    {
        "product": "liquid soap",
        "price": 100,
        "category": "household"
    },
    {
        "product": "toilet paper",
        "price": 150,
        "category": "household"
    },
    {
        "product": "wipes",
        "price": 100,
        "category": "household"
    },
    {
        "product": "razors",
        "price": 150,
        "category": "household"
    },
    {
        "product": "pants",
        "price": 2000,
        "category": "clothing"
    },
    {
        "product": "tee",
        "price": 2000,
        "category": "clothing"
    },
    {
        "product": "shoes",
        "price": 4000,
        "category": "clothing"
    },
    {
        "product": "medical tests",
        "price": 1000,
        "category": "health"
    },
    {
        "product": "doctor visit",
        "price": 2000,
        "category": "health"
    },
    {
        "product": "meds",
        "price": 1000,
        "category": "health"
    }
]

CATEGORIES = {
    'bills': {
        'rent': 40000,
        'electricity': 800,
        'water': 1500,
        'internet': 500,
        'mobile': 1000,
        'metro': 1500,
        'bus': 2200,
    },
    'food': {
        'bread': 60,
        'milk': 60,
        'eggs': 100,
        'cheese': 300,
        'another cheese': 300,
        'cream cheese': 100,
        'cottage cheese': 100,
        'yogurt': 50,
        'butter': 150,
        'olive oil': 350,
        'chicken': 300,
        'fish': 300,
        'buckwheat': 80,
        'rice': 80,
        'millet': 80,
        'oats': 60,
        'beans': 120,
        'potatoes': 60,
        'apples': 80,
        'oranges': 80,
        'lemons': 80,
        'bananas': 80,
        'tomatoes': 80,
        'cucumbers': 80,
        'peppers': 80,
        'carrots': 50,
        'onions': 50,
        'nuts': 300,
        'coffee': 400,
        'tea': 200,
    },
    'junk': {
        'coffee': 110,
        'latte': 110,
        'americano': 90,
        'takeaway coffee': 110,
        'chocolate': 120,
        'dark chocolate': 120,
        'white chocolate': 100,
        'ice cream': 100,
        'another ice cream': 80,
        'yet another ice cream': 60,
        'cookies': 80,
        'another cookies': 80,
        'candy bar': 50,
        'chips': 100,
        'bepis': 60,
        'chewing gum': 40,
        'cake': 100,
    },
    'household': {
        'toothpaste': 200,
        'toothbrushes': 200,
        'floss': 200,
        'shampoo': 200,
        'washing liquid': 200,
        'washing powder': 200,
        'dish wash gel': 100,
        'dish sponges': 50,
        'paper towels': 100,
        'garbage bags': 100,
        'cleaner': 150,
        'soap': 70,
        'liquid soap': 100,
        'toilet paper': 150,
        'wipes': 100,
        'razors': 150,
    },
    'clothing': {
        'pants': 2000,
        'tee': 2000,
        'shoes': 4000,
    },
    'health': {
        'medical tests': 1000,
        'doctor visit': 2000,
        'meds': 1000,

    },
}


def flip_categories_to_products():
    data = CATEGORIES.copy()
    result = []

    for category, products in data.items():
        for name, price in products.items():
            result.append(
                {
                    'product': name,
                    'price': price,
                    'category': category,
                }
            )

    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    flip_categories_to_products()
