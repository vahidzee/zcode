import argparse
import os
from zcode import compress, decompress, __version__


def main():
    parser = argparse.ArgumentParser(
        description=f'''ZCode ({__version__}) compress and decompress to and from `.zee` files!''')
    parser.add_argument('input', help='input file', )
    parser.add_argument('--action', dest='action', help='action (compress/decompress)', default='auto')
    parser.add_argument('--output', dest='output', default='', help='output file (default: automatic)')
    parser.add_argument('--symbol-size', dest='symbol_size', type=int, default=2,
                        help='how many bytes should be allocated for symbols (default: 2)')
    parser.add_argument('--code-size', dest='bytes_count', type=int, default=0,
                        help='bytes count for coding (default: 0)')
    args = parser.parse_args()
    action = args.action
    if args.action == 'auto':
        action = 'decompress' if os.path.splitext(args.input)[1] == '.zee' else 'compress'
    if action == 'compress':
        compress(input_file_name=args.input, output_file_name=args.output, symbols_count_bytes_number=args.symbol_size,
                 max_code_bytes_count=args.bytes_count)
    else:
        decompress(compressed_file_name=args.input, decompressed_file_name=args.output,
                   symbols_count_bytes_number=args.symbol_size)
