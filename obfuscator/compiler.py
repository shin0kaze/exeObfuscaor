from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_MODE_32, CsError
from keystone import Ks, KS_ARCH_X86, KS_MODE_64, KS_MODE_32

F32 = 0xffff_ffff
OFFS = 0x0040_0000

class Inst():
    """Класс хранящий 1 дизассемблированную инструкцию"""
    def __init__(self, mnemonic=None, ops=None, bytes=None): #, size=None, addr=None, id=None
        self.mnem = mnemonic
        self.ops = ops
        self.bytes = bytes
        # self.size = size if size else len(bytes) if bytes else None
        # self.addr = addr
        # self.csid = id
    
    def get_inst(self):
        return '\t%s %s\t%s' % ( self.mnem, self.ops, self.bytes)
        #return '%s\t0x%x:\t%s %s\t%s\t%s' % (self.csid, self.addr, self.mnem, self.ops, self.size, self.bytes)

    def __str__(self):    
        return '%s %s' % (self.mnem, self.ops)
    
    def code(self):
        return '%s %s\n' % (self.mnem, self.ops)

    i = property(get_inst)
    c = property(code)

class Compiler(object):
    """Обращается к Keystone и Capstone что бы получить код"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Compiler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.ks = Ks(KS_ARCH_X86, KS_MODE_32)
        self.cs = Cs(CS_ARCH_X86, CS_MODE_32)
        self.cs.detail = False

    def asm(self, op_str):
        """Компилирует код, что бы получить байты"""
        bytes, size = self.ks.asm(op_str)
        return bytearray(bytes), size
    
    def asmi(self, op_str, mnemonic = None, ops = None):
        """Компилирует код, что бы получить Instruction"""
        bytes, size = self.ks.asm(op_str)
        return Inst(mnemonic, ops, bytes) # size

    def asmu(self, inst):
        """Компилирует изменения в Instruction"""
        bytes, size = self.ks.asm(str(inst))
        inst.bytes = bytes
        # inst.size = size
        return inst

    def disasm(self, bytes, eoc=b'\00\00', offset=0x0):
        """Декомпилирует код, пока не встретит конец инструкций"""
        instructions = []
        for i in self.cs.disasm(bytes, offset): 
            if i.bytes == eoc:
                return instructions
            instructions.append(Inst(i.mnemonic, i.op_str, i.bytes)) # i.size, i.address, i.id
            #print("%s::%s::%s"%(i.mnemonic, i.op_str, i.bytes))
        return instructions
    
    def disi(self, bytes, offset=0x0):
        """Декомпилирует набор байтов, что бы получить Instruction"""
        i = next(self.cs.disasm(bytes, offset))
        return Inst(i.mnemonic, i.op_str, i.bytes) # , i.size, i.address, i.id
    
    def asmdis(self, op_str, eoc=b'\00\00', offset=0x0):
        """Компилирует код, и сразу же разбирает на Instructions"""
        return self.disasm(self.asm(op_str), eoc, offset)

    def asmdis1(self, op_str, eoc=b'\00\00', offset=0x0):
        """Компилирует код, и сразу же создает Instruction"""
        return self.disi(self.asm(op_str), eoc, offset)

c = Compiler()
