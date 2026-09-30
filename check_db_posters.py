import sqlite3

conn = sqlite3.connect('backend/cinenest.db')
c = conn.cursor()

c.execute("SELECT id, title, poster_url, backdrop_url, release_year, language FROM movies WHERE title LIKE '%RRR%' OR title LIKE '%Pushpa%' OR title LIKE '%Kalki%' OR title LIKE '%Kantara%' OR title LIKE '%Manjummel%' OR title LIKE '%Leo%' LIMIT 10")
rows = c.fetchall()

print("=" * 80)
print(f"FOUND {len(rows)} MATCHING MOVIES IN DB:")
print("=" * 80)
for r in rows:
    print(f"ID: {r[0]} | Title: {r[1]} | Year: {r[4]} | Lang: {r[5]}")
    print(f"   Poster URL:   {r[2]}")
    print(f"   Backdrop URL: {r[3]}")
    print("-" * 80)

conn.close()
