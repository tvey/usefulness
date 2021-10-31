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

Only `list` (GET) operation are present in the YouTube class.

All the `GET` calls require an [API key](https://developers.google.com/youtube/v3/getting-started).

## Todo

- [ ] Test better

The API sometimes doesn't return results for specific videos based on their ids or playlists for specific channels. Hmm...

- [ ] Handle [errors](https://developers.google.com/youtube/v3/docs/errors) better
