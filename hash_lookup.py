from hashlib import md5

rainbow = {}
NUMS = '0123456789'
ALL_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
PASS_TYPES = ['aaaaaa1', 'aaaaaa11', 'aaaaaaa1', 'aaaaaaa11', 'aaaaaaaaa1', 'aaaaaaaa11']
CHAIN_LEN = 1000


def read_rainbow():
    with open("PassTable.txt", 'r') as file:
        line = file.readlines()
        for l in line:
            lst = l.strip().split()
            rainbow[lst[0]] = lst[1]


def read_hashes():
    hash_values = []
    with open("hashes.txt", 'r') as file:
        line = file.readlines()
        for l in line:
            hash_values.append(l.strip())
    return hash_values


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


def lookup(test_hash):
    check_hash = test_hash
    for pt in PASS_TYPES:
        chain_num = CHAIN_LEN - 1
        while chain_num >= 0:
            if rainbow.get(check_hash):
                print(i)
                return [chain_num, rainbow.get(check_hash)]
            else:
                check_hash = test_hash
                for j in range(chain_num, CHAIN_LEN):
                    pt = reduction_function(pt, check_hash, j)
                    check_hash = md5_hasher(pt)
            chain_num -= 1


def hash_lookup(hash_val):
    pack = lookup(hash_val)
    if pack:
        pwd = pack[1]
        for i in range(pack[0] + 1):
            pwd = reduction_function(pwd, md5_hasher(pwd), i)
        return pwd
    else:
        return 'Password Not Found'


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


def main():
    hashes = read_hashes()
    read_rainbow()
    passes = []
    for chash in hashes:
        pwd = hash_lookup(chash)
        passes.append(pwd)
    print(passes)


main()