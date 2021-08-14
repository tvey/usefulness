# Python and REST APIs

This folder contains examples of calling external APIs (web services).
Every service has different formats and rules for the calls and resources.

Developers can use data from external APIs in their applications.
It makes these web services truly great and useful.

All HTTP requests are made using an amazing [Requests](https://github.com/psf/requests) library.

Sometimes simple API wrappers are created with use cases in a separate module.

For services that require authentication, keys are obtained and stored as environment variables.
(`.env` files store them, and [python-dotenv](https://github.com/theskumar/python-dotenv) loads them.)

## Index

* [FoodData Central](#fooddata-central)

## FoodData Central

**Code and info:** [fooddata_central](fooddata_central)

**Resources:** Nutritional and food data

**Auth:** API key
