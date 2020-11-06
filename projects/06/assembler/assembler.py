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

def insert_label_to_table(label_name):
    global init_label_start_addr
    symbol_table[label_name] = init_label_start_addr
    print("    add label:%s" % label_name)
    init_label_start_addr += 1

def get_symbol_from_bracket(line):


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
    for line in pre_fd.readlines():
        line = line.strip('\n')                               # all line end with '\n'
        if(line.startswith('(') and line.endswith(')')):
            label = line[line.index('(')+1:line.index(')')]
            insert_label_to_table(label)

def scan_variable_add_to_table(pre_fd):
    match_flag = False
    for line in pre_fd.readlines():
        if(line.startswith('@')):
            val = line[1:].strip('\n')
            if(val.isdigit()):
                continue
            for key in symbol_table:
                if(val == key):
                    match_flag = True
                    break
            if(False == match_flag):
                
                insert_variable_to_table(val)

# translate sybolic code to pure assemble instruction
def replace_all_symbol(pre_fd,pure_fd):
    count = 0                             # To remember the line number which to replace the label
    for line in pre_fd.readlines():
        count += 1
        if(line.startswith('('):
            line = line.strip('\n')
            if(line.endswith(')')):           # find a symbol defined,delete it.
                continue
        
        # replace variable and symbol
        if(line.startswith('@')):
            val = line[1:].strip('\n')
            if(val.isdigit()):
                continue

        pure_fd.write(line);                # write it to  .pure file.
            

asm_src_file = sys.argv[1]
src_file_without_suffix = asm_src_file.split('.')[0]
pre_file = src_file_without_suffix + ".pre"
pure_file = src_file_without_suffix + ".pure"

af = open(asm_src_file, "r")
pre_fd = open(pre_file, "w+")
pure_fd = open(pure_file, "w+")

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

print("start replace symbol")
replace_all_symbol(pre_fd,pure_fd)
print("replace symbol finished")
print(" ")

for key in symbol_table:
    print(key + ":" + str(symbol_table[key]))

pre_fd.close()
pure_file.close()



