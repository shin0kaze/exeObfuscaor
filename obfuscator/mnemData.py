from mnemonic import mnem, get
from random import choice, choices
# TODO: На самом деле можно создать неесколько значений с 1 мнемоникой
# для разного количества операндов. Это бы упростило бы логику
# Либо сделать функцию для сборки списка для импорта.

rm_rmi = [['r i','r m', 'r r', 'm r', 'm i']]
r_rm = [['r r', 'r m']]
rmi = [['r', 'm', 'i']]
rm_rl = [['r r', 'm r', 'r l', 'm l']]
r_rmi = [['r r', 'r m', 'r i']]
r_r = [['r r']]
r = [['r']]
r_l = [['r l', 'm l']]
i = [['i']]
rm_rm_i = [['r','m'],['r r', 'r m'],['r r i', 'r m i']]
rm_rm = [['r m', 'r r', 'm r']]
rmi = [['r', 'm', 'i']]
rm = [['r', 'm']]
ri = [['r', 'm', 'i']]
b = [['b']] # imm8
mnemonics = [
# https://www.strchr.com/x86_machine_code_statistics - анализ вероятности инструкций
# [frequency, mnemonic]
  
    # -===/ SHIFTS \===- 
    
    [1, # Cyclic rotate to the left using CF
        mnem('rcl', r_l)], #"r CL", "m l", "m CL" for 2 
    [1, # Cyclir rotate to the right using CF
        mnem('rcr', r_l)],
    [1, # Logic shift left
        mnem('shl', r_l)],    
    [0, # Double precise shift left
        mnem('shld', r_l)],   
    [1, # Logic shift right
        mnem('shr', r_l)],     
    [0, # Double precise shift right
        mnem('shrd', r_l)],  
    [2, # Cyclic rotate to the left
        mnem('rol', r_l)], # "r CL", "m l", "m CL"     
    [2, # Cyclic rotate to the right
        mnem('ror', r_l)], # for 2    
    [1, # Arithmetic shift left
        mnem('sal', r_l)],    
    [1, # Arithmetic shift right
        mnem('sar', r_l)], 
    
    # -===/ MATH \===-

    [2, # Negates op. CF=0|1 (if qe 0) OF=r SF=r ZF=r AF=r PF=r.
        mnem('neg', r)], 
    [1, # AL * REG = AX with sign.
        mnem('imul', rm)],
    [1, # AL * REG = AX with sign.
        mnem('imul', rm_rm_i, (2, 3))],    
    [1, # Increment 
        mnem('inc', r)],   
    [1, # Decrements op
        mnem('dec', r)],  
    [1, # AX / op = AL and mod AH, DX:AX / op = AX and mod DX
        mnem('div', r)],  
    [1, # Div with sign.
        mnem('idiv', r)],
    [10, # Add two values.
        mnem('add', rm_rmi)], 
    [1, # Add with carry. 
        mnem('adc', rm_rmi)], 
    [2, # Logical and.
        mnem('and', rm_rmi)], 
    [1, # Bit scan forward. 1 op get number, 2 op scan for bits. If 0 only, then ZF = 1
        mnem('bsf', r_rm, (2, 3))],  
    [1, # Bit scan reverse.
        mnem('bsr', r_rm, (2, 3))],  
    [1, # Bit test. 1 op from take the bit, 2 op number of bit. CF have the value of that bit. 
        mnem('bt', rm_rl, (2, 3))],   # "mw l" for 4
    [1, # Bit test and complement. Negate tested bit.
        mnem('btc', rm_rl, (2, 3))],  
    [1, # Bit test and reset. Set tested bit to 0.
        mnem('btr', rm_rl, (2, 3))],  
    [1, # Bit test and set. Set tested bit to 1.
        mnem('bts', rm_rl, (2, 3))], 
    [1, # Sub with Borrow
        mnem('sbb', rm_rmi)],
    [3, # Substraction
        mnem('sub', rm_rmi)],
    [5, # Logical or
        mnem('xor', rm_rmi)],
    [2, # AL * REG = AX
        mnem('mul', r)],
    [2, # Logical inversion.
        mnem('not', 'r')], 
    [3, # Logical or
        mnem('or', rm_rmi)],  

    # -===/ JUMPS \===-

    [15, 
        mnem('jmp', rmi, (2, 3))],
    [8, 
        mnem('jmp', b, (1, 1))],
    [10, 
        mnem('je', b, (1, 1))],
    [10, 
        mnem('jne', b, (1, 1))],
    [10, 
        mnem('jl', b, (1, 1))],
    [10, 
        mnem('jle', b, (1, 1))],
    [10, 
        mnem('jg', b, (1, 1))],
    [10, 
        mnem('jge', b, (1, 1))],
    [10, 
        mnem('jb', b, (1, 1))],
    [10, 
        mnem('jbe', b, (1, 1))],
    [10, 
        mnem('ja', b, (1, 1))],
    [10, 
        mnem('jae', b, (1, 1))],
    [10, 
        mnem('jz', b, (1, 1))],
    [10, 
        mnem('js', b, (1, 1))],
    [10, 
        mnem('jc', b, (1, 1))],
    [10, 
        mnem('jo', b, (1, 1))],
    [10, 
        mnem('jp', b, (1, 1))],
    [10, 
        mnem('jnz', b, (1, 1))],
    [10, 
        mnem('jns', b, (1, 1))],
    [10, 
        mnem('jnc', b, (1, 1))],
    [10, 
        mnem('jno', b, (1, 1))],
    [10, 
        mnem('jnp', b, (1, 1))],
    [10, 
        mnem('jcxz', b, (1, 1))],
    [10, 
        mnem('jecxz', b, (1, 1))],

    # -===/ STACK \===-

    [10,# Pop from stack to op
        mnem('pop', r, (2,3))],  
    [0, # Pop DI, SI, ВР, SP, BX, DX, СХ, АХ
        mnem('popa')], 
    [0, # Pop EDI, ESI, ЕВР, ESP, EBX, EDX, ЕСХ, ЕАХ
        mnem('popad')],
    [1, # Pop FLAGS
        mnem('popf')],   
    [0,  # Pop EFLAGS
        mnem('popfd')],  
    [17, # Push to stack 17
        mnem('push', r, (2,3))],   
    [0, # Pop DI, SI, ВР, SP, BX, DX, СХ, АХ
        mnem('pusha')],
    [0, # Pop EDI, ESI, ЕВР, ESP, EBX, EDX, ЕСХ, ЕАХ
        mnem('pushad')],
    [1,  # Pop FLAGS
        mnem('pushf')],
    [0,  # Pop EFLAGS
        mnem('pushfd')],

    # -===/ CYCLE, FUNCS \===-

    [1, # Return from procedure
        mnem('ret')],    
    [0, # Return far 
        mnem('retn')],   
    [1, # Retunr far + privilegies 
        mnem('retf')], 
    [1, # Dec ECX then continue or Jump to label if CX != 0 !imp
        mnem('loop', b)],
    [0, # Dec ECX then continue or Jump to label if CX !=0 and ZF = 0 !imp
        mnem('loopnz', b)], 
    [0, # Dec ECX then continue or Jump to label if CX !=0 and ZF = 1 !imp
        mnem('loopz', b)],   
    [1, # Synonyms
        mnem('loopne', b)],  
    [1, 
        mnem('loope', b)],

    # -===/ FLAGS \===-

    [1, # Call function and save IP and CS (far only). !imp
        mnem('call', rmi, (2,3))], 
    [1, # AH -> FLAGS
        mnem('sahf')],
    [1, # Set FLAGS -> AH (SF:ZF:0:AF:0:PF:1:CF)
        mnem('lahf')],
    [1, # CF=1
        mnem('stc')],    
    [1, # DF=1
        mnem('std')],    
    [1, # IF = 1
        mnem('sti')],
    [1, # CF = 0
        mnem('clc')],  
    [1, # DF = 0 
        mnem('cld')],  
    [1, # IF = 0
        mnem('cli')],  
    [1, # CF = r
        mnem('cmc')],   
    
    # -===/ OTHER \===-

    [1, # Fill ah to 1 or 0 depends on elder bit of al
        mnem('cbw')],   
    [1, # Word -> Double word AX -> DX
        mnem('cwd')],  
    [1, # DW -> QW EAX -> EDX
        mnem('cdq')],  
    [9, # Compares two ops. eq -> ZF = 1 gr -> SF=OF ls -> SF!=OF
        mnem('cmp', rm_rmi)],  
    [0, # Word -> Double word AX -> EAX
        mnem('cwde')],     
    [0, # 
        mnem('enter', i, (1,2))],     
    [1, # Copy BP -> SP. stack-> BP.
        mnem('leave')],   
    [50,# move value of op 2 in op 1. !imp 
        mnem('mov', rm_rmi)],    # 'm i'
    [1, # mov r16, r8 with sign fill.
        mnem('movsx', r_r, (1,2), (1,0))],   
    [1, # mov r16, r8 with zero fill
        mnem('movzx', r_r, (1,2), (1,0))],       
    [1, # Logical compare
        mnem('test', rm_rmi)],   
    [1, # Swap two ops
        mnem('xchg', rm_rm)], 
    [1, # Do notthing exept inc EIP.
        mnem('nop')],  
]

ptr_sizes = [
    'byte',
    'word',
    'dword',
    'qword',
    'oword',
    'yword',
    'tword'
]

aviable_regs = [
    ["AL", "BL", "CL", "DL", "AH", "BH", "CH", "DH"],
    ["AX", "BX", "CX", "DX"], # "SI", "DI", "BP", "SP", "CS", "DS", "SS", "ES", "IP"
    ["EAX", "EBX", "ECX", "EDX"], # "ESI", "EDI", "EBP", "ESP", "CS", "DS", "SS", "ES", "EIP"
]

def choice_reg(size):
    return choice(aviable_regs[size-1])

def gen_probs():
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

def choose_inst(mnems, probs):
    """Выбирает случайную инструкцию"""
    m = choices(mnems, cum_weights=probs, k=1)[0][1]
    return  get(m)

def ptr(size):
    return ptr_sizes[size-1]
