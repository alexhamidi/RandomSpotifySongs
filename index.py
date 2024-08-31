import asyncio # sempahore accessed through asyncio
import aiohttp
from collections import deque
import random
import sys

TOKEN = 'YOUR TOKEN HERE'

BASE_URL = "https://api.spotify.com/v1"
MAX_RETRIES = 5
RATE_LIMIT_DELAY = 1
CONCURRENT_REQUESTS = 10

SEMAPHORE = asyncio.Semaphore(CONCURRENT_REQUESTS)

async def fetch_data(session, url, params=None):
    async with SEMAPHORE:
        for attempt in range(MAX_RETRIES):
            try:
                async with session.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, params=params) as response:
                    if response.status == 429:
                        retry_after = int(response.headers.get('Retry-After')) or RATE_LIMIT_DELAY
                        await asyncio.sleep(retry_after)
                        continue
                    elif response.status == 401:
                        raise Exception("Unauthorized. Please check your API key.")
                    return await response.json()
            except aiohttp.ClientError as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        raise Exception(f"Error: Max retries reached for {url}")

async def get_artist_albums(session, artist_id, max_albums_per_artist):
    url = f"{BASE_URL}/artists/{artist_id}/albums"
    data = await fetch_data(session, url)
    albums = data.get('items', [])
    return [album['id'] for album in random.sample(albums, min(max_albums_per_artist, len(albums)))]

async def get_related_artists(session, artist_id, max_related_artists_per_artist):
    url = f"{BASE_URL}/artists/{artist_id}/related-artists"
    data = await fetch_data(session, url)
    artists = data.get('artists', [])
    return [artist['id'] for artist in random.sample(artists, min(max_related_artists_per_artist, len(artists)))]


async def get_album_tracks(session, album_ids, max_tracks_per_album_request):
    url = f"{BASE_URL}/albums"
    params = {"ids": ",".join(album_ids), "market": "US"}
    data = await fetch_data(session, url, params)
    tracks = []
    for album in data.get('albums', []):
        if album:
            tracks.extend([track['id'] for track in album.get('tracks', {}).get('items', [])])

    return [track for track in random.sample(tracks, min(max_tracks_per_album_request, len(tracks)))]

async def get_related_artists_bfs(session, seed_ids, depth, max_related_artists_per_artist):
    dq = deque([(id, 0) for id in seed_ids])
    visited_artists = set(seed_ids)
    all_artists = []
    while len(dq) > 0:
        curr_id, curr_depth = dq.popleft()
        all_artists.append(curr_id)
        if curr_depth < depth:
            related_artist_ids = await get_related_artists(session, curr_id, max_related_artists_per_artist)
            for artist_id in related_artist_ids:
                if artist_id not in visited_artists:
                    visited_artists.add(artist_id)
                    dq.append((artist_id, curr_depth + 1))
    return all_artists

async def generate_songs(seed_ids, search_depth=1, max_albums_per_artist=sys.maxsize, max_tracks_per_album_request=sys.maxsize,max_related_artists_per_artist=sys.maxsize, max_songs=-1):
    try:
        async with aiohttp.ClientSession() as session:
            print('Getting artist ids...')
            all_artist_ids = await get_related_artists_bfs(session, seed_ids, search_depth, max_related_artists_per_artist)
            print(f'Retrieved {len(all_artist_ids)} artist ids')

            print('Getting album ids...')
            album_tasks = [get_artist_albums(session, artist_id, max_albums_per_artist) for artist_id in all_artist_ids]
            all_album_ids = [id for sublist in await asyncio.gather(*album_tasks) for id in sublist]
            print(f'Retrieved {len(all_album_ids)} album ids')

            print('Getting song ids...')
            song_tasks = [get_album_tracks(session, all_album_ids[i:i+20], max_tracks_per_album_request) for i in range(0, len(all_album_ids), 20)]
            all_song_ids = [id for sublist in await asyncio.gather(*song_tasks) for id in sublist]
            print(f'Retrieved {len(all_song_ids)} song ids')

            if max_songs != -1 and len(all_song_ids) > max_songs:
                all_song_ids = all_song_ids[:max_songs]

            if len(all_song_ids) == 0:
                raise Exception("Error: no data collected")

            return all_song_ids

    except Exception as e:
        print(f"An error occurred during data fetching: {e}")
