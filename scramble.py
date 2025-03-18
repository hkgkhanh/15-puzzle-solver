from math import floor
import random


def shuffle():
    tiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    for i in range(len(tiles) - 1, 0, -1):
        j = floor(random.random() * (i + 1))
        temp = tiles[i]
        tiles[i] = tiles[j]
        tiles[j] = temp

    return tiles

def get_inv_count(tiles):
    inv_count = 0
    for i in range(0, 14):
        for j in range(i + 1, 15):
            if tiles[i] and tiles[j] and tiles[i] > tiles[j]:
                inv_count += 1
    return inv_count

def scramble():
    matrix = []
    scramble_list = shuffle()
    inv_count = get_inv_count(scramble_list)
    arr1 = [4, 5, 6, 7, 12, 13, 14, 15]
    arr2 = [0, 1, 2, 3, 8, 9, 10, 11]

    r = 0
    if inv_count % 2 == 0:
        r = random.choice(arr1)
    else:
        r = random.choice(arr2)

    scramble_list.insert(r, 0)

    for i in range(4):
        row = []
        for j in range(4):
            row.append(scramble_list[i * 4 + j])
        matrix.append(row)

    return matrix