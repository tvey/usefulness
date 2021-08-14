# FoodData API wrapper

FoodData Central is a system of food and nutrient data. Its API provides REST access to this data.

The API provides two major endpoints:
- the Food Search endpoint (`/search`),
- the Food Details endpoint (`/food/{fdcId}`).

We'll be using only GET requests to the available endpoints.

For access, anyone should [obtain an API key](https://fdc.nal.usda.gov/api-guide.html) and use it with every request.

Use importing a `FoodData` class from `fooddata.py` module or as a command line tool.

## Example of usage as a command line tool

```bash
python fooddata.py apple

python fooddata.py orange --write

python fooddata.py "ice cream" --get_ids --write

python fooddata.py 1097926 -w
```

Get help: `python fooddata.py --help`

Output:

```
usage: fooddata api_key query --get_ids --write

Get food data from FoodData Cental API.

positional arguments:
  query                 Either a search string or a food id.
  api_key               Valid API key, get it signing up on https://fdc.nal.usda.gov/

optional arguments:
  -h, --help            show this help message and exit
  -ids [GET_IDS], --get-ids [GET_IDS]
                        Search and get abridged results in a form of food ids and names.
  -w [WRITE], --write [WRITE]
                        Write results to a file locally.

```

## Example of usage the FoodData class directly

```python
from fooddata import FoodData

fd = FoodData.init(api_key='Your valid FDC API key')

result = fd.search('ice cream', write=True)
```

## To-do

- [ ] Test the functionality