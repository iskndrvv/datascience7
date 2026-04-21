# Задача 1 — Статистика списка
# Напишите функцию stats(lst), которая принимает список чисел и возвращает словарь
# с минимумом, максимумом, средним и суммой.
# Пример:
# >>> stats([10, 20, 30, 40, 50])
# {'min': 10, 'max': 50, 'avg': 30.0, 'sum': 150}
 
# >>> stats([5])
# {'min': 5, 'max': 5, 'avg': 5.0, 'sum': 5}
 
# >>> stats([])
# {'min': None, 'max': None, 'avg': None, 'sum': 0}

print('\n\t======== zadacha 1 ========\n')

nums = [10, 20, 40, 80, 160, 320]

def stats(lst):
    if lst == []:
        return {'min': None, 'max': None, 'avg': None, 'sum': 0}
    
    return {
        'min': min(lst),
        'max': max(lst),
        'avg': sum(lst) / len(lst),
        'sum': sum(lst)
    }

print(stats(nums))


# Задача 2 — Подсчёт слов 
# Напишите функцию count_words(text), которая принимает строку и возвращает словарь, где ключ 
# слово (в нижнем регистре), значение — сколько раз оно встречается. Знаки препинания убрать.
# Пример:
# >>> count_words("Привет мир привет Python мир мир")
# {'привет': 2, 'мир': 3, 'python': 1}
 
# >>> count_words("Hello, hello! HELLO.")
# {'hello': 3}




print('\n\t======== zadacha 2 ========\n')

def count_words(text):
    text = text.lower()
    
    for znak in ",.!?:;'":
        text = text.replace(znak, "")
    
    words = text.split()
    result = {}

    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    
    return result

print(count_words("Привет мир привет Python мир мир"))
print(count_words("Hello, hello! HELLO."))
print(count_words("меня з!овут аза. приятно познакомиться меня зовут, но вы можете зовут аза"))




# Задача 3 — Калькулятор
# Напишите программу-калькулятор. Пользователь вводит два числа и операцию (+, -, *, /). Программа выводит результат
# При делении на ноль — сообщение об ошибке.
# Пример:

# Первое число: 10
# Второе число: 3
# Операция (+, -, *, /): /
# Результат: 10 / 3 = 3.3333
 
# Первое число: 5
# Второе число: 0
# Операция (+, -, *, /): /
# Ошибка: деление на ноль
 
# Первое число: 7
# Второе число: 3
# Операция (+, -, *, /): %
# Ошибка: неизвестная операция




print('\n\t======== zadacha 3 ========\n')

while True:
    print('if u wanna exit type "exit"')
    a = input("first num: ")

    if a == "exit":
        break
    try:
        a = int(a)
    
    except ValueError:
        print("ошибка: нужно ввести число")
        continue

    print('if u wanna exit type "exit"')
    znak = input("знак (+, -, *, /): ")
    if znak == exit:
        break
    print('if u wanna exit type "exit"')

    b = input("second num: ")

    if b == "exit":
        break

    try:
        
        b = int(b)
    except ValueError:
        print("ошибка: нужно ввести число")
        continue

    if znak == "+":
        print(f"result: {a} + {b} = {a + b}")
    elif znak == "-":
        print(f"result: {a} - {b} = {a - b}")
    elif znak == "*":
        print(f"result: {a} * {b} = {a * b}")
    elif znak == "/":
        if b == 0:
            print("ne deli na 0, nas jdet collapse")
        else:
            print(f"result: {a} / {b} = {a / b}")
    else:
        print("bro, tolko +, -, *, /")


# Задача 4 — Определитель сезона
# Напишите функцию season(month), которая принимает номер месяца (1–12) и возвращает название сезона. При неверном вводе вернуть "Неверный месяц".
# Пример:
# >>> season(1)   # "Зима"
# >>> season(4)   # "Весна"
# >>> season(7)   # "Лето"
# >>> season(10)  # "Осень"
# >>> season(13)  # "Неверный месяц"



print('\n\t======== zadacha 4 ========\n')

