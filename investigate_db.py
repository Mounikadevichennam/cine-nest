import sqlite3

conn = sqlite3.connect('backend/cinenest.db')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM movies")
total_rows = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM movies WHERE poster_url IS NOT NULL AND poster_url != ''")
valid_posters = c.fetchone()[0]

c.execute("SELECT COUNT(DISTINCT tmdb_id) FROM movies WHERE tmdb_id IS NOT NULL")
distinct_tmdb = c.fetchone()[0]

c.execute("SELECT tmdb_id, title, release_date, release_year FROM movies WHERE release_year NOT BETWEEN 2016 AND 2026 OR release_year IS NULL")
out_of_range_years = c.fetchall()

print(f"Total Rows in 'movies' table: {total_rows}")
print(f"Valid Posters Count: {valid_posters}")
print(f"Distinct TMDB IDs: {distinct_tmdb}")
print(f"Out of range (not 2016-2026) records count: {len(out_of_range_years)}")

for r in out_of_range_years:
    print(f"  TMDB_ID: {r[0]} | Title: {r[1]} | Release Date: {r[2]} | Release Year: {r[3]}")

# Check duplicate tmdb_ids
c.execute("SELECT tmdb_id, COUNT(*) FROM movies WHERE tmdb_id IS NOT NULL GROUP BY tmdb_id HAVING COUNT(*) > 1")
duplicates = c.fetchall()
print(f"\nDuplicate TMDB IDs count: {len(duplicates)}")
for d in duplicates:
    print(f"  TMDB_ID: {d[0]} | Count: {d[1]}")

# Year breakdown sum
years = list(range(2016, 2027))
sum_years = 0
print("\nYear Breakdown:")
for y in years:
    c.execute("SELECT COUNT(*) FROM movies WHERE release_year = ?", (y,))
    cnt = c.fetchone()[0]
    sum_years += cnt
    print(f"  {y}: {cnt}")

print(f"Sum of 2016-2026 years: {sum_years}")
print(f"Difference (Total Rows - Year Sum): {total_rows - sum_years}")

conn.close()
