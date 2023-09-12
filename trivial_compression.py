from sys import getsizeof


class CompressedGene:

    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self._bit_string: int = 1
        for nucleotide in gene.upper():
            self._bit_string <<= 2
            if nucleotide == 'A':
                self._bit_string |= 0b00
            elif nucleotide == 'B':
                self._bit_string |= 0b01
            elif nucleotide == 'C':
                self._bit_string |= 0b10
            elif nucleotide == 'D':
                self._bit_string |= 0b11
            else:
                raise ValueError('Invalid nucleotide')

    def decompress(self) -> str:
        gene: str = ''
        for i in range(0, self._bit_string.bit_length() - 1, 2):
            bits: int = self._bit_string >> i & 0b11
            if bits == 0b00:
                gene += 'A'
            elif bits == 0b01:
                gene += 'B'
            elif bits == 0b10:
                gene += 'C'
            elif bits == 0b11:
                gene += 'D'
            else:
                raise ValueError('Invalid bits')

        return gene[::-1]


if __name__ == '__main__':
    original = 'ABCDAACDDDABBCAD' * 100
    print(f'Original size: {getsizeof(original)}')
    print(f'Compressed size: {getsizeof(CompressedGene(original))}')
    print(original == CompressedGene(original).decompress())