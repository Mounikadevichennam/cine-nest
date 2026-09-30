# CineNest Relational Database ER Schema

## Normalized Entities (16 Relational Tables)

1. `users`: Subscriber & Admin user accounts. (`id`, `name`, `email` [UQ], `password_hash`, `role` [`USER`|`ADMIN`], `preferred_language`).
2. `profiles`: Account watching profile avatars (`id`, `user_id` [FK], `profile_name`, `avatar`).
3. `movies`: Catalog movie records (`id`, `imdb_id` [UQ], `tmdb_id` [UQ], `title` [IDX], `language` [IDX], `release_year` [IDX], `imdb_rating` [IDX], `poster_url`, `trailer_url`).
4. `genres`: Catalog genres (`id`, `name` [UQ]).
5. `actors`: Cast members (`id`, `name` [UQ], `profile_image_url`).
6. `movie_genres`: Junction table (`movie_id` [FK], `genre_id` [FK]).
7. `movie_actors`: Junction table (`movie_id` [FK], `actor_id` [FK], `character_name`).
8. `user_favourite_genres`: Junction table (`user_id` [FK], `genre_id` [FK]).
9. `user_favourite_actors`: Junction table (`user_id` [FK], `actor_id` [FK]).
10. `watch_history`: Watch tracking (`id`, `user_id` [FK], `movie_id` [FK], `progress_seconds`, `completion_percentage`, `completed`).
11. `likes`: Explicit likes (`id`, `user_id` [FK], `movie_id` [FK], UQ: `[user_id, movie_id]`).
12. `not_interested`: Negative feedback (`id`, `user_id` [FK], `movie_id` [FK], UQ: `[user_id, movie_id]`).
13. `ratings`: User 1-5 star ratings (`id`, `user_id` [FK], `movie_id` [FK], UQ: `[user_id, movie_id]`, `rating`).
14. `search_history`: Search queries (`id`, `user_id` [FK], `search_query`, `searched_at`).
15. `continue_watching`: Active watch progress (`id`, `user_id` [FK], `movie_id` [FK], UQ: `[user_id, movie_id]`).
16. `recent_activities`: Timestamped user logs (`id`, `user_id` [FK], `movie_id` [FK], `activity_type`).
