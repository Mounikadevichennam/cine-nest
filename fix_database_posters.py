import sqlite3

conn = sqlite3.connect('backend/cinenest.db')
c = conn.cursor()

# Remove old seed rows with fake/placeholder poster URLs
c.execute("DELETE FROM movies WHERE poster_url LIKE '%z8c8%' OR poster_url LIKE '%3z8%' OR tmdb_id IS NULL")
deleted_count = c.rowcount

conn.commit()

# Verify remaining movies
c.execute("SELECT COUNT(*) FROM movies")
total_movies = c.fetchone()[0]

c.execute("SELECT id, title, poster_url, release_year, language FROM movies WHERE title IN ('RRR', 'Pushpa 2: The Rule', 'Kalki 2898 AD', 'Kantara', 'Manjummel Boys', 'Leo') LIMIT 10")
samples = c.fetchall()

print("=" * 80)
print(f"DATABASE POSTER CLEANUP SUCCESSFUL!")
print(f"Deleted old seed entries with fake posters: {deleted_count}")
print(f"Total Genuine TMDB Movies Remaining: {total_movies}")
print("=" * 80)
print("SAMPLE REAL TMDB MOVIES IN DB:")
for s in samples:
    print(f"ID: {s[0]} | Title: {s[1]} | Year: {s[3]} | Lang: {s[4]}")
    print(f"   Real TMDB Poster URL: {s[2]}")
    print("-" * 80)

conn.close()
