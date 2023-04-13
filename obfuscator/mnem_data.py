
#i - imm - value
#l - length of previous operand
#r - reg - registr
#d - reg that twice longer next operands
#g - reg that any longer next operands 
#m - memory
#b - 1 byte
#w - 2 bytes
#d - 4 bytes
#q - 8 bytes
#x - 16 bytes
#y - 32 bytes
#z - 64 bytes
#a - any

mnemonics = [
# https://www.strchr.com/x86_machine_code_statistics
# frequency, mnemonic, possible args, possible next instruction
    [10, "add", # Add two values. 8
        ["r i","r m", "m r", "r r"]],  
    [1, "adc", # Add with carry.
        ["r i","r m", "m r", "r r"]],  
    [2, "and", # Logical and.
        ["r i","r m", "m r", "r r"]],
    [1, "bsf", # Bit scan forward. 1 op get number, 2 op scan for bits. If 0 only, then ZF = 1
        ["rw rw", "rw mw"]],  
    [1, "bsr", # Bit scan reverse.
        ["rw rw", "rw mw"]],  
    [1, "bt", # Bit test. 1 op from take the bit, 2 op number of bit. CF have the value of that bit. 
        ["rw rw", "mw rw", "rw l"]],   # "mw l" for 4
    [1, "btc", # Bit test and complement. Negate tested bit.
        ["rw rw", "mw rw", "rw l"]],  
    [1, "btr", # Bit test and reset. Set tested bit to 0.
        ["rw rw", "mw rw", "rw l"]],  
    [1, "bts", # Bit test and set. Set tested bit to 1.
        ["rw rw", "mw rw", "rw l"]],  
    [1, "call", # Call function and save IP and CS (far only). !imp
        ["iwd"]], 
    [1, "cbw", # Fill ah to 1 or 0 depends on elder bit of al
        ['']],  
    [1, "clc", # CF = 0
        ['']],  
    [1, "cld", # DF = 0 
        ['']],  
    [1, "cli", # IF = 0
        ['']],  
    [1, "cmc", # CF = r
        ['']],  
    [1, "cwd", # Word -> Double word AX -> DX
        ['']],  
    [1, "cdq", # DW -> QW EAX -> EDX
        ['']],  
    [9, "cmp", # Compares two ops. eq -> ZF = 1 gr -> SF=OF ls -> SF!=OF
        ["r i","r m", "m r", "r r"]],  
    [0, "cwde", # Word -> Double word AX -> EAX
        ['']], 
    [1, "dec", # Decrements op
        ["r"]],  
    [1, "div", # AX / op = AL and mod AH, DX:AX / op = AX and mod DX
        ["r"]],  
    [1, "idiv", # Div with sign.
        ["r"]],    
    [1, "enter", #
        ["iw l"]],
    [1, "imul", # AL * REG = AX with sign.
        ["rw mw", "rw rw", "rw rw i"]], #"m r"    
    [1, "inc", # Increment 
        ["r"]],    
    [0, "lahf", # Set FLAGS -> AH (SF:ZF:0:AF:0:PF:1:CF)
        ['']],    
    [0, "leave", # Copy BP -> SP. stack-> BP.
        ['']],   
    [0, "loop", # Dec ECX then continue or Jump to label if CX != 0 !imp
        ['']],
    [0, "loopnz", # Dec ECX then continue or Jump to label if CX !=0 and ZF = 0 !imp
        ['']], 
    [0, "loopz", # Dec ECX then continue or Jump to label if CX !=0 and ZF = 1 !imp
        ['']],   
    [0, "loopne", # Synonyms
        ['']],  
    [0, "loope", 
        ['']],
    [50, "mov",  # move value of op 2 in op 1. !imp 
        ['r r', 'm r', 'r m', 'r i']],    # 'm i'
    [1, "movsx", # mov r16, r8 with sign fill.
        ["gw r"]],   
    [1, "movzx", # mov r16, r8 with zero fill
        ["gw r"]],  
    [2, "mul", # AL * REG = AX
        ["r"]], 
    [2, "neg",  # Negates op. CF=0|1 (if qe 0) OF=r SF=r ZF=r AF=r PF=r.
        ["r"]], 
    [1, "nop", # Do notthing exept inc EIP.
        ['']],  
    [2, "not",  # Logical inversion.
        ["r"]], 
    [3, "or",  # Logical or
        ["r i","r m", "m r", "r r"]],  
    [10, "pop", # Pop from stack to op
        ["rw"]],  
    [0, "popa", # Pop DI, SI, ВР, SP, BX, DX, СХ, АХ
        ['']], 
    [0, "popad", # Pop EDI, ESI, ЕВР, ESP, EBX, EDX, ЕСХ, ЕАХ
        ['']],
    [1, "popf", # Pop FLAGS
        ['']],   
    [0, "popfd",  # Pop EFLAGS
        ['']],  
    [17, "push", # Push to stack 17
        ["rw"]],   
    [0, "pusha", # Pop DI, SI, ВР, SP, BX, DX, СХ, АХ
        ['']],
    [0, "pushad", # Pop EDI, ESI, ЕВР, ESP, EBX, EDX, ЕСХ, ЕАХ
        ['']],
    [1, "pushf",  # Pop FLAGS
        ['']],
    [0, "pushfd",  # Pop EFLAGS
        ['']],
    [1, "rcl", # Cyclic rotate to the left using CF
        ["r l"]], #"r CL", "m l", "m CL" for 2 
    [1, "rcr", # Cyclir rotate to the right using CF
        ["r l"]],    
    [1, "ret", # Return from procedure !imp
        ['']],    
    [0, "retn", # Return far !imp
        ['']],   
    [1, "retf", # Retunr far + privilegies !imp
        ['']],   
    [2, "rol", # Cyclic rotate to the left
        ["r l"]], # "r CL", "m l", "m CL"     
    [2, "ror", # Cyclic rotate to the right
        ["r l"]], # for 2   
    [1, "sahf", # AH -> FLAGS
        ['']],   
    [1, "sal", # Arithmetic shift left
        ["r l"]],    
    [1, "sar", # Arithmetic shift right
        ["r l"]],    
    [1, "sbb", # Sub with Borrow
        ["r i","r m", "m r", "r r"]],    
    [1, "shl", # Logic shift left
        ["r l"]],    
    [0, "shld", # Double prrecise shift left
        ["r l"]],   
    [1, "shr", # Logic shift right
        ["r l"]],     
    [0, "shrd", # Double precise shift right
        ["r l"]],   
    [1, "stc", # CF=1
        ['']],    
    [1, "std", # DF=1
        ['']],    
    [1, "sti", # IF = 1
        ['']],    
    [3, "sub", # Substraction
        ["r i","r m", "m r", "r r"]],    
    [1, "test", # Logical compare
        ["r i", "m r", "r r"]],   
    [1, "xchg", # Swap two ops
        ["r m", "m r", "r r"]],   
    [5, "xor", # Logical or
        ["r i","r m", "m r", "r r"]],    
]

