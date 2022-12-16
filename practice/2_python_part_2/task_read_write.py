"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os
from pathlib import Path

def create_file(path="./files"):
    path=Path(path)
    result = []

    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), 'rt') as f:
            result.append(int(f.read()))
            f.close()
    d=path/'result.txt'
    result_file=open(d, 'w')
    result_file.write(str(result)[1:-1])


if __name__ == '__main__':
    create_file()
    
