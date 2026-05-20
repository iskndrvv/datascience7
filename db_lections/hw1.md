mysql> CREATE DATABASE `library`;
Query OK, 1 row affected (0.052 sec)

mysql> USE library;
Database changed
mysql> CREATE TABLE books(
    ->     id INT PRIMARY KEY,
    ->     title VARCHAR(100),
    ->     author VARCHAR(100),
    ->     year INT,
    ->     price DECIMAL(10, 2)
    -> );
Query OK, 0 rows affected (0.029 sec)

mysql> 
mysql> INSERT INTO books VALUES(1, 'Мастер и Маргарита', 'Булгаков', 1967, 500.00);
Query OK, 1 row affected (0.006 sec)

mysql> INSERT INTO books VALUES(2, '1984', 'Оруэлл', 1949, 350.00);
Query OK, 1 row affected (0.001 sec)

mysql> INSERT INTO books VALUES(3, 'Маленький принц', 'Сент-Экзюпери', 1943, 280.00);
Query OK, 1 row affected (0.000 sec)

mysql> SELECT * FROM books;
+----+------------------------------------+---------------------------+------+--------+
| id | title                              | author                    | year | price  |
+----+------------------------------------+---------------------------+------+--------+
|  1 | Мастер и Маргарита                 | Булгаков                  | 1967 | 500.00 |
|  2 | 1984                               | Оруэлл                    | 1949 | 350.00 |
|  3 | Маленький принц                    | Сент-Экзюпери             | 1943 | 280.00 |
+----+------------------------------------+---------------------------+------+--------+
3 rows in set (0.001 sec)

mysql> SELECT title, author FROM books WHERE year > 1950;
+------------------------------------+------------------+
| title                              | author           |
+------------------------------------+------------------+
| Мастер и Маргарита                 | Булгаков         |
+------------------------------------+------------------+
1 row in set (0.001 sec)

mysql> UPDATE books
    -> SET price = 600.00
    -> WHERE id = 1;
Query OK, 1 row affected (0.003 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> 
mysql> DELETE FROM books
    -> WHERE id = 3;
Query OK, 1 row affected (0.002 sec)

mysql> SELECT * FROM `books`;
+----+------------------------------------+------------------+------+--------+
| id | title                              | author           | year | price  |
+----+------------------------------------+------------------+------+--------+
|  1 | Мастер и Маргарита                 | Булгаков         | 1967 | 600.00 |
|  2 | 1984                               | Оруэлл           | 1949 | 350.00 |
+----+------------------------------------+------------------+------+--------+
2 rows in set (0.001 sec)

mysql> 
