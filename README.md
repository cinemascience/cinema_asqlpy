Cinema Spec A SQL for Python (cinemasqlpy)
=========================================

*cinemasqlpy* is a package that allows *SQL* queries
on *Cinema* Spec A databases in *Python*.

It does so by building a "virtual table" interface to
*Cinema* to *SQLite* via *apsw* (a *SQLite* interface
in Python that allows virtual tables).

If you are not familiar with *Cinema*, please see
http://cinemascience.org

If you are not familiar with *SQL* or *SQLite*,
please see http://sqlite.org

Currently, this package only supports *SQL* queries
on *Cinema* Spec A through *Python*.

*Installation*
==============

1. Install *apsw*

   *cinemasqlpy* is dependent on *apsw* and should be
   installed prior to using this package. The author
   of *apsw* suggests cloning the repository and installing
   from the repo. There is a *pypi* package, but
   it is not maintained by the author.

   ```bash
   $ git clone https://github.com/rogerbinns/apsw.git
   $ cd apsw
   $ pip install .
   ```

2. Install *cinemasqlpy*

   ```bash
   $ git clone https://github.com/dhrogers/cinemasqlpy.git
   $ cd cinemasqlpy
   $ pip install .
   ```

*Example Spec A Usage*
======================

```python
import apsw
import cinemasqlpy.a as A

table = 'cinema'
path = '/home/user/mycinema.cdb/image/'

conn = apsw.Connection(':memory:')
cursor = conn.cursor()
module = A.Module()
conn.createmodule('Cinema', module)

cursor.execute('drop table if exists %s' % table)
cursor.execute('create virtual table %s using Cinema(%s)' % (table, path))

for row in cursor.execute('select * from cinema'):
    print(row)

cursor.execute('select full_path from cinema where phi = theta')
print(cursor.fetchall())

cursor.execute('select count(*) from cinema where phi > 0')
print(cursor.fetchone()[0])
```

More examples can be found in the *test/* directory.
