import spec_a_examples as A
from pytest import fixture
from os import path
from shutil import copytree

@fixture
def data_copy(tmpdir, request):
    test_dir = path.dirname(request.module.__file__) 
    temp_dst, _ = path.splitext(path.basename(request.module.__file__))
    copytree(test_dir + '/test.cdb/', str(tmpdir) + '/' + temp_dst + '/test.cdb/')
    db = str(tmpdir) + '/' + temp_dst + '/test.cdb/image/'
    return db

def test_1(data_copy):
    assert A.read_cinema_json(data_copy) == (' (filename text,full_path text,phi real,theta real)', [[-180, -162, -144, -126, -108, -90, -72, -54, -36, -18, 0, 18, 36, 54, 72, 90, 108, 126, 144, 162], [0]], '{0}/{1}.png')

def test_2(data_copy):
    assert A.select_all_rows(A.cinema_cursor(data_copy)) == [('-180/0.png', -180.0, 0.0), ('-162/0.png', -162.0, 0.0), ('-144/0.png', -144.0, 0.0), ('-126/0.png', -126.0, 0.0), ('-108/0.png', -108.0, 0.0), ('-90/0.png', -90.0, 0.0), ('-72/0.png', -72.0, 0.0), ('-54/0.png', -54.0, 0.0), ('-36/0.png', -36.0, 0.0), ('-18/0.png', -18.0, 0.0), ('0/0.png', 0.0, 0.0), ('18/0.png', 18.0, 0.0), ('36/0.png', 36.0, 0.0), ('54/0.png', 54.0, 0.0), ('72/0.png', 72.0, 0.0), ('90/0.png', 90.0, 0.0), ('108/0.png', 108.0, 0.0), ('126/0.png', 126.0, 0.0), ('144/0.png', 144.0, 0.0), ('162/0.png', 162.0, 0.0)] 

def test_3(data_copy):
    assert A.select_paths(A.cinema_cursor(data_copy)) == [(data_copy + '-180/0.png', '-180/0.png'), (data_copy + '-162/0.png', '-162/0.png'), (data_copy + '-144/0.png', '-144/0.png'), (data_copy + '-126/0.png', '-126/0.png'), (data_copy + '-108/0.png', '-108/0.png'), (data_copy + '-90/0.png', '-90/0.png'), (data_copy + '-72/0.png', '-72/0.png'), (data_copy + '-54/0.png', '-54/0.png'), (data_copy + '-36/0.png', '-36/0.png'), (data_copy + '-18/0.png', '-18/0.png'), (data_copy + '0/0.png', '0/0.png'), (data_copy + '18/0.png', '18/0.png'), (data_copy + '36/0.png', '36/0.png'), (data_copy + '54/0.png', '54/0.png'), (data_copy + '72/0.png', '72/0.png'), (data_copy + '90/0.png', '90/0.png'), (data_copy + '108/0.png', '108/0.png'), (data_copy + '126/0.png', '126/0.png'), (data_copy + '144/0.png', '144/0.png'), (data_copy + '162/0.png', '162/0.png')]

def test_4(data_copy):
    assert A.get_schema(A.cinema_cursor(data_copy)) == [(0, 'filename', 'text', 0, None, 0), (1, 'full_path', 'text', 0, None, 0), (2, 'phi', 'real', 0, None, 0), (3, 'theta', 'real', 0, None, 0)]

def test_5(data_copy):
    assert A.range_phi_query(A.cinema_cursor(data_copy)) == [('18/0.png',), ('36/0.png',), ('54/0.png',), ('72/0.png',), ('90/0.png',), ('108/0.png',), ('126/0.png',), ('144/0.png',), ('162/0.png',)]

def test_6(data_copy):
    assert A.same_phi_theta_query(A.cinema_cursor(data_copy)) == [(0.0, 0.0, data_copy + '0/0.png')]

def test_7(data_copy):
    assert A.inner_join(A.cinema_cursor(data_copy)) == [('0/0.png', data_copy + '0/0.png')]

