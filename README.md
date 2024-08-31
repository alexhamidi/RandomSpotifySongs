# Spotibulk

## Info
Spotibulk is an algorithm that returns a list of related spotify track ids given a set of artists. It:
- Supports fetching a very high number of spotify ids (tested to 2 million, though it took a while)
- Uses a Breath-first search approach on artists' related artists to gradually expand the search space
- Provides several parameters to adjust the search behavior, allowing you to fine-tune the app based on your needs (See usage for details)
- Is easily modifiable to fetch albums or artists

- Storing everything in a list allows for versatility - once you have the list, you can add tracks to a database, write them to a file, or even add them to a playlist. 


## Install

To start, clone into this repository in your project:
```git
git clone https://github.com/alexhamidi/Spotibulk.git
```

After this, you need to install aiohttp:
```python
pip3 install aiohttp
```

The final step is to add your spotify token to index.py using any method you'd like:
```python
TOKEN = 'YOUR TOKEN HERE'
```

Now, you're ready to Spotibulk!

## Usage


Provided a list of Spotify artist ids and nothing else, Spotibulk returns every (unique) song of these artists and their related artists.

`seed_ids` _(Required)_:
- A list of Spotify artist IDs to start the search from
- These are the initial artists whose music and related artists will be explored
- Example: `['0iEtIxbK0KxaSlF7G42ZOp', '5K4W6rqBFWDnAN6FQUkS6x']`

`search_depth` _(Optional, default: 1)_:
- This value represents the number of rounds of BFS are completed on the existing artists.
- Increasing this leads to exponentially higher songs and runtime.
- Example: if this is 2, then you get all the artists related to the seed artists, then you get all the artists related to _those_ artists, then you get the tracks of every single artist you've encountered.

`max_albums_per_artist` _(Optional, default: inf)_:
- The maximum number of albums to fetch per artist
- Useful to limit the influence of prolific artists on the result
- Randomly selects albums if the artist has more albums than this number

`max_tracks_per_album_request`  _(Optional, default: inf)_:
- The maximum number of tracks to fetch per album request
- Limits the number of tracks fetched from each album
- Randomly selects tracks if a set of albums has more tracks than this number
- **Note:** this is _not_ the maximum tracks retrieved per album. Fetching tracks album by album is too computationally expensive, and this parameter adjusts how many tracks are selected in each batch request of 20 songs.

`max_related_artists_per_artist` _(Optional, default: inf)_:
- The maximum number of related artists to fetch for each artist
- Useful for controlling the breadth of the search
- Also useful to accelerate the spread of the search space
- Randomly selects related artists if an artist has more related artist than this number of related artists

`max_songs`  _(Optional, default: -1 [no limit])_:
- The maximum total number of songs to return
- Useful for capping the total size of the returned list for certain applications
- **Note:** this value is not guaranteed - if the number of returned songs is lower than ```max_songs```, this parameter changes nothing


### Example

```python
from index import generate_songs

async def main():
    seed_ids = [
        '0iEtIxbK0KxaSlF7G42ZOp',  # Travis Scott
        '5K4W6rqBFWDnAN6FQUkS6x',  # Ye
        '699OTQXzgjhIYAHMy9RyPD',  # Carti
    ]

    trap_song_ids = await generate_songs(seed_ids, search_depth=2, max_albums_per_artist=1)

    print(f"ids retreived succesfully, {len(trap_song_ids)} ids in the list. First 5 items: {trap_song_ids[:5]}")

asyncio.run(main())

```
