DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    title TEXT NOT NULL
);

INSERT INTO category (
  title)
VALUES('kategori1'),('kategori2'),('kategori3');

CREATE TABLE thread (
    author_id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    title TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER,
    FOREIGN KEY(author_id) REFERENCES user(id)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  /*title TEXT NOT NULL,*/
  body TEXT NOT NULL,
  FOREIGN KEY(author_id) REFERENCES user(id)
);

-- CREATE TABLE comment (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   comment_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   body TEXT NOT NULL,
--   FOREIGN KEY(author_id) REFERENCES user(id),
--   FOREIGN KEY(comment_id) REFERENCES user(id)
-- );