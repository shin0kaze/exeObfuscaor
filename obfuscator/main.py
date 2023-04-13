import sys
from rw import rw
from compiler import c
from ob_utils import Obfuscator

target, output = sys.argv[1:]


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

#llist_cb.shuffle()

# add_jumps(llist_cb)
# add_garbage(llist_cb)
# calculate_addr_of_blocks(llist_cb)
# calculate_jump_addr(llist_cb)
# print_cb(llist_cb)
#print_cbcf(llist_cb)
rw.set_eop(ob.get_ep())
rw.write(output, ob.llist_cb)



