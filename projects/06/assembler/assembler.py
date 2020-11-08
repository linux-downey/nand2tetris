import sys

symbol_table = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,
                "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,
                "R6":6,"R7":7,"R8":8,"R9":9,"R10":10,
                "R11":11,"R12":12,"R13":13,"R14":14,
                "R15":15,"SCREEN":0x4000,"KBD":0x6000
                }

init_label_start_addr = 16

def insert_variable_to_table(var_name):
    global init_label_start_addr
    symbol_table[var_name] = init_label_start_addr
    print("    add variable:%s" % var_name)
    init_label_start_addr += 1

def insert_label_to_table(label_name,addr):
    symbol_table[label_name] = addr
    print("    add label:%s" % label_name)



def is_only_comment(sline):
    if(sline[0] == '/' and sline[1] == '/'):
        return True
    return False
        
def is_inline_comment(sline):
    for i in range(len(sline)):
        if(sline[i] == '/' and sline[i+1] == '/'):
            return sline[0:i]
    return False

def is_empty(line):
    return (len(line) == 0)

def pre_process_lines(sline):

    # if is empty,do not write back
    if(is_empty(sline)):
        return False

    # if is only comment,do not write back
    if(is_only_comment(sline)):
        return False
    
    # cut off the inline comment
    s = is_inline_comment(sline)
    if(s):
        return s
    return sline

# delete white space & comment
# pass src's fd,operate on src file directly.return line count;
def del_invalid_lines(fd,pre_fd):
    count = 0
    for line in fd.readlines():
        sline = line.strip()
        s = pre_process_lines(sline)
        
        if(s):
            s = s.strip()
            pre_fd.write(s+'\n')
    pre_fd.flush()


# scan the whole lines to find the label to add it to table
def scan_label_add_to_table(pre_fd):
    count = 0
    for line in pre_fd.readlines():
        count += 1
        line = line.strip('\n')                               # all line end with '\n'
        if(line.startswith('(') and line.endswith(')')):
            count -= 1
            label = line[line.index('(')+1:line.index(')')]
            insert_label_to_table(label,count)

def scan_variable_add_to_table(pre_fd):
    matched = False
    for line in pre_fd.readlines():
        if(line.startswith('@')):
            val = line[1:].strip('\n')
            # print("xxxxx %s" % val)
            if(val.isdigit()):
                continue
            for key in symbol_table:
                matched = False
                if(val == key):
                    # print("%s -> %s" %(val,key))
                    matched = True
                    break
            # print(matched)
            if(False == matched):
                # print("adddddddd %s" % val)
                insert_variable_to_table(val)

# translate sybolic code to pure assemble instruction
def replace_all_symbol(pre_fd,pure_fd):
    count = 0                             # To remember the line number which to replace the label
    match_flag = False
    for line in pre_fd.readlines():
        count += 1
        if(line.startswith('(')):
            line = line.strip('\n')
            if(line.endswith(')')):           # find a symbol defined,delete it.
                # count -= 1
                continue
        
        # replace variable and symbol
        if(line.startswith('@')):
            # print(line)
            val = line[1:].strip('\n')
            if(val.isdigit()):
                pure_fd.write(line)
                continue
            else:
                for key in symbol_table:
                    if(val == key):
                        match_flag = True
                        line = "@" + str(symbol_table[val]) + '\n'
                        print("    Replace %s to %s" % (val,line))
                        break
                if(match_flag == False):
                    print("Error:can't find symbol!")
                    while(1):
                        pass
        # clear all white space
        line = line.replace(" ","")
        pure_fd.write(line);                # write it to  .pure file.
    pure_fd.flush()


def decode_dest(dest):
    code = 0
    # print("dest = %s" % dest)
    if(None == dest):
        return None
    if('A' in dest):
        code |= 1 << 5
    if('D' in dest):
        code |= 1 << 4
    if('M' in dest):
        code |= 1 << 3  
    return code

def decode_comp(comp):
    code = 0
    if(None == comp):
        return None
    if("0" == comp):
        code |= 0b0101010 << 6
    elif("1" == comp):
        code |= 0b0111111 << 6
    elif("-1" == comp):
        code |= 0b0111010 << 6    
    elif("D" == comp):
        code |= 0b0001100 << 6
    elif("A" == comp):
        code |= 0b0110000 << 6
    elif("!D" == comp):
        code |= 0b0001101 << 6
    elif("!A" == comp):
        code |= 0b0110001 << 6
    elif("-D" == comp):
        code |= 0b0001111 << 6
    elif("-A" == comp):
        code |= 0b0110011 << 6
    elif("D+1" == comp):
        code |= 0b0011111 << 6
    elif("A+1" == comp):
        code |= 0b0110111 << 6
    elif("D-1" == comp):
        code |= 0b0001110 << 6
    elif("A-1" == comp):
        code |= 0b0110010 << 6
    elif("D+A" == comp):
        code |= 0b0000010 << 6
    elif("D-A" == comp):
        code |= 0b0010011 << 6
    elif("A-D" == comp):
        code |= 0b0000111 << 6    
    elif("D&A" == comp):
        code |= 0b0000000 << 6
    elif("D|A" == comp):
        code |= 0b0010101 << 6
    elif("M" == comp):
        code |= 0b1110000 << 6
    elif("!M" == comp):
        code |= 0b1110001 << 6
    elif("-M" == comp):
        code |= 0b1110011 << 6    
    elif("M+1" == comp):
        code |= 0b1110111 << 6
    elif("M-1" == comp):
        code |= 0b1110010 << 6
    elif("D+M" == comp):
        code |= 0b1000010 << 6
    elif("D-M" == comp):
        code |= 0b1010011 << 6
    elif("M-D" == comp):
        code |= 0b1000111 << 6
    elif("D&M" == comp):
        code |= 0b1000000 << 6
    elif("D|M" == comp):
        code |= 0b1010101 << 6
    else:
        print("*****Unkown comp instruction: %s *****" % comp)
    return code


