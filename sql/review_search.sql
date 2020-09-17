-- Find review of a particular user.name
SELECT * FROM movie_review JOIN user ON movie_review.user_id=user.id WHERE user.name='Vaisakh';