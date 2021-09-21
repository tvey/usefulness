import os

import dotenv

from fooddata import FoodData

dotenv.load_dotenv()

fd = FoodData(api_key=os.environ.get('API_KEY'))

# search endpoint
apple_result = fd.search('apple')
apple_ids = fd.get_ids('orange', write=True)

# detail endpoint
detail = fd.get_foods(1097926, write=True)

# more than one item
result = fd.get_foods(['1105314', '1750349'])
