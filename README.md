# Zee Code

ZCode is a custom compression algorithm I originally developed for a competition held for the Fall 2018 Datastructures
and Algorithms course of Dr. Mahdi Safarnejad-Boroujeni at Sharif University of Technology, at which I became
first-place. The code is pretty slow and has a lot of room for optimization, but it is pretty readable. It can be an
excellent educational resource for whoever is starting on compression algorithms.

The algorithm is a cocktail of classical compression algorithms mixed and served for Unicode documents. It hinges around
the LZW algorithm to create a finite size symbol dictionary; the results are then byte-coded into variable-length custom
symbols, which I call zee codes! Finally, the symbol table is truncated accordingly, and the compressed document is
encoded into a byte stream.

Huffman trees highly inspire zee codes, but because in normal texts, symbols are usually much more uniformly distributed
than the original geometrical (or exponential) distribution assumption for effective Huffman coding, the gains of using
variable-sized byte-codes both from an implementation and performance perspective outweighed bit Huffman encodings.
Results may vary, but my tests showed a steady ~4-5x compression ratio on Farsi texts, which is pretty nice!

## Installation

ZCode is available from pip, and requires only a 3.6 or higher python installation beforehand.

```shell
pip install -U zcode
```

## Usage

You can run the algorithm for any `utf-8` encoded file using the `zcode` command. It will automatically decompress files
ending with a `.zee` extensions and compress others into `.zee` files, but you can always override the default behavior
by providing optional arguments like:

```shell
zcode INPUTFILE [--output OUTPUT_FILE --action compress/decompress --symbol-size SYMBOL_SIZE --code-size CODE_SIZE]
```

The `symbol-size` argument controls the algorithms' buffer size for processing symbols (in bytes). It is automatically
set depending on your input file size but you can change it as you wish. `code-size` controls the maximum length for
coded bytes while encoding symbols (this equals to 2 by default and needs to be provided to the algorithm upon
decompression).

## LICENSE

MIT LICENSE, see [vahidzee/zcode/LICENSE](https://github.com/vahidzee/zcode/blob/main/LICENSE)