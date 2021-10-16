import mmap
import contextlib
import os.path


def decompress(compressed_file_name: str, decompressed_file_name: str = None, symbols_count_bytes_number: int = 2):
    # input & output path & names
    decompressed_file_name = decompressed_file_name or f'{os.path.splitext(compressed_file_name)[0]}'

    # reading compressed file
    with open(compressed_file_name, 'rb') as file:
        with contextlib.closing(mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)) as input_file:
            # reading meta data
            symbols_count = int.from_bytes(input_file.read(symbols_count_bytes_number), byteorder='big')
            max_code_bytes_count = int.from_bytes(input_file.read(1), byteorder='big')
            print('\033[32;0msymbols count:\033[0m', symbols_count, '\033[32;0mmax code bytes count:\033[0m',
                  max_code_bytes_count)
            symbols_frequency_list = []
            for i in range(symbols_count):
                cache = bytes(0)
                while True:
                    cache += input_file.read(1)
                    try:
                        symbols_frequency_list.append(cache.decode('utf-8'))
                        break
                    except:
                        pass

            # reading compressed data
            data_bytes = input_file.read()

    compressed_data = []
    next_code = symbols_count

    string = ""
    #
    # Reading the compressed file.
    counter = code = 0

    for byte in data_bytes:
        counter += 1
        if counter == max_code_bytes_count:
            compressed_data.append(code * 256 + byte)
            code = counter = 0
            continue
        if byte < 128:
            compressed_data.append(code * 128 + byte)
            code = counter = 0
            continue
        code = code * 128 + (byte - 128)

    # building and initializing the dictionary.
    dictionary = {x: symbols_frequency_list[x] for x in range(symbols_count)}

    # iterating through the codes.
    # lzw decompression algorithm
    with open(decompressed_file_name, 'w', encoding='utf-8', buffering=2 ** 24) as output_file:
        for code in compressed_data:
            if code not in dictionary:
                dictionary[code] = string + (string[0])
            output_file.write(dictionary[code])
            if len(string) != 0:
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]
