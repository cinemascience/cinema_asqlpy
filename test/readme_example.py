import apsw
import cinemasqlpy.a as A

table = 'cinema'
path = 'test.cdb/image/'

conn = apsw.Connection(':memory:')
cursor = conn.cursor()
module = A.Module()
conn.createmodule('Cinema', module)

cursor.execute('drop table if exists %s' % table)
cursor.execute('create virtual table %s using Cinema(%s)' % (table, path))

for row in cursor.execute('select * from %s' % table):
    print(row)

cursor.execute('select full_path from %s where phi = theta' % table)
print(cursor.fetchall())

cursor.execute('select count(*) from %s where phi > 0' % table)
print(cursor.fetchone()[0])
