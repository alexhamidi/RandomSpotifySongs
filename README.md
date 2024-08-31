# Spotibulk

## Info
Spotify is an algorithm that returns a list of related spotify track ids given a set of artists. It:

- Supports fetching a very high number of spotify ids (tested to 2 million, though it took a while)
- Uses a Breath-first search approach on artists' related artists to gradually expand the search space
- Provides several parameters to adjust the search behavior, allowing you to fine-tune the app based on your needs (See usage for details)
- Is easily modifiable to fetch albums or artists

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

`seed_ids` (Required):
- A list of Spotify artist IDs to start the search from
- These are the initial artists whose music and related artists will be explored
- Example: `['0iEtIxbK0KxaSlF7G42ZOp', '5K4W6rqBFWDnAN6FQUkS6x']`

`search_depth` (Optional, default: 1):
- This value represents the number of rounds of BFS are completed on the existing artists.
- Default is 1 (only immediate related artists)
- Increasing this leads to exponentially higher songs and runtime.
- Example, if this is 2, then you get all the artists related to the seed artists, then you get all the artists related to _those_ artists, then you get the tracks of every single artist.

`max_albums_per_artist` (Optional, default: inf):
- The maximum number of albums to fetch per artist
- Limits the number of albums considered for each artist, useful for very prolific artists or to reduce API calls
- Randomly selects albums if the artist has more than this number

`max_tracks_per_album_request`  (Optional, default: inf):
- The maximum number of tracks to fetch per album request
- Limits the number of tracks fetched from each album
- Randomly selects tracks if an album has more than this number

`max_related_artists_per_artist` (Optional, default: inf):
- The maximum number of related artists to fetch for each artist
- Limits the branching factor of the artist search, useful for controlling the breadth of the search
- Randomly selects related artists if an artist has more than this number of related artists

`max_songs`  (Optional, default: -1 [no limit]):
- The maximum total number of songs to return
- Useful for capping the total size of the returned list
- The program will stop adding songs once this limit is reached, even if there are more available



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
