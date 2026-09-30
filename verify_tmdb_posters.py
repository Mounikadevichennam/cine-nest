import httpx
import json

TMDB_API_KEY = "d7d6c342fd68868931a108381ab57bcf"
BASE_URL = "https://api.themoviedb.org/3"

titles = ["RRR", "Pushpa 2: The Rule", "Kalki 2898 AD", "Kantara", "Manjummel Boys", "Leo"]

print("=" * 80)
print("FETCHING REAL TMDB POSTERS FOR KEY TITLES:")
print("=" * 80)

for t in titles:
    res = httpx.get(f"{BASE_URL}/search/movie", params={"api_key": TMDB_API_KEY, "query": t})
    if res.status_code == 200:
        results = res.json().get("results", [])
        if results:
            first = results[0]
            poster_path = first.get("poster_path")
            full_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            print(f"Title: {first.get('title')} | TMDB ID: {first.get('id')} | Year: {first.get('release_date')[:4] if first.get('release_date') else 'N/A'}")
            print(f"   Real TMDB Poster URL: {full_url}")
            print("-" * 80)
