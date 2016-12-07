import apsw
import cinemasqlpy.a as A

# open a connection to the cinema database
def cinema_cursor(path):
    conn = apsw.Connection(':memory:')
    cursor = conn.cursor()
    module = A.Module()
    conn.createmodule('Cinema', module)

    cursor.execute('drop table if exists cinema')
    cursor.execute('create virtual table cinema using Cinema(%s)' % path)

    return cursor

def read_cinema_json(path):
    return A.read_cinema(path)

def select_all_rows(cursor):
    cursor.execute('select filename,phi,theta from cinema')
    return cursor.fetchall()

def select_paths(cursor):
    cursor.execute('select full_path,filename from cinema')
    return cursor.fetchall()

def get_schema(cursor):
    cursor.execute('pragma table_info(cinema)')
    return cursor.fetchall()

def range_phi_query(cursor):
    return [row for row in cursor.execute('select filename from cinema where phi > 0')]

def same_phi_theta_query(cursor):
    result = []
    for row in cursor.execute('select phi,theta,full_path from cinema where phi = theta'):
        result.append(row)
    return result

def inner_join(cursor):
    cursor.execute('select a.filename, b.full_path from cinema as a, cinema as b where a.phi = b.phi and a.phi = b.theta')
    return cursor.fetchall()

if __name__ == '__main__':
    path = 'test.cdb/image/' 
    print(read_cinema_json(path))

    cursor = cinema_cursor(path)

    print(select_all_rows(cursor))
    print(select_paths(cursor))
    print(get_schema(cursor))
    print(range_phi_query(cursor))
    print(same_phi_theta_query(cursor))
    print(inner_join(cursor))
