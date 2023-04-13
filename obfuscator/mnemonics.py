from compiler import c, Inst, OFFS
from codeblock import CodeBlock
from mnem_data import mnemonics, jumps, loops, registers
import random
import re

class InstructionGenerator:

    def gen_prob(self):
        """Считает шанс появления инструкций"""
        probalities = []
        inc_instructions = []
        value = 0
        for m in mnemonics:

            # Если вероятность генерации инструкции выше 0
            if m[0] != 0:
                probalities.append(value + m[0])
                inc_instructions.append(m)
                value += m[0]
        return probalities, inc_instructions
    
    def __init__(self):
        self.c = c
        self.probs, self.insts = self.gen_prob()

    def random_bit(self, size):
        """Случайный бит для регистра указанной размерности"""
        max_bit = pow(2, 3 + size)
        return random.randrange(max_bit)

    def random_value(self, size):
        """Случайное число указанной размерности"""
        max_value = pow(256,size+1)-1
        return random.randrange(max_value)

    def check_size(self, min_size_char, max_size_char, size):
        """Содержит допустимый размер регистра"""
        min_size = 0
        match min_size_char:
            case 'b': min_size = 0
            case 'w': min_size = 1
            case 'd': min_size = 2
            case 'q': min_size = 3
            case 'x': min_size = 4
            case 'y': min_size = 5
            case 'z': min_size = 6
            case 'a': min_size = 0
            case _: min_size = 0
        max_size = 0
        match min_size_char:
            case 'b': max_size = 0
            case 'w': max_size = 1
            case 'd': max_size = 2
            case 'q': max_size = 3
            case 'x': max_size = 4
            case 'y': max_size = 5
            case 'z': max_size = 6
            case 'a': max_size = 6
            case _: max_size = 6
        return min(max(min_size, size), max_size)

    def parse_op(self, op, size):
        """Возвращает тип операнда и его размер"""
        optype, min_size, max_size = (list(op) + [None]*2)[:3]
        actual_size = self.check_size(min_size, max_size, size)
        return optype, actual_size

    def build_op(self, optype, size):
        """Создает операнд и адресацию к нему"""
        match optype:
                case "r": # Регистр
                    return random.choice(registers[size])
                case "i": # Число
                    return str(self.random_value(size))
                case "m": # Адрес в памяти
                    return '[' + random.choice(registers[2]) + ']' # 32bit 
                case "d": # Регистр следующей размерности
                    return random.choice(registers[size+1])
                case "g": # Регистр большей размерности
                    return random.choice(registers[size+1])
                case "l": # Номер бита
                    return str(self.random_bit(size))


    def make_args(self, args, size):
        """Определяет аргументы для инструкции"""
        if len(args) == 0:
            return ''
        operands = args.split()
        result = []

        for op in operands:
            optype, opsize = self.parse_op(op, size)
            result.append(self.build_op(optype, opsize))

        return ", ".join(result)

    def choose_inst(self):
        """Выбирает случайную инструкцию"""
        instruction = random.choices(self.insts, cum_weights=self.probs, k=1)[0]
        mnemonic = instruction[1]
        args = random.choice(instruction[2])
        return mnemonic, args

    def make_inst(self):
        """Создает инструкцию"""
        mnemonic, args = self.choose_inst()
        #print(str(args) + ' from ' + result)
        size = random.randrange(2)
        ops = self.make_args(args, size)
        instruction = Inst(mnemonic, ops)
        return self.c.asmu(instruction)

    def genb(self, size_cap):
        """Создает код длиной не больше size_cap байтов"""
        cur_size = 0
        insts = []
        while cur_size < size_cap:
            inst = self.make_inst()
            insts.append(inst)
            cur_size += len(inst.bytes)
        return CodeBlock(insts)
    
    def genc(self, count):
        """Создает код длиной count инструкций"""
        insts = []
        for i in range(count):
            inst = self.make_inst()
            insts.append(inst)
        return CodeBlock(insts)
    
    def gen_jmp(self, jump_type = 'jmp', where='<pos>', condition='none', op1=None, op2=None):
        """Создает инструкции прыжка"""
        insts = []
        match(condition):
            case 'cmp':
                inst = Inst('cmp', '%s, %s \n'%(op1, op2))
                inst = self.c.asmu(inst)
                insts.append(inst)
            case 'test':
                inst = Inst('test', '%s, %s \n'%(op1, op2))
                inst = self.c.asmu(inst)
                insts.append(inst)

        #op = '%s %s'%(compare, jump_type, where)
        #bytes, count = self.c.asm('%s %s %s'%(compare, jump_type, OFFS))
        inst = Inst(jump_type, 4)
        inst = self.c.asmu(inst)
        inst.ops = where
        insts.append(inst)
        return insts#(op_str, bytearray(bytes), count)
        
    
    def set_addr(self, cb, tar_addr, cur_addr = 0, def_offset = OFFS):
        """Обновляет адрес прыжка"""
        pattern = re.compile(r"<.{3}>") #r'\*<.{3}>\*' 
        #print(op_str)
        match = re.search(pattern, cb.code)[0]
        address = def_offset
        match(match):
            case '<rel>':
                pass
            case '<abs>':
                pass
            case '<pos>':
                print(cb.code)
                print(tar_addr)
                print(cur_addr)
                address = str(tar_addr-cur_addr) #'0x%s'%((address + tar_addr).to_bytes(4, 'big').hex())
                new_op_str = re.sub(match, address, cb.code)
                print(new_op_str)
                assert cb.code != new_op_str
                bytes, size = c.asm(new_op_str)
                cb.bytes = bytes
                cb.size = len(bytes)
                cb.code = new_op_str
                print('ta:%s ca:%s ta-ca:%s op_str:%s cb.b:%s'%(tar_addr, cur_addr, address, new_op_str, cb.bytes[-1]))

ig = InstructionGenerator()

# print (ig.make_inst())
# print (ig.make_inst())
# print (ig.make_inst())
# print (ig.make_inst())
# print (ig.make_inst())
# print (ig.make_inst())


