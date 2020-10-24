DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user (
  username, password)
VALUES('tester1','hunter1'),('tester2','hunter2'),('tester3','hunter3');

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

INSERT INTO category (
  title)
VALUES('kategori1'),('kategori2'),('kategori3');

CREATE TABLE thread (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category_id INTEGER
);

INSERT INTO thread (
  title, category_id)
VALUES('threadd1','1'),('thread2','2'),('thread3','3');

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  /*title TEXT NOT NULL,*/
  body TEXT NOT NULL,
  thread_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
INSERT INTO post (
  author_id, body,thread_id)
VALUES('tester1','test1','1'),('tester2','test12','1'),('tester3','test13','1'),('tester1','test21','2'),('tester2','test21','2'),('tester3','test23','2'),('tester1','test31','3'),('tester2','test32','3'),('tester3','test33','3');