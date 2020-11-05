import sys

def is_buitin_var():
    pass

def is_variable():
    pass

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

def pre_process(sline):

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
        s = pre_process(sline)
        
        if(s):
            print(s)
            pre_fd.write(s)

asm_src_file = sys.argv[1]
src_file_without_suffix = asm_src_file.split('.')[0]
pre_file = src_file_without_suffix + ".pre"

af = open(asm_src_file, "r")
pre_fd = open(pre_file, "w+")

del_invalid_lines(af,pre_fd)

for line in pre_fd.readlines():
    print(line)

af.close()
pre_fd.close()

    



