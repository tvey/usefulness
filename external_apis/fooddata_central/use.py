import os

import dotenv

from fooddata import FoodData

dotenv.load_dotenv()

fd = FoodData(api_key=os.environ.get('API_KEY'))

# search endpoint
apple_result = fd.search('apple')
apple_ids = fd.get_ids('orange', write=True)

# detail endpoint
detail = fd.foods(1097926, write=True)
