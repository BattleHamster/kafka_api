
def attempts(n=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('---------')
            print(n)
            func(*args, **kwargs)
            print('---------')
            return
        return wrapper
    return decorator


@attempts(n=5)
def my_print(name):
    print(f"Hello, {name}")

@attempts(n=4)
def my_print1(name):
    print(f"Hello, {name} 1")

@attempts(n=3)
def my_print2(name):
    print(f"Hello, {name} 2")

@attempts(n=2)
def my_print3(name):
    print(f"Hello, {name} 3")


my_print('Aaaa')
my_print1('Bbbb')
my_print2('Cccc')
my_print3('Dddd')

