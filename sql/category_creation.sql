CREATE TABLE category (id int NOT NULL AUTO_INCREMENT, name varchar(255), PRIMARY KEY (id));

-- Relationship table - movie_category
CREATE TABLE movie_category (id int NOT NULL AUTO_INCREMENT, movie_id int, category_id  int, PRIMARY KEY (id), FOREIGN KEY (movie_id) REFERENCE movie(id), FOREIGN KEY (category_id) REFERENCES category(id));

