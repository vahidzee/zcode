from io import StringIO
import fileinput
import os
import math
import typing as th


def read_and_calculate_symbol_frequencies(file_name: str):
    data = StringIO()
    symbol_dict = dict()

    # reading file while calculating symbols' frequencies
    for line in fileinput.input(file_name):
        for char in line:
            if char not in symbol_dict:
                symbol_dict[char] = 1
            else:
                symbol_dict[char] += 1
            data.write(char)

    return data.getvalue(), sorted(symbol_dict.items(), key=lambda x: x[1], reverse=True)


def compute_metadata(
        symbols_frequency_list: list,
        lzw_max_bytes_count: int,
        output_stream,
        symbols_count_bytes_number: int = 2,
):
    # processing meta data
    symbols_count_in_bytes = int.to_bytes(len(symbols_frequency_list), symbols_count_bytes_number, 'big')

    # writing meta data on output stream
    output_stream.write(symbols_count_in_bytes)
    output_stream.write(bytes([lzw_max_bytes_count]))

    for item in symbols_frequency_list:
        output_stream.write(bytes(item[0], encoding='utf-8'))


def zee_code(code, max_code_bytes_count: int):
    bytes_count = 1 if not code else (int(math.log2(code)) // 7) + 1
    bytes_count = bytes_count if bytes_count < max_code_bytes_count else max_code_bytes_count
    byte_values = [0] * bytes_count
    counter = 1

    if bytes_count == max_code_bytes_count:
        byte_values[-1] = code % 256
        temp = code // 256
    else:
        byte_values[-1] = code % 128
        temp = code // 128

    while temp:
        counter += 1
        byte_values[-counter] = temp % 128 + 128
        temp //= 128

    if counter < bytes_count:
        byte_values[0] = 128

    return bytes(byte_values)


def lzw_compressed(input_data, symbols_frequency_list, output_stream, max_code_bytes_count: int):
    # setting up limitations
    max_table_size = 2 ** (max_code_bytes_count * 7 + 1)

    # Building and initializing the dictionary.
    dictionary_size = len(symbols_frequency_list)
    dictionary = {symbols_frequency_list[i][0]: i for i in
                  range(dictionary_size)}

    string = ""  # String is null.

    # lzw compression  algorithm combined with zee_codes
    for symbol in input_data:

        string_plus_symbol = string + symbol  # get input symbol.
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            output_stream.write(zee_code(dictionary[string], max_code_bytes_count=max_code_bytes_count))
            if dictionary_size < max_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        output_stream.write(zee_code(dictionary[string], max_code_bytes_count=max_code_bytes_count))

    return output_stream


def compress(
        input_file_name: str,
        output_file_name: th.Optional[str] = None,
        max_code_bytes_count: int = 0,  # 0 for auto adjustment
        symbols_count_bytes_number=2,
):
    # settings
    file_size = os.path.getsize(input_file_name) / 1000000
    if not max_code_bytes_count:
        if file_size < 2:
            max_code_bytes_count = 2
        elif file_size < 64:
            max_code_bytes_count = 4
        else:
            max_code_bytes_count = 8

    output_file_name = output_file_name or f'{input_file_name}.zee'
    # reading input file & calculating symbol frequencies
    input_data, symbols_frequency_list = read_and_calculate_symbol_frequencies(input_file_name)

    # checking max_code_bytes_count
    if int(math.log2(len(symbols_frequency_list))) // 7 > max_code_bytes_count:
        max_code_bytes_count = int(math.log2(len(symbols_frequency_list))) // 7 + 2

    # applying custom lzw compression algorithm and getting output bytestream
    with open(output_file_name, 'wb', buffering=2 ** 24) as output_file:
        compute_metadata(symbols_frequency_list, max_code_bytes_count, output_file,
                         symbols_count_bytes_number=symbols_count_bytes_number)
        lzw_compressed(input_data, symbols_frequency_list, output_file, max_code_bytes_count=max_code_bytes_count)
