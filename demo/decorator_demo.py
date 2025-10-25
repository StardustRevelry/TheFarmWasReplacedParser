# 装饰器测试

def dec(func):
    def wrapper(*args, **kwargs):
        print("before")
        func(*args, **kwargs)
        print("after")
    return wrapper

def dec_with_arg(*args, **kwargs):
    text = ""
    for arg in args:
        text += arg + ", "
    for key, value in kwargs.items():
        text += str(key) + "=" + str(value) + ", "
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("decorator with arg: " + text)
            print("before")
            func(*args, **kwargs)
            print("after")
        return wrapper
    return decorator

@dec
def test():
    print("test")

@dec_with_arg("hello", "world", name="Alice", age=20)
def test_with_arg():
    print("test with arg")

print("===")
test()
print("===")
test_with_arg()