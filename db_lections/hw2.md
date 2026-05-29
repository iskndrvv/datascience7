mysql> CREATE TABLE courses (
    -> id INT PRIMARY KEY,
    -> course_name VARCHAR(100),
    -> price DECIMAL(10,2),
    -> mentor_id INT
    -> );
Query OK, 0 rows affected (0.398 sec)

mysql> INSERT INTO courses(id, course_name, price, mentor_id)
    -> VALUES
    -> (1, 'Аналитика данных', 15000.00, 100),
    -> (2, 'QA тестировщик', 8200.00, 101),
    -> (3, 'Python для начинающих', 20000.00, 102),
    -> (4, 'SQL тренажер', 3600.00, 103),
    -> (5, 'Fronted разработка', 12800.00, 100),
    -> (8, 'QA тестировщик: Продвинутый уровень', 10200.00, 102),
    -> (10, 'Английский для IT-специалистов', 5000.00, 103),
    -> (20, 'Fullstack-разработчик (Индивидуально)', 50000.00, 100);
Query OK, 8 rows affected (0.139 sec)
Records: 8  Duplicates: 0  Warnings: 0

mysql> WITH expensive_courses AS (
    -> SELECT * FROM courses WHERE price > 15000
    -> )
    -> SELECT * FROM expensive_courses;
+----+---------------------------------------+----------+-----------+
| id | course_name                           | price    | mentor_id |
+----+---------------------------------------+----------+-----------+
|  3 | Python для начинающих                 | 20000.00 |       102 |
| 20 | Fullstack-разработчик (Индивидуально) | 50000.00 |       100 |
+----+---------------------------------------+----------+-----------+
2 rows in set (0.060 sec)

mysql> WITH avarage_cost AS (
    -> SELECT AVG(price) AS avg_price FROM courses
    -> )
    -> SELECT * FROM avarage_cost;
+--------------+
| avg_price    |
+--------------+
| 15600.000000 |
+--------------+
1 row in set (0.020 sec)

mysql> WITH max_price AS (
    -> SELECT MAX(price) AS maxPrice FROM courses
    -> )
    -> SELECT * FROM max_price;
+----------+
| maxPrice |
+----------+
| 50000.00 |
+----------+
1 row in set (0.024 sec)

mysql> WITH min_price AS (
    -> SELECT MIN(price) AS minPrice FROM courses
    -> )
    -> SELECT * FROM min_price;
+----------+
| minPrice |
+----------+
|  3600.00 |
+----------+
1 row in set (0.016 sec)

mysql> WITH mentor_courses AS (
    -> SELECT * FROM courses WHERE mentor_id = 101
    -> )
    -> SELECT * FROM mentor_courses;
+----+----------------+---------+-----------+
| id | course_name    | price   | mentor_id |
+----+----------------+---------+-----------+
|  2 | QA тестировщик |  8200.00 |       101 |
+----+----------------+---------+-----------+
1 row in set (0.006 sec)