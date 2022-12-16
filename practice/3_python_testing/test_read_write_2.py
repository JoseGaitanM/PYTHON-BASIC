"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest
import importlib
module = importlib.import_module('.task_read_write_2', 'practice.2_python_part_2')
generate_file,generate_words=module.generate_file,module.generate_words

@pytest.fixture
def words():
    return generate_words()

def text(list,caracter):
    data=''
    for x in list:
        data=data+x+caracter
    return data 

def test_create_line_breaks_file(tmpdir,words):
    p = tmpdir.mkdir("sub").join("file1.txt")

    generate_file(p,'utf-8','\n',words)

    assert p.read_text(encoding='utf-8') == text(words,'\n')
    assert len(tmpdir.listdir()) == 1



def test_create_commas_file(tmpdir,words):
    p = tmpdir.mkdir("sub").join("file2.txt")

    generate_file(p,'cp1252',',',words)

    assert p.read_text(encoding='cp1252') == text(words,',')
    assert len(tmpdir.listdir()) == 1



