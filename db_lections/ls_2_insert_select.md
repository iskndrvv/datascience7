"""================= INSERT ================="""
команда используется для добавления данных
относится к классу DML

структура Insert:
    1) если мы хотим заполнит частично, то указываем название колонок которые надо заполнить 
    INSERT INTO <name of table> (name_column1, name_column2) 
    VALUE (value1, value2);
    пример:
        INSERT INTO students (id, name, age, email)
        -> VALUE (3, 'aiba', 20, 'aibo123@gmail.com');


    2) если надо заполнить все поля 
    INSERT INTO <name of table> 
    VALUE (value1, value2;)
    пример:
        INSERT INTO students 
        -> VALUES (4, 'sam', 21, 'samcosmo@gmail.com', '2003-05-15');

    3) добавление нескольких данных одновременно
    INSERT INTO <name of table> (name_column1, name_column2) 
    VALUE (value1, value2), (value3, value4)
    пример:
        insert into students(id, name, age, email)
        -> values(5, 'nurs', 27, 'nursturs@gmail.com'),
        -> (6, 'emir', 23, 'emkatop@gmail.com');


# типичные ошибки при INSERT
1) колонки не совпадают с кол-во значений
пример:
    INSERT INTO students 
    -> VALUE (4, 'sam', 21, 'samcosmo@gmail.com');
    ERROR 1136 (21S01): Column count doesn't match value count at row 1
2) дубликаты PRIMARY KEY(id)
    INSERT INTO students (id, name, age, email) VALUE (7, 'Almaz', 30, 'almaz@gmail.com');
    ERROR 1062 (23000): Duplicate entry '7' for key 'students.PRIMARY'

3) неправильные типы данных 
    INSERT INTO students VALUE (8, 'Almaz', 'almaz@gmail.com', 30);
    ERROR 1366 (HY000): Incorrect integer value: 'almaz@gmail.com' for column 'age' at row 1
    INCORECT <data type> value: ......




"""================= SELECT ================="""
команда для получения данных 
1) получение всех данных
SELECT * FROM <table name>;
2) получение одной колонки:
SELECT <name of column> FROM <table name>;
пример:
    SELECT name FROM students;
    +------+
    | name |
    +------+
    | aza  |
    | aza  |
    | aiba |
    | sam  |
    | nurs |
    | emir |
    +------+

3) получени енескольких колонок 
SELECT <name of column1>, <name of column2> FROM <table name>;
пример:
    select name, age, id from students;
    +------+------+----+
    | name | age  | id |
    +------+------+----+
    | aza  |   22 |  1 |
    | aza  |   22 |  2 |
    | aiba |   20 |  3 |
    | sam  |   21 |  4 |
    | nurs |   27 |  5 |
    | emir |   23 |  6 |
    +------+------+----+




"""================= фильтрация ================="""
WHERE - фильтрует строки(объекты) по условию
структура:
    SELECT column_name/* FROM <table name>
    WHERE <condition>;
пример:
    SELECT * FROM students WHERE age > 20;
    +----+------+------+--------------------+------------+
    | id | name | age  | email              | birth_day  |
    +----+------+------+--------------------+------------+
    |  1 | aza  |   22 | aza@gmail.com      | 2002-11-11 |
    |  2 | aza  |   22 | aza@gmail.com      | 2003-11-11 |
    |  4 | sam  |   21 | samcosmo@gmail.com | 2003-05-15 |
    |  5 | nurs |   27 | nursturs@gmail.com | NULL       |
    |  6 | emir |   23 | emkatop@gmail.com  | NULL       |
    +----+------+------+--------------------+------------+

# основные операторы
1) = -> равно
2) != -> не равно
3) > -> больше 
4) < -> меньше
5) >= -> больше или равно
6) <= -> меньше или равно

# фильтрация строк столбцов
    SELECT * FROM <table name> WHERE <str column> = <target>
пример:
    SELECT * FROM students WHERE name = 'aza';
    +----+------+------+---------------+------------+
    | id | name | age  | email         | birth_day  |
    +----+------+------+---------------+------------+
    |  1 | aza  |   22 | aza@gmail.com | 2002-11-11 |
    |  2 | aza  |   22 | aza@gmail.com | 2003-11-11 |
    +----+------+------+---------------+------------+

# практика
1) создать таблицу менторов (id, name, salary, phone, email)
2) записать с помощью множественного добавления как минимум 5 данных 
3) провести фильтрацию salary
4) фильтр по строчным данным



