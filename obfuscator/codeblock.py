from llist import Node

class CodeBlock(Node):
    """Класс, который отвечаеет за хранение кода в списке"""

    def __init__(self, insts, next_code=None, has_jump=False, cb_id = None, *args, **kw):
        # Ссылка на Codeblock, который должен исполняться следующим
        # Либо следующий блок должен быть следующим в списке,
        # либо иметь прыжок, что бы добраться до следующего блока
        # Иначе нарушится ход исполнения программы
        self.next_code = next_code
        # Скомпилированные байты
        self.bytes = bytearray()
        # Текстовое представление кода
        self.code = ''
        # Имеет ли данный код инструкцию прыжка, для которой нужно
        # вычислять адрес
        self.has_jump = has_jump
        # Адрес данного Codeblock. addr = sum(all_prev_CB.size)
        self.addr = 0

        if not (type(insts) is list):
            insts = [insts]
        #print(insts)
        for i in insts:
            #print(i)
            self.code += i.c
            self.bytes.extend(i.bytes)
            #print(i.bytes)
        #print(self.bytes)
        # Размер данного Codeblock.
        self.size = len(self.bytes)
        # Поскольку наследуется от Node, имеет следующие свойства: 
        # value = bytes, prev и next предыдущий и следующий Codebock в списке
        self.cb_id = cb_id
        self.used_regs = []
        super().__init__(len(self.bytes), *args, **kw)

    @classmethod
    def chain(that, prev, insts, next_code=None, has_jump=False, cb_id = None, *args, **kw):
        cb = CodeBlock(insts, next_code=None, has_jump=False, cb_id=cb_id, *args, **kw)
        prev.next_code = cb
        return cb

    def set_bytes(self, bytes):
        self.bytes = bytes
        self.size = len(bytes)

    b = property(fset=set_bytes)

    def is_need_to_calc_addr(self):
        """Определяет необходимость вычисления адреса"""
        # Имеет прыжок, вычислеение адрееса необходимо
        if self.has_jump:
            return 1
        # Нет прыжка, и следующий блок тот, который должен исполнятся следующим
        if self.next_code == self.next:
            return 0
        # Нет прыжка, и следующий блок не является следуующим по исполнению
        return -1
    
    def insertcf(self, prev):
        """Вставляет данный блок в поток кода"""
        if prev:
            self.next_code = prev.next_code
            prev.next_code = self
    
    def __str__(self):    
        return "cb: " + self.code
    
    
        