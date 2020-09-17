-- Find movies of a particular Category.name

 SELECT * FROM movie JOIN movie_category ON movie.id=movie_category.movie_id JOIN category ON  category.id=movie_category.category_id WHERE category.name='Thriller';

-- Find movies of a particular Category.name by a particular user.name

SELECT * FROM movie JOIN movie_category ON movie.id=movie_category.movie_id JOIN user ON  user.id=movie.user_id WHERE user.name='Vaisakh';