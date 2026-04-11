#1
check= lambda x: "положительное" if x > 0 else ("отрицательное" if x < 0 else "ноль")
print(check(5))
print(check(-3))
print(check(0))

#2
words= ["арбуз", "кот", "машина", "дом", "ананас"]
sorted_words= sorted(words, key=lambda w: (len(w), w[0]))
print(sorted_words)

#3
numbers= [5, 12, 7, 20, 33, 8]
evens= list(filter(lambda x: x%2 == 0 and x > 10, numbers))
print(evens)

#4
numbers= [1, 2, 3, 4, 5, 6]
result= list(map(lambda x: x**2 if x%2 == 0 else x*3, numbers))
print(result)

#5
compare= lambda a, b: "a больше" if a > b else ("b больше" if b > a else "равны")
print(compare(10, 7))
print(compare(3, 5))
print(compare(4, 4))

#6
numbers= [0, -3, 5, -7, 8]
result= [(lambda x: "положительное" if x > 0 else ("отрицательное" if x < 0 else "ноль"))(n) for n in numbers]
print(result)

#7
def even_numbers(n):
    for i in range(1, n+1):
        if i%2 == 0:
            if i%4 == 0:
                yield "кратно 4"
            else:
                yield i

for x in even_numbers(10):
    print(x)


    # 8
    def filter_words(words):
        for w in words:
            if len(w) > 4:
                if "а" in w:
                    yield "с а"
                else:
                    yield w


    words = ["кот", "машина", "арбуз", "дом"]
    for w in filter_words(words):
        print(w)


        # 9
        def infinite_numbers():
            i = 1
            while True:
                if i % 3 == 0:
                    yield "Fizz"
                elif i % 5 == 0:
                    yield "Buzz"
                elif i % 3 == 0 and i % 5 == 0:
                    yield "FizzBuzz"
                else:
                    yield i
                i += 1


        g = infinite_numbers()
        for _ in range(10):
            print(next(g))


            # 10
            def squares(n):
                for i in range(1, n + 1):
                    if i ** 2 % 2 == 0:
                        yield "чётный квадрат"
                    else:
                        yield i ** 2


            for x in squares(5):
                print(x)

                # 11
                even_squares = [x ** 2 for x in range(1, 21) if x % 2 == 0]
                print(even_squares)

                # 12
                from functools import reduce

                matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                result = [(lambda x: reduce(lambda a, b: a * b, x))(x) for x in matrix]
                print(result)

                # 13
                words = ["кот", "машина", "ананас", "дом"]
                result = [w for w in words if len(w) > 4 and "а" not in w]
                print(result)

                # 14
                numbers = [1, 2, 3, 4, 5]
                result = {n: "чётное" if n % 2 == 0 else "нечётное" for n in numbers}
                print(result)

                # 15
                matrix = [[1, 2], [3, 4], [5, 6]]
                result = [x for row in matrix for x in row]
                print(result)

                # 16
                numbers = list(range(1, 21))
                result = [
                    "FizzBuzz" if n % 3 == 0 and n % 5 == 0 else
                    "Fizz" if n % 3 == 0 else
                    "Buzz" if n % 5 == 0 else
                    n
                    for n in numbers
                ]
                print(result)


                # 17
                def is_prime(x):
                    if x < 2:
                        return False
                    for i in range(2, int(x ** 0.5) + 1):
                        if x % i == 0:
                            return False
                    return True


                def special_numbers(n):
                    for i in range(1, n + 1):
                        if i % 3 == 0 and i % 5 == 0:
                            yield "FizzBuzz"
                        elif i % 3 == 0:
                            yield "Fizz"
                        elif i % 5 == 0:
                            yield "Buzz"
                        elif is_prime(i):
                            yield "простое"
                        else:
                            yield i


                for x in special_numbers(15):
                    print(x)

                    # 18
                    words = ["кот", "машина", "арбуз", "дом", "ананас"]

                    process = lambda word: (
                            (word.upper() if len(word) > 4 else "short") + ("*" if "а" in word else "")
                    )

                    result = [process(w) for w in words]
                    print(result)


                    # 19
                    def process_numbers(numbers):
                        filtered = filter(lambda x: x >= 0, numbers)

                        for num in filtered:
                            transform = lambda x: x / 2 if x % 2 == 0 else x * 3 + 1
                            yield transform(num)


                    numbers = [5, -2, 8, 0, -7, 3]
                    for x in process_numbers(numbers):
                        print(x)

                        # 20
                        students = [("Иван", 85), ("Анна", 72), ("Пётр", 90), ("Мария", 60)]
                        grade_level = lambda x: (
                            "Отлично" if x >= 90
                            else "Хорошо" if x >= 70
                            else "Удовлетворительно"
                        )

                        result = {name: grade_level(score) for name, score in students}
                        print(result)


                        # 21
                        def matrix_transform(matrix):
                            for value in (item for row in matrix for item in row):
                                if value % 6 == 0:
                                    yield "кратно 6"
                                elif value % 2 == 0:
                                    yield "чётное"
                                elif value % 3 == 0:
                                    yield "кратно 3"
                                else:
                                    yield value


                        matrix = [
                            [1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]
                        ]

                        for x in matrix_transform(matrix):
                            print(x)

                            # 22
                            numbers = [1, 2, 3, 4, 5]
                            doubled = list(map(lambda x: x * 2, numbers))
                            print(doubled)

                            # 23
                            words = ["кот", "машина", "арбуз", "дом"]
                            result = list(map(lambda w: w.upper() + "!" if len(w) > 3 else w.upper(), words))
                            print(result)

                            # 24
                            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                            evens = list(filter(lambda x: x % 2 == 0, numbers))
                            print(evens)

                            # 25
                            numbers = [0, 5, 12, 7, 20, -3, 8]
                            result = list(
                                map(
                                    lambda x: x / 2 if x % 2 == 0 else x * 3,
                                    filter(lambda x: x > 5, numbers)
                                )
                            )

                            print(result)