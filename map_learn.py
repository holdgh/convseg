import numpy as np


def print_iterator(iterator):
    for item in iterator:
        print(item)


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5]
    b = map(float, a)
    print_iterator(b)
    c = np.array(b)
    print_iterator(c)
