def col_to_letters(col):
    result = ""
    while col >= 0:
        result = chr(col % 26 + 65) + result
        col = col // 26 - 1
    return result


def letters_to_col(letters):
    col = 0
    for c in letters:
        col = col * 26 + (ord(c.upper()) - ord('A') + 1)
    return col - 1