def season(month):
    if month == 12 or month == 1 or month == 2:
        return "zima"
    elif month == 3 or month == 4 or month == 5:
        return "vesna"
    elif month == 6 or month == 7 or month == 8:
        return "leto"
    elif month == 9 or month == 10 or month == 11:
        return "osen'"
    else:
        return "net takogo mesyaca"


print(season(1))
print(season(10))
print(season(99))


# Задача 5 — Безопасный ввод
# Напишите функцию safe_input(prompt, type_func), которая запрашивает ввод у пользователя 
# и пытается преобразовать к нужному типу. Если не получается — просит ввести заново (максимум 3 попытки). 
# Возвращает значение или None.

# Пример:
# >>> age = safe_input("Введите возраст: ", int)
# Введите возраст: abc
# Ошибка! Попробуйте ещё раз.
# Введите возраст: 25.5
# Ошибка! Попробуйте ещё раз.
# Введите возраст: 25
# >>> print(age)  # 25
 
# # Если 3 раза неверно:
# >>> val = safe_input("Число: ", float)
# Число: abc
# Ошибка! Попробуйте ещё раз.
# Число: xyz
# Ошибка! Попробуйте ещё раз.
# Число: !!!
# Ошибка! Попробуйте ещё раз.
# >>> print(val)  # None



print('\n\t======== zadacha 5 ========\n')


def safe_input(prompt, type_func):
    for i in range(3):
        value = input(prompt)
        try:
            return type_func(value)
        except ValueError:
            print("Ошибка! Попробуйте ещё раз.")
    return None


age = safe_input("Введите возраст: ", int)
print(age)

val = safe_input("Число: ", float)
print(val)


# Задача 6 — Чтение списка из строки
# Напишите функцию parse_numbers(text), которая принимает строку с числами через запятую и возвращает список чисел. 
# Нечисловые значения пропускаются, но добавляются в список ошибок. Функция возвращает кортеж (numbers, errors).
# Пример:
# >>> parse_numbers("1, 2, abc, 3.5, , xyz, 10")
# ([1.0, 2.0, 3.5, 10.0], ["abc", "xyz"])
 
# >>> parse_numbers("10, 20, 30")
# ([10.0, 20.0, 30.0], [])



print('\n\t======== zadacha 6 ========\n')

def parse_numbers(text):
    parts = text.split(",")
    numbers = []
    errors = []

    for item in parts:
        item = item.strip()

        if item == "":
            continue

        try:
            numbers.append(float(item))
        except ValueError:
            errors.append(item)

    return numbers, errors


print(parse_numbers("1, 2, abc, 3.5, , xyz, 10, 80, eowuieuowijfe,, weather , . , name, world"))



# Задача 7 — Генератор пароля
# Напишите функцию generate_password(length=8, use_digits=True, use_special=False), которая генерирует случайный пароль.
# Пример:
# >>> generate_password()
# 'kQm3nP8x'          # 8 символов, буквы + цифры
 
# >>> generate_password(12, use_special=True)
# 'aB3$kM9!pLx2'      # 12 символов, буквы + цифры + спецсимволы
 
# >>> generate_password(6, use_digits=False)
# 'kQmBnP'            # 6 символов, только буквы

print('\n\t======== zadacha 7 ========\n')

import random

def generate_password(length=8, use_digits=True, use_special=False):
    chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

    if use_digits:
        chars += "1234567890"

    if use_special:
        chars += "!@#$%^&*()_+-=<>?/"

    password = ""

    for i in range(length):
        password += random.choice(chars)

    return password


print(generate_password())
print(generate_password(12, use_special=True))
print(generate_password(6, use_digits=False))


# Задача 8 — Применить функцию к списку
# Напишите функцию apply_to_each(lst, func), которая применяет функцию func к каждому элементу списка и возвращает новый список. Затем используйте её с разными функциями.
# Пример:
# >>> apply_to_each([1, 4, 9, 16], lambda x: x ** 0.5)
# [1.0, 2.0, 3.0, 4.0]
 
# >>> apply_to_each(["hello", "world"], str.upper)
# ['HELLO', 'WORLD']
 
# >>> apply_to_each([1, 2, 3], lambda x: x * 2)
# [2, 4, 6]


print('\n\t======== zadacha 8 ========\n')


def apply_to_each(lst, func):
    result = []

    for item in lst:
        result.append(func(item))

    return result


