-- Find the count of all the reviews in different movies
SElECT movie.movie_name,COUNT(movie_review.movie_id) as number_of_comments FROM movie_review JOIN movie ON movie_review.movie_id=movie.id GROUP BY movie_review.movie_id;
