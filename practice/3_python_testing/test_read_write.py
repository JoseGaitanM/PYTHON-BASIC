"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import pytest
from pathlib import Path
import importlib
module = importlib.import_module('.task_read_write', 'practice.2_python_part_2')
create_file=module.create_file

data_test_files=[23,78,3]

#We create temp files with data_test_files
@pytest.fixture
def files(tmpdir):
    d = tmpdir.mkdir("sub")

    i=1
    for n in data_test_files:
        p = d / ("file_"+str(i)+".txt")
        p.write_text(str(n),encoding='utf-8')
        i=i+1

    return d

#We read the temp files and the content of each for create result.txt
def test_result_file(files):
    create_file(files)
    
    p=files/'result.txt'

    assert p.read_text(encoding='utf-8') == '23, 78, 3'