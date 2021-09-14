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

* [YouTube Data API](#youtube-data-api)

* [FoodData Central](#fooddata-central)

## YouTube Data API

**Code and info:** [youtube_data_api](youtube_data_api)

**Resources:** [Various types](https://developers.google.com/youtube/v3/getting-started#resources) of data entities from YouTube

**Auth:** API key (for retrieve operations only)

## FoodData Central

**Code and info:** [fooddata_central](fooddata_central)

**Resources:** Nutritional and food data

**Auth:** API key
