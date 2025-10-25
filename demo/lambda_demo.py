from decorator_demo import dec
import decorator_demo

square = lambda x: x ** 2
print(f"1. 单参数: {square(5)}")

import queue

x, y = lambda: 1, lambda: 2
print(f"2. 解包赋值: {x()}, {y()}")

add = lambda x, y: x + y
print(f"3. 多参数: {add(3, 7)}")

get_pi = lambda: 3.14159
print(f"4. 常数: {get_pi()}")

# 尚不支持
# l = [i for i in range(10) if i % 2 == 0]
# print(f"4. 列表推导式: {l}")

x = "奇数" if True else "偶数"
print(f"5. 条件表达式: {x}")  # 输出: 奇数

# lambda 套娃
f = lambda x: lambda y: x + y
print(f"6. lambda 套娃: {f(3)(4)}")  # 输出: 7

# lambda + closure
def make_adder(n):
    def test():
        return lambda : print(n)
    test()
    return lambda x: x + n

add_3 = make_adder(3)
print(f"7. lambda + closure: {add_3(4)}")  # 输出: 7

# lambda + for 循环
print("8. lambda + for 循环:")
for i in range(10):
    if i % 2 == 0:
        var = lambda: print(i)
    else:
        a = lambda: print(i)
        a()
else:
    a = lambda: print("else block")
    a()
print("end of 8.")

# lambda + if 条件语句, 含 elif
i = 1
if i % 3 == 0:
    a = lambda: print(i)
    a()
elif i % 2 == 0:
    a = lambda: print(i)
    a()
else:
    a = lambda: print(i)

# lambda + match case 语句
print("9. lambda + match case 语句:")
match i:
    case 0:
        a = lambda: print(i)
        a()
    case 1:
        a = lambda: print(i)
        a()
    case _:
        a = lambda: print(i)
        a()
