import sys
from rw import rw
from compiler import c
from ob_utils import Obfuscator
import logger

target, output = sys.argv[1:]

logger.init(is_debug=True)

rw.read(target)
code = rw.codedata()
instructions = c.disasm(code)
ob = Obfuscator(instructions)

ob.shuffle()
ob.add_jumps()
ob.add_garbage()
ob.calculate_addr_of_blocks()
ob.calculate_jump_addr()
ob.print_cb()
ob.print_cbcf()

rw.set_eop(ob.get_ep())
rw.write(output, ob.llist_cb)