print(apply_to_each([1, 4, 9, 16], lambda x: x ** 0.5))
print(apply_to_each(["hello", "world"], str.upper))
print(apply_to_each([1, 2, 3], lambda x: x * 2))


# Задача 9 — Сумма вложенного списка
# Напишите рекурсивную функцию nested_sum(lst), которая считает сумму всех чисел во вложенном списке любой глубины.
# Пример:
# >>> nested_sum([1, 2, [3, 4], [5, [6, 7]]])
# 28
 
# >>> nested_sum([1, [2, [3, [4, [5]]]]])
# 15
 
# >>> nested_sum([])
# 0



print('\n\t======== zadacha 9 ========\n')

def nested_sum(lst):
    total = 0

    for item in lst:
        if type(item) == list:
            total += nested_sum(item)
        else:
            total += item

    return total


print(nested_sum([1, 2, [3, 4], [5, [6, 7]]]))
print(nested_sum([1, [2, [3, [4, [5]]]]]))
print(nested_sum([]))


# Задача 10 — Палиндром рекурсивно
# Напишите рекурсивную функцию is_palindrome(s), которая проверяет, является ли строка палиндромом. Игнорировать пробелы и регистр.
# Пример:
# >>> is_palindrome("шалаш")
# True
 
# >>> is_palindrome("А роза упала на лапу Азора")
# True
 
# >>> is_palindrome("hello")
# False

print('\n\t======== zadacha 10 ========\n')


def is_palindrome(s):
    s = s.replace(" ", "").lower()

    if len(s) <= 1:
        return True

    if s[0] != s[-1]:
        return False

    return is_palindrome(s[1:-1])


print(is_palindrome("шалаш"))
print(is_palindrome("lol who r u?"))
print(is_palindrome("hello"))


# Задача 11 — Таймер
# Напишите декоратор @timer, который измеряет и печатает время выполнения функции.
# Пример:
# import time
 
# @timer
# def slow_function():
#     time.sleep(1)
#     return "done"
 
# >>> slow_function()
# slow_function выполнилась за 1.0012 сек.
# 'done'

print('\n\t======== zadacha 11 ========\n')

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} выполнилась за {end - start:.4f} сек.")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "done"


print(slow_function())


12
print('\n\t======== zadacha 12 ========\n')

def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper

@count_calls
def say_hello(name):
    return f"Привет, {name}!"


print(say_hello("Аня"))
print(say_hello("Боб"))
print(say_hello("Чарли"))
print(say_hello.call_count)




13

print('\n\t======== zadacha 13 ========\n')


def make_counter(start=0):
    count = start

    def counter():
        nonlocal count
        current = count
        count += 1
        return current

    return counter


counter = make_counter()
print(counter())
print(counter())
print(counter())

c2 = make_counter(10)
print(c2())
print(c2())

print(counter())
print(c2())


14

print('\n\t======== zadacha 14 ========\n')

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        if len(self.grades) == 0:
            return 0
        return round(sum(self.grades) / len(self.grades), 2)

    def __str__(self):
        return f"Студент {self.name}, средний балл: {self.average():.2f}"


s = Student("Аня")
s.add_grade(5)
s.add_grade(4)
s.add_grade(5)

print(s.average())
print(s)


15


print('\n\t======== zadacha 15 ========\n')

import math

class Shape:
    def area(self):
        return 0


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return round(math.pi * self.radius ** 2, 2)

    def __str__(self):
        return f"Круг(r={self.radius})"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"Прямоугольник({self.width}x{self.height})"


def total_area(shapes):
    total = 0
    for shape in shapes:
        total += shape.area()
    return round(total, 2)


c = Circle(5)
r = Rectangle(3, 4)

print(c.area())
print(r.area())
print(total_area([c, r]))
print(c)
print(r)



16

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Нельзя сложить {self.currency} и {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __gt__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Нельзя сравнить {self.currency} и {other.currency}")
        return self.amount > other.amount

    def __str__(self):
        return f"{self.amount} {self.currency}"


a = Money(100, "USD")
b = Money(50, "USD")

print(a + b)
print(a > b)
print(a == Money(100, "USD"))

c = Money(200, "EUR")
