from decorator_demo import dec
import decorator_demo

def __lambda_0(x):
    return x ** 2

def __lambda_1():
    return 1

def __lambda_2():
    return 2

def __lambda_3(x, y):
    return x + y

def __lambda_4():
    return 3.14159

def __lambda_5(x):

    def __lambda_17(y):
        return x + y
    return __lambda_17
square = __lambda_0
print(f'1. 单参数: {square(5)}')
import queue
x, y = (__lambda_1, __lambda_2)
print(f'2. 解包赋值: {x()}, {y()}')
add = __lambda_3
print(f'3. 多参数: {add(3, 7)}')
get_pi = __lambda_4
print(f'4. 常数: {get_pi()}')
x = '奇数' if True else '偶数'
print(f'5. 条件表达式: {x}')
f = __lambda_5
print(f'6. lambda 套娃: {f(3)(4)}')

def make_adder(n):

    def __lambda_7(x):
        return x + n

    def test():

        def __lambda_6():
            return print(n)
        return __lambda_6
    test()
    return __lambda_7
add_3 = make_adder(3)
print(f'7. lambda + closure: {add_3(4)}')
print('8. lambda + for 循环:')
for i in range(10):
    if i % 2 == 0:

        def __lambda_8():
            return print(i)
        var = __lambda_8
    else:

        def __lambda_9():
            return print(i)
        a = __lambda_9
        a()
else:

    def __lambda_10():
        return print('else block')
    a = __lambda_10
    a()
print('end of 8.')
i = 1
if i % 3 == 0:

    def __lambda_11():
        return print(i)
    a = __lambda_11
    a()
elif i % 2 == 0:

    def __lambda_12():
        return print(i)
    a = __lambda_12
    a()
else:

    def __lambda_13():
        return print(i)
    a = __lambda_13
print('9. lambda + match case 语句:')
match i:
    case 0:

        def __lambda_14():
            return print(i)
        a = __lambda_14
        a()
    case 1:

        def __lambda_15():
            return print(i)
        a = __lambda_15
        a()
    case _:

        def __lambda_16():
            return print(i)
        a = __lambda_16
        a()