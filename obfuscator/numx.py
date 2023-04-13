def insert_(str, n=4):
    """Вставляет _ в длинные числа 0000_1010"""
    if n == 0:
        return str
    l = len(str)
    rstr = ''
    for i in range(0, l-n, n):
        rstr += str[i:i+n]
        rstr += '_'
    rstr += str[-n:]
    return rstr

def n_h(value, format='s', size=1, bo='little'):
    """Преобразует строковое представление value всех форматов в байты"""
    match format:
        case 's': 
            s = int(value)
            return s.to_bytes(size, bo, signed = True)
        case 'u': 
            u = int(value)
            return u.to_bytes(size, bo, signed = False)
        case 'b':
            b = int(value, 2)
            return b.to_bytes(size, bo, signed =True)
        case 'h':
            return bytes.fromhex(value)
        case 'i':
            return value.to_bytes(size, bo, signed = True)
        case 'ui':
            return value.to_bytes(size, bo, signed = False)

def h_a(hvalue, size = 1, bo='little', b_=4):
    """Преобразует байты в строковое представление для всех видов чисел"""
    h = hvalue.hex()
    u = int.from_bytes(hvalue, bo, signed=False)
    s = int.from_bytes(hvalue, bo, signed=True)
    b = format(u, '0>%sb'%(size*8))
    b = insert_(b, b_)
    return (h, u, s, b)

def h_s(hvalue, size = 1, bo='little', b_=4):
    """Вывод строкового представления"""
    husb = h_a(hvalue, size, bo, b_)
    return 'h_%s u_%s s_%s b_%s:'%(husb)

def n_s(value, format='i', size=1, bo='little', b_=4):
    """Получает другие представления данного числа"""
    hv = n_h(value, format, size, bo)
    return h_s(hv, size, bo, b_)

def b_i(bytes, from_ = -1, to = -1, bo='little', signed = True ):
    """Байты в int"""
    to = to if to > -1 else len(bytes)
    if to - (len(bytes) - from_) < 2:
        return int.from_bytes(bytearray(bytes[from_:to]), bo, signed= signed)
    return int.from_bytes(bytes[from_:to], bo, signed)

def b_u(bytes, from_ = -1, to = -1, bo='little'):
    """Байты в unsigned int"""
    return b_i(bytes, from_, to, bo, signed=False)