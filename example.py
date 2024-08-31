from index import generate_songs
import asyncio

async def main():
    seed_ids = [
        '0iEtIxbK0KxaSlF7G42ZOp',  # Travis Scott
        '2ye2Wgw4gimLv2eAKyk1NB',  # Metallica
        '4tZwfgrHOc3mvqYlEYSvVi',  # Daft Punk
        '6kACVPfCOnqzgfEF5ryl0x',  # Johnny Cash
        '51Blml2LZPmy7TTiAg47vQ',  # U2
        '5aIqB5nVVvmFsvSdExz408',  # Bach
        '7w29UYBi0qsHi5RTcv3lmA',  # Bjork
        '3koiLjNrgRTNbOwViDipeA',  # Marvin Gaye
        '6MJKlN8ya42Agsw3iQZs6e',  # French 79
        '5Pb27ujIyYb33zBqVysBkj',  # Rufus
        '4Z8W4fKeB5YxbusRsdQVPb',  # Radiohead
    ]

    song_ids = await generate_songs(seed_ids, search_depth=2)

    print(f"ids retreived succesfully, {len(song_ids)} ids in the list. First 5 items: {song_ids[:5]}")
    # Retrieves 301931 ids related to the artists


asyncio.run(main())



