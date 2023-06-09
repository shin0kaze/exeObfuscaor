from random import randint, choice, randrange
#i - IMMediate - constant value
#b - BITs (length of previous operand in bits)
#r - REGister
#m - MEMory

global_size = (1,3)

def bound(value, borders):
    """Ограничивает число на отрезке"""
    return max(min(value, borders[1]),borders[0])

def add_tuple(a, b):
    return tuple(map(sum, zip(a, b)))

def intersect(borders1, borders2):
    """Находит пересечение двух отрезков"""
    return (max(borders1[0], borders2[0]), min(borders1[1], borders2[1]))

def mnem(mnemonic, operands = [], size=(1,3), ops_size=None):
    """Создает мнемонику, список комбинаций операндов сгрупированы в списки по их количеству"""
    return {'mnem': mnemonic, 'ops_list': operands, 'borders':intersect(global_size, size), 'ops_size':ops_size}

def get(mnem, ops_index=None, cur_size=None):
    """Возвращает название, размер, количество операндов, типы операндов, и 
    возможные комабинации для данного количества операндов"""
    if cur_size is None:
        cur_size = randint(*mnem['borders'])
    elif type(cur_size) is tuple:
        cur_size = randint(*intersect(cur_size, mnem['borders']))
    else:
        cur_size = bound(cur_size, mnem['borders'])
    
    ops = []
    cur_ops = ''
    count = 0

    if mnem['ops_list']:
        if ops_index is None:
            ops_index = randrange(0, len(mnem['ops_list']))
        ops = mnem['ops_list'][ops_index]
        cur_ops = choice(ops)
        count = len(cur_ops.split(' '))

    return {'mnem':mnem['mnem'], 'size':cur_size, 'ops_count':count, 'ops':cur_ops, 'combs':ops, 'ops_size':mnem['ops_size']}

def random_bit(size):
    """Случайный бит для регистра указанной размерности"""
    max_bit = pow(2, 3 + size)
    return randrange(max_bit)

def random_value(size):
    """Случайное число указанной размерности"""
    max_value = pow(256,size)-1
    return randrange(max_value)

if __name__ == "__main__":
    m1 = mnem('mov', operands=[['r m', 'r r', 'r i', 'm r']])
    m2 = mnem('imov', operands=[['r m', 'r r'],[ 'r r i']], size=(2,3))
    m3 = mnem('nop')
    print(get(m1))
    print(get(m1))
    print(get(m1))
    print(get(m2))
    print(get(m2))
    print(get(m2))
    print(get(m2))
    print(get(m3))