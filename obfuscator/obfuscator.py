from llist import LList
from codeblock import CodeBlock
from instGenerator import ig
from numx import *
import random
import logger as lg

class Obfuscator:

    def split_insts_on_inst_groups(self, code_list, min=3, max=6):
        """Объединяет инструкции в небольшие группы кода"""
        code_groups = []
        index = 0
        while index < len(code_list):
            length = random.randrange(min, max)
            code_group = code_list[index:index+length]
            code_groups.append(code_group)
            index += length

        return code_groups

    def make_llist_of_codeblocks(self, inst_groups):
        """Создаем список представляющий код программы"""
        llist_codeblocks = LList()
        prev_cb = CodeBlock(inst_groups[0], cb_id="0")
        llist_codeblocks.addn(prev_cb)
        id = 1
        for inst_group in inst_groups[1:]:
            cb = CodeBlock.chain(prev = prev_cb, insts = inst_group, cb_id=str(id))
            llist_codeblocks.addn(cb)
            prev_cb = cb
            id+=1

        # Устанавливает свойство entry_point, которое всегда указывает на
        # первый исполняющийся блок, независимо от его расположения в списке.
        llist_codeblocks.entry_point = llist_codeblocks.head
        return llist_codeblocks

    def __init__(self, code_list) -> None:
        cg = self.split_insts_on_inst_groups(code_list)
        self.llist_cb = self.make_llist_of_codeblocks(cg)

    def add_jumps(self):
        """Добавляет прыжки в код"""
        for cb in self.llist_cb.forwardn():
            if cb.next_code and not cb.has_jump:
                insts = ig.gen_jmp()
                jump_cb = CodeBlock(insts)
                jump_cb.next_code = cb.next_code
                jump_cb.has_jump = True
                jump_cb.cb_id = cb.cb_id + ".0j"
                cb.next_code = jump_cb
                self.llist_cb.ins(cb, jump_cb)

    def add_garbage(self):
        """Добавляет мусор в код"""
        for cb in self.llist_cb.backwardn():
            if cb.has_jump:
                garbage_cb = ig.genb(10)
                self.llist_cb.ins(cb, garbage_cb)

    def print_cb(self):
        """Выводим Codeblocks в консоль"""
        for cb in self.llist_cb.forwardn():
            next_addr = cb.next_code.addr if cb.next_code else 'empty'
            lg.debug("%s has addr:%s and size:%s and next:%s, has_jump:%s, bytes:%s"% (cb.cb_id, cb.addr, cb.size, next_addr, cb.is_need_to_calc_addr(), cb.bytes))
            if cb.is_need_to_calc_addr():
                lg.debug(cb.code)
                assert cb.code != 'jmp <pos>\n', 'JMP POS'

    def print_cbcf(self):
        """Выводим указатели"""
        for cb in self.llist_cb.forwardn():
            next_cb_id = cb.next_code.cb_id if cb.next_code else 'none'
            to = ''
            if cb.is_need_to_calc_addr():
                next_ca = cb.next_code.addr if cb.next_code else 'none'
                diff = n_s(value=int(next_ca) - cb.addr, size=4) if next_ca != 'none' else 'nan'
                lb = cb.bytes[-1]
                to = "lb:%s, ta:%s, ca:%s, ta-ca:%s"%(n_s(lb, 'ui'), next_ca, cb.addr, diff)
            lg.debug("cb:%s -> cb:%s, %s"%(cb.cb_id, next_cb_id, to))

    def calculate_addr_of_blocks(self):
        """Подсчет адресов"""
        prev_cb_addr = 0
        for cb in self.llist_cb.forwardn():
            cb.addr = prev_cb_addr
            prev_cb_addr += cb.size

    def calculate_jump_addr(self):
        """вычисление адреса прыжков"""
        for cb in self.llist_cb.forwardn():
            if cb.is_need_to_calc_addr() > 0:
                if (tar_addr := cb.next_code.addr) is not None:
                    cb.old_code = ''.join(cb.code)
                    cb.next_addr = cb.next.addr
                    ig.set_addr(cb, tar_addr, cb.addr)

        for cb in self.llist_cb.forwardn():
            if cb.is_need_to_calc_addr() > 0:
                if (tar_addr := cb.next_code.addr) is not None:
                    cb.code = ''.join(cb.old_code)
                    ig.set_addr(cb, tar_addr, cb.addr)
                    pass

    def calculate_jump_addr2(self):
        """вычисление адреса прыжков"""
        for cb in self.llist_cb.forwardn():
            if cb.is_need_to_calc_addr() > 0:
                if (tar_addr := cb.next_code.addr) is not None:
                    cb.code = ''.join(cb.old_code)
                    ig.set_addr(cb, tar_addr, cb.addr)


    def check_bugs(self):
        print('check')
        bugs = True
        while bugs:
            self.calculate_addr_of_blocks()
            for cb in self.llist_cb.forwardn():
                if cb.size != len(cb.bytes):
                    bugs = True
                    lg.warning('bugs with addres found!')
                    self.calculate_jump_addr2()
                    continue
                if hasattr(cb, 'next_addr'):
                    if cb.next_addr != cb.next.addr:
                        bugs = True
                        lg.warning('bugs with addres found!!!')
                        self.calculate_jump_addr2()
                        continue
                bugs = False




    def shuffle(self):
        self.llist_cb.shuffle()
        pass


    def get_ep(self):
        """Получения начального адреса"""
        return self.llist_cb.entry_point.addr

