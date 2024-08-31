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

### Parameters: 
```seed_ids:```
- 

```search_depth:```
- 

```max_albums_per_artist:```
- 

```max_tracks_per_album_request:```
- 

```max_related_artists_per_artist:```
- e

```max_songs:```
- 



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
