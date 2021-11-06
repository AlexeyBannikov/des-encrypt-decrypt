import operator
from textwrap import wrap
from functools import reduce
from desTables import IP, IIP, EK, CK, EP, P, sBox, shiftBits
 
#преобразует строку в шестнадцатеричную строку
def stringToHex(string):
    return [i.zfill(16) for i in wrap(''.join([hex(ord(i))[2:] for i in string]), 16)]

#преобразует строку в 4 битные фрагменты и при необходимости заполняет 0
def stringToBin(string):
    return ''.join([bin(int(i, 16))[2:].zfill(4) for i in string])
 
#перестановка последовательности согласно P боксам
def permutation(block, box):
    return ''.join([block[i] for i in box])
 
def xor(a, b):
    return ''.join([str(int(i) ^ int(j)) for i, j in zip(a, b)])
 
#левый сдвиг
def leftCircularShift(block, i):
    return bin(int(block, 2) << i & 0x0fffffff | int(block, 2) >> 28 - i)[2:].zfill(28)
 
def concatenate(args):
    return reduce(operator.iadd, args, [])
 
def key_gen(block_1, block_2):
    li = []
    for i in shiftBits:
        block_1 = leftCircularShift(block_1, i)
        block_2 = leftCircularShift(block_2, i)
        li.append(permutation(block_1 + block_2, CK))
 
    return li
 
#функция f
def f(block, key):
    final = []
 
    for j, i in enumerate(wrap(xor(permutation(block, EP), key), 6)):
 
        temp_box = [
            sBox[j][0:16],
            sBox[j][16:32],
            sBox[j][32:48],
            sBox[j][48:64]
        ]
        final.append(bin(temp_box[int(i[0] + i[-1], 2)]
                         [int(i[1:-1], 2)])[2:].zfill(4))
 
    return permutation(''.join(final), P)
 
def des(block, key_array):
 
    left, right = block[0: len(block) // 2], block[len(block) // 2:]
    for j, i in zip(range(1, 17), key_array):
        right, left = xor(f(right, i), left), right
    return wrap(permutation(right + left, IIP), 8)
 
def encrypt(KEY, letter):
    encrypted_list = []
    for i in stringToHex(letter):
        bin_letter, bin_key = stringToBin(i), stringToBin(KEY)
        permutationd_key, permutationd_block = permutation(
            bin_key, EK), permutation(bin_letter, IP)
        key_list = key_gen(
            permutationd_key[: len(permutationd_key) // 2], permutationd_key[len(permutationd_key) // 2:])
        encrypted_list.append(''.join([hex(int(i, 2))[2:].zfill(
            2).upper() for i in des(permutationd_block, key_list)]))
    return (''.join(encrypted_list))
       
def decrypt(KEY, letter):   
    temp_li = []
    final = []
    for i in wrap(letter, 16):
        bin_letter, bin_key = stringToBin(i), stringToBin(KEY)
        permutationd_key, permutationd_block = permutation(
            bin_key, EK), permutation(bin_letter, IP)
        key_list = key_gen(
            permutationd_key[: len(permutationd_key) // 2], permutationd_key[len(permutationd_key) // 2:])
        temp_li.append(''.join([hex(int(i, 2))[2:].zfill(2).upper()
                                for i in des(permutationd_block, reversed(key_list))]))
    return (''.join(concatenate(
            [[chr(int(j, 16)) for j in wrap(i, 2) if int(j, 16) != 0] for i in temp_li])))