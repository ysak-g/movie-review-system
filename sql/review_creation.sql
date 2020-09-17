CREATE TABLE movie_review (id int NOT NULL AUTO_INCREMENT, comment varchar(255), movie_id int, user_id int, PRIMARY KEY (id), FOREIGN KEY (movie_id) REFERENCES movie(id), FOREIGN KEY (user_id) REFERENCES user(id));

INSERT INTO movie_review (comment,movie_id,user_id) VALUES ('Good',1,1);