from hashlib import md5
import random

NUMS = '0123456789'
ALL_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def md5_hasher(word):
    word = word.encode('utf-8')
    return md5(word).hexdigest()


def reduction_function(pwd, hasher, column):
    plaintext = []
    byte_array = generate_hash_byte(hasher)
    char_len = count_chars(pwd)
    for i in range(len(pwd)):
        index = byte_array[(i + column) % len(byte_array)]
        if i < char_len:
            new_c = ALL_CHARS[index % len(ALL_CHARS)]
        else:
            new_c = NUMS[index % len(NUMS)]
        plaintext.append(new_c)
    return "".join(plaintext)


def count_chars(word):
    count = 0
    for i in word:
        if i in ALL_CHARS:
            count += 1
    return count


def generate_hash_byte(to_hash):
    arr = []
    remaining = int(to_hash, 16)
    while remaining > 0:
        arr.append(remaining % 256)
        remaining //= 256
    return arr


def passgen():
    NUM_RANGE = random.randrange(1, 3)
    CHAR_RANGE = random.randrange(6, 9)
    pwd = ''
    for i in range(CHAR_RANGE):
        random.pwd = pwd + random.choice(ALL_CHARS)
    if NUM_RANGE == 2:
        random.pwd = pwd + str(random.randrange(10, 100))
    else:
        random.pwd = pwd + str(random.randrange(0, 10))
    return pwd

def read_text(file_name):
    terms = []
    with open(file_name, 'r') as file:
        line = file.readlines()
    for l in line:
        l = l.strip()
        terms.append(l)  # get each term
    return terms


def write_to_file(pwd, file_name):
    with open(file_name, 'w') as outfile:
        for p in pwd:
            # outfile.write(p+" : "+str(pwd[p]))
            outfile.write(p + "\t" + pwd[p])
            outfile.write("\n")


rainbow = {}
allpass = read_text("PassTable.txt")
for pwd in allpass:
    thash = md5_hasher(pwd)
    for i in range(0, 1000):
        tpwd = reduction_function(pwd, thash, i)
        thash = md5_hasher(tpwd)
    rainbow[thash] = pwd
write_to_file(rainbow, "rainbow.txt")