import sys
from rw import rw
from compiler import c
from obfuscator import Obfuscator
import logger

target, output = sys.argv[1:]

logger.init(is_debug=False)
logger.info('obfuscation started...')

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

ob.check_bugs()

rw.set_eop(ob.get_ep())
l = ob.llist_cb
pass
rw.write(output, ob.llist_cb)



