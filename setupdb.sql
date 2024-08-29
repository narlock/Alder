-- Create Database
DROP DATABASE IF EXISTS `alder`;
CREATE DATABASE alder;
USE alder;

-- Initialize Database Tables
DROP TABLE IF EXISTS `user`;
CREATE TABLE user(
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    tokens INT UNSIGNED NOT NULL,
    stime BIGINT UNSIGNED NOT NULL,
    hex VARCHAR(7),
    trivia INT UNSIGNED
);

DROP TABLE IF EXISTS `monthtime`;
CREATE TABLE monthtime(
    user_id BIGINT UNSIGNED NOT NULL,
    mth SMALLINT NOT NULL,
    yr SMALLINT NOT NULL,
    stime INT UNSIGNED NOT NULL,
    PRIMARY KEY (user_id, mth, yr),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `dailytime`;
CREATE TABLE dailytime(
    user_id BIGINT UNSIGNED NOT NULL,
    d SMALLINT NOT NULL,
    mth SMALLINT NOT NULL,
    yr SMALLINT NOT NULL,
    stime INT UNSIGNED NOT NULL,
    PRIMARY KEY (user_id, d, mth, yr),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `rbuser`;
CREATE TABLE rbuser(
    user_id BIGINT UNSIGNED NOT NULL,
    rbtype VARCHAR(15) NOT NULL,
    xp BIGINT UNSIGNED NOT NULL,
    model INT UNSIGNED NOT NULL,
    purchased_models VARCHAR(200),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `accomplishment`;
CREATE TABLE accomplishment(
    user_id BIGINT UNSIGNED NOT NULL,
    msg VARCHAR(200),
    PRIMARY KEY(user_id, msg)
);

DROP TABLE IF EXISTS `dailytoken`;
CREATE TABLE dailytoken(
    user_id BIGINT UNSIGNED NOT NULL,
    date_time DATETIME NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `achievement`;
CREATE TABLE achievement(
    id INT UNSIGNED,
    user_id BIGINT UNSIGNED,
    PRIMARY KEY(id, user_id)
);

DROP TABLE IF EXISTS `streak`;
CREATE TABLE streak(
    user_id BIGINT UNSIGNED NOT NULL,
    current_streak INT UNSIGNED DEFAULT 0,
    previous_connection_date DATE NOT NULL,
    highest_streak_achieved INT UNSIGNED DEFAULT 0,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `todo`;
CREATE TABLE todo(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    item_name VARCHAR(250),
    completed_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS `triviaquestion`;
CREATE TABLE `triviaquestion` (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(500) NOT NULL,
  option_a VARCHAR(100) NOT NULL,
  option_b VARCHAR(100) NOT NULL,
  option_c VARCHAR(100) NOT NULL,
  option_d VARCHAR(100) NOT NULL,
  correct SMALLINT NOT NULL,
  author VARCHAR(100) NOT NULL,
  category VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS `kanban`;
CREATE TABLE kanban (
    user_id BIGINT UNSIGNED NOT NULL,
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(250) NOT NULL,
    column_name VARCHAR(50) NOT NULL,
    priority_number INT,
    tag_name VARCHAR(50),
    velocity INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Insert sample data
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('What is Discord''s signature color?', 'Red', 'Blurple', 'Green', 'Gray', 1, 'Alder', 'Entertainment');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('What is the capital of France?', 'Berlin', 'Paris', 'Madrid', 'Rome', 1, 'Alder', 'Geography');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('Who was the first person to walk the moon?', 'Neil Armstrong', 'Buzz Aldrin', 'Michael Collins', 'Yuri Gagarin', 0, 'Alder', 'Science');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('Which planet in our solar system is known as the "Red Planet"?', 'Jupiter', 'Mars', 'Venus', 'Saturn', 1, 'Alder', 'Science');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('Which famous scientist wrote the book "A Brief History of Time"?', 'Albert Einstein', 'Stephen Hawking', 'Isaac Newton', 'Galileo Galilei', 1, 'Alder', 'Science');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('Which country gifted the Statue of Liberty to the United States?', 'Germany', 'France', 'Spain', 'Italy', 1, 'Alder', 'History');
INSERT INTO triviaquestion (title, option_a, option_b, option_c, option_d, correct, author, category) VALUES ('In what year did World War II end?', '1945', '1939', '1941', '1942', 0, 'Alder', 'History');