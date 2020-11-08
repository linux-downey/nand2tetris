

def test(a):
    a[0] |= 2

b=123
s=b.to_bytes(4,byteorder="little")
print(s)
test(s)
print(s)