jumps = [
    [1, "jmp"],
    [1, "je"],
    [1, "jne"],
    [1, "jl"],
    [1, "jle"],
    [1, "jg"],
    [1, "jge"],
    [1, "jb"],
    [1, "jbe"],
    [1, "ja"],
    [1, "jae"],
    [1, "jz"],
    [1, "js"],
    [1, "jc"],
    [1, "jo"],
    [1, "jp"],
    [1, "jnz"],
    [1, "jns"],
    [1, "jnc"],
    [1, "jno"],
    [1, "jnp"],
    [1, "jcxz"],
    [1, "jecxz"],
]

loops = [

]

registers = [
    ["AL", "BL", "CL", "DL", "AH", "BH", "CH", "DH"],
    ["AX", "BX", "CX", "DX"], # "SI", "DI", "BP", "SP", "CS", "DS", "SS", "ES", "IP"
    ["EAX", "EBX", "ECX", "EDX"], # "ESI", "EDI", "EBP", "ESP", "CS", "DS", "SS", "ES", "EIP"
    ["RAX"],
]

insts = []
probs = []

class Mnemonic:
    def __init__(self, instruction, min_size=1, max_size=3, operands = [], ops_sizes = []):
        self.instruction = instruction
        self.min_size = min_size
        self.max_size = max_size
        self.operands = operands
        self.ops_sizes = ops_sizes

