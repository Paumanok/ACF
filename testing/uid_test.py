#quick proof of concept of using the name for uid for tag

short_name = "fluffy"
weight = 12
uid = 0
for c in short_name:
    #print(hex(uid))
    uid = (uid << 8) + ord(c)

uid = uid + weight
print(hex(uid))

length = 0
temp_uid = uid
while temp_uid != 0:
    temp_uid = temp_uid >> 8
    length += 1

print(length)
print(hex(uid))
for i in range(length,16):
    uid = (uid << 8) + 0xFF


print(hex(uid))
listed = []
temp_uid = uid
for i in range(16):
    byt = temp_uid & 0xFF
    temp_uid = temp_uid >> 8
    listed.insert(0, byt)

print(listed)
