CREATE TABLE movie (id int NOT NULL AUTO_INCREMENT, movie_name varchar(255), year varchar(255), duration varchar(255), user_id int, PRIMARY KEY (id), FOREIGN KEY (user_id) REFERENCES user(id));


INSERT INTO movie (movie_name,year,duration,user_id) VALUES ('Avengers', '2019', '3hr', 1);