def decode_jump(jump):
    code = 0
    if(None == jump):
        return None
    if("JGT" in jump):
        code |= 0b001
    elif("JEQ" in jump):
        code |= 0b010
    elif("JGE" in jump):
        code |= 0b011
    elif("JLT" in jump):
        code |= 0b100
    elif("JNE" in jump):
        code |= 0b101
    elif("JLE" in jump):
        code |= 0b110
    elif("JMP" in jump):
        code |= 0b111
    else:
        print("*****Unknown jump instruction*****")
    
    return code


def get_three_parts(line):
    dic = {"dest":None,"comp":None,"jump":None}
    if('=' in line):
        dest,tmp = line.split('=')
        dic["dest"] = dest
        #dest = comp;jump
        if(';' in line):
            comp,jump = tmp.split(';')
            dic["comp"] = comp
            dic["jump"] = jump
        #dest = comp; jump=null
        else:
            dic["comp"] = tmp
    else:
        #comp;jump
        if(';' in line):
            comp,jump = line.split(';')
            dic["comp"] = comp
            dic["jump"] = jump
        # only jump or only comp
        else:
            print("***** Temprory not support instruction! *****")
    return dic

def construct_A_instruction(addr,binary_fd):
    # print(addr)
    addrint = int(addr)
    # print(addrint)
    code = addrint.to_bytes(4,byteorder="big")
    # print(code)
    binary_fd.write(code[2:4])
    binary_fd.flush()

def construct_C_instruction(line,binary_fd):
    # code = bytes([0,0])
    # code[0] |= 7 << 5     # set high 3 bits to 111
    code = 0
    code |= 7 << 13         # set high 3 bits to 111

    # There optional parts: dest = comp;jump
    dic = get_three_parts(line)
    
    dest_code = decode_dest(dic["dest"])
    if(dest_code != None):
        code |= dest_code & (0b111 << 3)

    comp_code = decode_comp(dic["comp"])
    if(comp_code != None):
        code |= comp_code & (0b1111111 << 6)

    jump_code = decode_jump(dic["jump"])
    if(jump_code != None):
        code |= jump_code & 0b111
    
    code = code.to_bytes(4,byteorder="big")
    binary_fd.write(code[2:4])
    binary_fd.flush()



def translate_pure_to_machine_code(pure_fd,binary_fd):
    for line in pure_fd.readlines():
        if(line.startswith('@')):
            # print(line)
            val = line[1:].strip('\n')
            construct_A_instruction(val,binary_fd)
        else:
            line = line.strip('\n')
            construct_C_instruction(line,binary_fd)



asm_src_file = sys.argv[1]
src_file_without_suffix = asm_src_file.split('.')[0]
pre_file = src_file_without_suffix + ".pre"
pure_file = src_file_without_suffix + ".pure"
binary_file = src_file_without_suffix + ".hack"

af = open(asm_src_file, "r")
pre_fd = open(pre_file, "w+")
pure_fd = open(pure_file, "w+")
binary_fd = open(binary_file, "wb")

# delete emptyline,comment,write to xxx.pre
print("start preprocess , delete invalid line")
del_invalid_lines(af,pre_fd)
print("preprocess finished")
print(" ")

af.close()

pre_fd.seek(0)
print("start scan lable")
scan_label_add_to_table(pre_fd)
print("scan lable finished")
print(" ")

pre_fd.seek(0)
print("start scan variable")
scan_variable_add_to_table(pre_fd)
print("scan finished")
print(" ")

pre_fd.seek(0)
print("start replace symbol")
replace_all_symbol(pre_fd,pure_fd)
print("replace symbol finished")
print(" ")

# for key in symbol_table:
#     print(key + ":" + str(symbol_table[key]))

pre_fd.close()

pure_fd.seek(0)
print("start compile")
# construct_A_instruction(12345,binary_fd)
translate_pure_to_machine_code(pure_fd,binary_fd)
print("compile finished")





pure_fd.close()
binary_fd.close()


