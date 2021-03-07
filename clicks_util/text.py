from clicks_util import numbers
import string
import numbers

def split(sentence, num_chunks: int = 0):
    """Split the given sentence into num_chunk pieces.

    If the length of the sentence is not exactly divisible by
    num_chunks, some slices will be 1 character shorter than
    the others.
    https://codereview.stackexchange.com/questions/145489/slicing-a-string-into-three-pieces-and-also-controlling-manipulating-through-lo
    """
    if not num_chunks:
        num_chunks = numbers.find_lowest_under(len(sentence))
    size, remainder = divmod(len(sentence), num_chunks)
    chunks_sizes = [size + 1] * remainder + [size] * (num_chunks - remainder)
    offsets = [sum(chunks_sizes[:i]) for i in range(len(chunks_sizes))]

    return [sentence[o:o+s] for o, s in zip(offsets, chunks_sizes)]

all_letters = string.ascii_letters
all_digits = string.digits