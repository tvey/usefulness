# YouTube Data API

The API provides access to various types of resources. Among them:
* channels
* comments
* playlistItems
* playlists
* search
* subscriptions
* videoCategories
* videos

Most of the resources support common methods:
* **`list`** (GET)
* **`insert`** (POST)
* **`update`** (PUT)
* **`delete`** (DELETE)

Only `list` operation will be used in examples from this section of usefulness.

All the `GET` calls require an [API key](https://developers.google.com/youtube/v3/getting-started).