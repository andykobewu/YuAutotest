def log(func):
    def wrapper(*args, **kw):
        print("Call %s():" %func.__name__)
        return func(*args, **kw)
    return wrapper
@log
def now():
	print('===========')

if __name__ == '__main__':
    now()