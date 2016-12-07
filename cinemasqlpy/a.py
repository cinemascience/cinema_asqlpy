"""
This is an apsw virtual table interface to Cinema Spec A.

In here are defined 3 things:

1. The cursor
2. The table
3. The module

You have to tell apsw about your module, which will
then allow you to attach to a cinema database and
be able to create cursors on it. The minimal setup is:

    # given a table name and path to the database with the info.json
    import apsw
    import cinemasqlpy.a as A

    conn = apsw.Connection(':memory:')
    cursor = conn.cursor()
    module = A.Module()
    conn.createmodule('CinemaA', module)

    cursor.execute('drop table if exists %s' % table)
    cursor.execute('create virtual table %s using CinemaA(%s)' % (table, path))
"""

import json
from os import path

class Cursor:
    """An apsw cursor implementation to a Cinema Spec A database."""

    # table data
    _cols = None
    _pattern = None
    _path = None
    
    # cursor data
    _rowid = None
    _limit = None
    _offsets = None
   
    def __init__(self, cols, pattern, path):
        """Takes the columns, filename pattern, and path to the cinema database."""

        self._cols = cols
        self._pattern = pattern
        self._path = path
        
        offsets = [1] * len(cols)
        for i in range(0, len(cols) - 1):
            offsets[i+1] = offsets[i] * len(cols[i])
        self._offsets = offsets
        self._limit = self._offsets[-1] * len(cols[-1])
   
    def Close(self):
        pass
   
    # Column index is used to figure out to index into the columns,
    # based on row id.
    def _column_index(self, i):
        return ((self._rowid - 1) // self._offsets[i]) % len(self._cols[i])
    
    def Column(self, num):
        if num == 0:
            args = [self._cols[i][self._column_index(i)] for i in range(0, len(self._cols))]
            return self._pattern.format(*args)
        elif num == 1:
            args = [self._cols[i][self._column_index(i)] for i in range(0, len(self._cols))]
            return self._path + self._pattern.format(*args)           
        else:
            num = num - 2
            return self._cols[num][self._column_index(num)]
    
    def Eof(self):
        return self._rowid > self._limit
    
    def Filter(self, num, name, cons):
        self._rowid = 1
    
    def Next(self):
        self._rowid = self._rowid + 1
    
    def Rowid(self):
        return rowid
    
class Table:
    """An apsw table implementation to a Cinema Spec A database."""

    # table data
    _cols = None
    _pattern = None
    _path = None
    
    def __init__(self, cols, pattern, path):
        """Takes the columns, filename pattern, and path to the cinema database."""

        self._cols = cols
        self._pattern = pattern
        self._path = path
    
    def BestIndex(self, cons, order):
        # *TODO* create some indices
        #        because it's going to be slow (everything will be a scan)
        return None
    
    def Destroy(self):
        pass
    
    def Disconnect(self):
        pass
    
    # This is where the cursor is actually created for apsw.
    def Open(self):
        return Cursor(self._cols, self._pattern, self._path)
   
    # *Unimplemented apsw functions*
    # def Begin(self)
    # def Commit(self)
    # def FindFunction(self, name, args)
    # def Rename(self)
    # def Rollback(self)
    # def Sync(self)
    # def UpdateChangeRow(self, rowid, newid, vals)
    # def UpdateDeleteRow(self, rowid)
    # def UpdateInsertRow(self, rowid, vals)
    
def read_cinema(fn):
    """Parse a Cinema Spec A database schema.
       
       Parameters
       ----------
           fn : string
           Path to the database that contains the info.json

       Side-effects
       ------------
           None.

       Returns
       -------
           (valstr, cols, pattern)
           valstr : string
               A SQL substring for describing the Cinema DB as values schema
           cols : a list of lists of values 
               The values of the range parameters in the Cinema DB
           pattern : string
               The filename pattern for columns to image filename
    """

    t = json.load(open(fn + '/info.json'))

    # *TODO* validate metadata header (I don't think the spec A sphere example is valid...)
    
    # scan for the parameters and only get the 'range' ones
    name_pairs = []
    for k, v in t['arguments'].items():
        if v['type'] == 'range':
            name_pairs.append((k, v['label']))
        # *TODO* throw an exception if not 'range'?
    name_pairs = sorted(name_pairs, key=lambda x: x[0])

    # create a pattern based on column order
    kwargs = {}
    for i, pair in zip(range(0, len(name_pairs)), name_pairs):
        kwargs[pair[0]] = '{' + str(i) + '}'
    pattern = t['name_pattern'].format(**kwargs)
    
    # create the (value) string for the create table
    # put the values into columns ordered by name_pairs (same order as value string)
    valstr = ' (filename text,full_path text,'
    cols = []
    for pair in name_pairs:
        valstr = valstr + pair[1] + ' real,'
        cols.append(sorted(t['arguments'][pair[0]]['values']))
    valstr = valstr[:-1] + ')'

    return (valstr, cols, pattern)

class Module:
    """An apsw virtual table implementation to a Cinema Spec A database."""

    _valstr = None
    _cols = None
    _pattern = None
    _path = None
    
    def __init__(self):
        pass
    
    def Create(self, conn, mod, db, name, *vtargs):
        """Takes an apsw connection, module, database, tablename, and additional
           creation arguments which are all passed via the SQL create virtual table
           command. Returns a tuple of (SQL create table string, Cinema A apsw table object).
        """

        self._path = path.dirname(vtargs[0]) 
        if self._path[-1] != '/':
            self._path = self._path + '/'
        self._valstr, self._cols, self._pattern = read_cinema(self._path)
        
        return ('create table ' + name + self._valstr, Table(self._cols, self._pattern, self._path))
    
    Connect = Create
    
