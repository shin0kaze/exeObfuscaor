from compiler import c, Inst, OFFS, KsError
from codeblock import CodeBlock
from mnemData import gen_probs, choice_reg, choose_inst, ptr
from mnemonic import random_bit, random_value
import random
import re
import logging

def randbool():
    return bool(random.getrandbits(1))

def random_val_or_reg(size):
    if randbool():
        return random_value(size)
    return choice_reg(size)
    

class InstructionGenerator:
    
    def __init__(self):
        self.c = c
        self.probs, self.insts = gen_probs()

    def build_op(self, optype, size):
        """Создает операнд и адресацию к нему"""
        match optype:
                case 'r': # Регистр
                    return choice_reg(size)
                case 'i': # Число
                    return str(random_value(size))
                case 'm': # Адрес в памяти
                    return '%s ptr [%s]'%(ptr(size),str(random_val_or_reg(size))) # 32bit 
                case 'l': # Номер бита
                    return str(random_bit(size))
                case 'b': # 1 Байт
                    return str(random_value(1))
                case 'a': # 32bit Адрес
                    return '%s ptr [%s]'%(ptr(min(size, 2)),str(random_val_or_reg(size)))
                case _:
                    raise Exception('Non-existent operand')


    def make_args(self, ops, size, ops_size = None):
        """Определяет аргументы для инструкции"""
        if len(ops) == 0:
            return ''

        result = []
        if ops_size:
            for op, op_size in zip(ops.split(' '), ops_size):
                result.append(self.build_op(op, size+op_size))
        else:
            for op in ops.split(' '):
                print('%s:%s'%(op, size))
                result.append(self.build_op(op, size))
                print(result[-1])

        return ", ".join(result)

    def make_inst(self):
        """Создает инструкцию"""
        mnem_data = choose_inst(self.insts, self.probs)
        #print(str(args) + ' from ' + result)
        ops = self.make_args(mnem_data['ops'], mnem_data['size'], mnem_data['ops_size'])
        instruction = Inst(mnem_data['mnem'], ops)
        try:
            instruction_updated = self.c.asmu(instruction)
        except KsError as ex:
            logging.error('KsError:%s'%(ex), exc_info=True)
        return instruction_updated

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

if __name__ == "__main__":
    while True:
        print (ig.make_inst())
    print (ig.make_inst())
    print (ig.make_inst())
    print (ig.make_inst())
    print (ig.make_inst())
    print (ig.make_inst())


