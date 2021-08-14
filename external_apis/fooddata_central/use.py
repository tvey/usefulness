import os

import dotenv

from fooddata import FoodData

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')

fd = FoodData.init(api_key=API_KEY)

# search endpoint
apple_result = fd.search('apple')
apple_ids = fd.get_ids('orange', write=True)

# detail endpoint
detail = fd.get_details(1097926, write=True)
