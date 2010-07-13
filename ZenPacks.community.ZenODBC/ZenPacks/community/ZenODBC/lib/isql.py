#***************************************************************************
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# Based on pymssql.py from: Andrzej Kukula <akukula@gmail.com>
# Original homapage:        http://pymssql.sourceforge.net
#
#***************************************************************************
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA
#***************************************************************************

__author__ = "Egor Puzanov"
__version__ = '1.0.0'
import types, string, time, datetime, warnings, subprocess, os

### module constants

# compliant with DB SIG 2.0
apilevel = '2.0'

# module may be shared, but not connections
threadsafety = 0

# this module use extended python format codes
paramstyle = 'qmark'

### exception hierarchy

class Warning(StandardError):
	pass

class Error(StandardError):
	pass

class InterfaceError(Error):
	pass

class DatabaseError(Error):
	pass

class DataError(DatabaseError):
	pass

class OperationalError(DatabaseError):
	pass

class IntegrityError(DatabaseError):
	pass

class InternalError(DatabaseError):
	pass

class ProgrammingError(DatabaseError):
	pass

class NotSupportedError(DatabaseError):
	pass


### cursor object

class isqlCursor(object):
	"""
	This class represent a database cursor, which is used to issue queries
	and fetch results from a database connection.
	"""

	def __init__(self, src):
		"""
		Initialize a Cursor object. 'src' is a pymssqlCnx object instance.
		"""
		self.__source = src
		self._batchsize = 1
		self._rownumber = 0

	@property
	def _source(self):
		"""
		INTERNAL PROPERTY. Returns the pymssqlCnx object, and raise
		exception if it's set to None. It's easier than adding necessary
		checks to every other method.
		"""
		if self.__source == None:
			raise InterfaceError, "Cursor is closed."
		return self.__source

	@property
	def _rows(self):
		"""
		Returns last result table
		"""
		return self.__source._rows

	@property
	def _header(self):
		"""
		Returns tables description
		"""
		return self.__source._header

	@property
	def description(self):
		"""
		Returns tables description
		"""
		return self.__source._descr

	@property
	def rowcount(self):
		"""
		Returns number of rows affected by last operation. In case
		of SELECTs it returns meaningful information only after
		all rows has been fetched.
		"""
		return len(self._rows)

	@property
	def connection(self):
		"""
		Returns a reference to the connection object on which the cursor
		was created. This is the extension of the DB-API specification.
		"""
		#warnings.warn("DB-API extension cursor.connection used", SyntaxWarning, 2)
		return self._source

	@property
	def lastrowid(self):
		"""
		Returns identity value of last inserted row. If previous operation
		did not involve inserting a row into a table with identity column,
		None is returned. This is the extension of the DB-API specification.
		"""
		#warnings.warn("DB-API extension cursor.lastrowid used", SyntaxWarning, 2)
		return None

	@property
	def rownumber(self):
		"""
		Returns current 0-based index of the cursor in the result set.
		This is the extension of the DB-API specification.
		"""
		#warnings.warn("DB-API extension cursor.rownumber used", SyntaxWarning, 2)
		return self._rownumber

	def close(self):
		"""
		Closes the cursor. The cursor is unusable from this point.
		"""
		self.__source = None

	def execute(self, operation, *args):
		"""
		Prepare and execute a database operation (query or command).
		Parameters may be provided as sequence or mapping and will be
		bound to variables in the operation. Parameter style for pymssql
		is %-formatting, as in:
		cur.execute('select * from table where id=%d', id)
		cur.execute('select * from table where strname=%s', name)
		Please consult online documentation for more examples and
		guidelines.
		"""
		self._rownumber = 0  # don't raise warning

		# for this method default value for params cannot be None,
		# because None is a valid value for format string.

		if (args != () and len(args) != 1):
			raise TypeError, "execute takes 1 or 2 arguments (%d given)" % (len(args) + 1,)

		if args == (): args = ((),)

		try:
			self.executemany(operation, [args[0],])
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e

	def executemany(self, operation, param_seq):
		"""
		Execute a database operation repeatedly for each element in the
		parameter sequence. Example:
		cur.executemany("INSERT INTO table VALUES(%s)", [ 'aaa', 'bbb' ])
		"""
		self._rownumber = 0  # don't raise warning

		try:
		        queries = [operation % params for params in param_seq]
			self._source.execute_queries(queries)
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e

	def nextset(self):
		"""
		This method makes the cursor skip to the next available result set,
		discarding any remaining rows from the current set. Returns true
		value if next result is available, or None if not.
		"""

		return None

	def fetchone(self):
		"""
		Fetch the next row of a query result, returning a tuple,
		or None when no more data is available. Raises OperationalError
		if previous call to execute*() did not produce any result set
		or no call was issued yet.
		"""
		if self.description == None:
			raise OperationalError, "No data available."

		try:
			self._rownumber += 1
			return self._rows[(self._rownumber - 1)]

		except IndexError:
			return None
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e

	def fetchmany(self, size=None):
		"""
		Fetch the next batch of rows of a query result, returning them
		as a list of tuples. An empty list is returned if no more rows
		are available. You can adjust the batch size using the 'size'
		parameter, which is preserved across many calls to this method.
		Raises OperationalError if previous call to execute*() did not
		produce any result set or no call was issued yet.
		"""
		if self.description == None:
			raise OperationalError, "No data available."

		if size == None:
			size = self._batchsize

		try:
			list = []
			for i in xrange(size):
				try:
					list.append(self._rows[self._rownumber])
					self._rownumber += 1
				except IndexError:
					break
			return list
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e

	def fetchall(self):
		"""
		Fetch all remaining rows of a query result, returning them
		as a list of tuples. An empty list is returned if no more rows
		are available. Raises OperationalError if previous call to
		execute*() did not produce any result set or no call was
		issued yet.
		"""
		if self.description == None:
			raise OperationalError, "No data available."

		try:
			list = self._rows[self._rownumber:]
			self._rownumber = len(self._rows)
			return list
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e

	def __iter__(self):
		"""
		Return self to make cursors compatible with
		Python iteration protocol.
		"""
		#warnings.warn("DB-API extension cursor.__iter__() used", SyntaxWarning, 2)
		return self

	def next(self):
		"""
		This method supports Python iterator protocol. It returns next
		row from the currently executing SQL statement. StopIteration
		exception is raised when the result set is exhausted.
		With this method you can iterate over cursors:
		    cur.execute('SELECT * FROM persons')
		    for row in cur:
		        print row[0]
		"""
		#warnings.warn("DB-API extension cursor.next() used", SyntaxWarning, 2)
		if self.description == None:
			raise StopIteration, "No data available."

		try:
			header = [k[0] for k in self.description]
			self._rownumber += 1
			return self._rows[(self._rownumber - 1)]

		except IndexError:
			raise StopIteration, "No data available."
		except OperationalError, e:
			raise OperationalError, e
		except InterfaceError, e:
			raise InterfaceError, e


	def setinputsizes(self, sizes=None):
		"""
		This method does nothing, as permitted by DB-API specification.
		"""
		pass

	def setoutputsize(self, size=None, column=0):
		"""
		This method does nothing, as permitted by DB-API specification.
		"""
		pass

### connection object

class isqlCnx:
	"""
	This class represent an database connection.
	"""
	def __init__(self, args):
	        self._args = args
		self.__cnx = None
		self._queue = []
		self._result = []
		self._autocommit = True


	def __del__(self):
		if self.__cnx:
			self.close()

	@property
	def _cnx(self):
		try:
			if not self.__cnx:
				self.__cnx = subprocess.Popen(list(self._args),
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT,
							bufsize=0)
			if self.__cnx.stdin.closed:
				self.__cnx = subprocess.Popen(list(self._args),
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT,
							bufsize=0)
			return self.__cnx
		except:
			return None
	
	@property
	def _rows(self):
		if len(self._queue) > 0: self.commit()
		if not self._result: return []	
		return self._result[1:]

	@property
	def _descr(self):
		if len(self._queue) > 0: self.commit()
		if not self._result: return None	
		return tuple([ (cn, str, None, None, None, None, None) for cn in self._result[0] ])

	@property
	def _header(self):
		if len(self._queue) > 0: self.commit()
		if not self._result: return None	
		return self._result[0]

	def execute_queries(self, operations):
		self._queue.extend(operations)
	
	def close(self):
		"""
		Close connection to the database. Implicitly rolls back
		all uncommitted transactions.
		"""
		if self.__cnx:
			self.__cnx.stdin.close()
			self.__cnx.stdout.close()
			self._result = []
		self.__cnx = None

	def commit(self):
		"""
		Commit transaction which is currently in progress.
		"""
		if self._queue == []: return
		if self._cnx:
			for query in self._queue:
				self._cnx.stdin.write('%s\n'%query.strip())
			self._cnx.stdin.write('\n')
			self._queue = []
			try:
				tables = []
				wr = False
				while True:
					line = self._cnx.stdout.readline()
					if not line: break
					if line.startswith('['): raise OperationalError, ('00000', line.strip())
					elif line.strip().endswith('</font>') and wr:
						line = line.strip()[:-7]
						if line != '</font>': tables[-1][-1].append(line.strip())
					elif not line.startswith('<') and wr: tables[-1][-1].append(line.strip())
					elif line.startswith('<td'): wr = True
					elif line.startswith('</td>'): wr = False
					elif line.startswith('<tr'): tables[-1].append([])
					elif line.startswith('</tr>'): tables[-1][-1] = tuple(tables[-1][-1])
					elif line.startswith('<table'): tables.append([])
					else: pass
				self._cnx.stdin.close()
				self._result = tables[-1]
			except OperationalError, e:
				raise OperationalError, e
			except:
				self._result = []
		else:
			raise InterfaceError, "Connection is closed."
		return

	def rollback(self):
		"""
		Roll back transaction which is currently in progress.
		"""
		self._queue = []
		return

	def cursor(self):
		"""
		Return cursor object that can be used to make queries and fetch
		results from the database.
		"""
		return isqlCursor(self)

	def autocommit(self,status):
		"""
		Turn autocommit ON or OFF.
		"""
		if status:
			if self._autocommit == False:
				self._autocommit = True
		else:
			if self._autocommit == True:
				self._autocommit = False


class connectionString:
    
	def __init__(self, cs, uid=None, pwd=None):
		self.uid = uid
		self.pwd = pwd
		self.dsn = None
		options = {}
		for item in cs.split(';'):
			var,val = tuple([i.strip() for i in item.split('=')])
			if var.upper() == 'UID' and not self.uid: self.uid = val
			elif var.upper() == 'PWD' and not self.pwd: self.pwd = val
			elif var.upper() == 'DSN': self.dsn = val
			elif var.upper() == 'FILEDSN': self.dsn = val
			elif var.upper() == 'DRIVER': options[var] = val.strip('{}')
			else: options[var] = val
		if not self.dsn:
			import md5
			newcs = ';'.join(['%s = %s'%o for o in options.iteritems()])
			self.dsn = md5.new(newcs).hexdigest()
			f = open(os.path.expanduser('~/.odbc.ini'), 'a+')
			while True:
				line = f.readline()
				if not line:
					f.write('[%s]\n'%self.dsn)
					for option in options.iteritems():
						f.write('%s = %s\n'%option)
					break
				if line.startswith('[%s]'%self.dsn): break
			f.close()

	def isqlArgs(self):
		ret = [self.dsn,]
		if self.uid is not None:
			ret.append(self.uid)
			if self.pwd is not None: ret.append(self.pwd)
		return ret


# connects to a database
def connect(cs = None, uid = None, pwd = None):
		    
	"""
	Constructor for creating a connection to the database. Returns
	a connection object. Paremeters are as follows:

	cs        connection string
	          primarily for compatibility with previous versions of pymssql.
	uid       database user to connect as
	pwd       user's password
	
	Examples:
	con = pymssql.connect(cs='DRIVER={MySQL};OPTION=3;PORT=3307;Database=information_schema;SERVER=127.0.0.1',
	                      uid='username',
                              pwd='P@ssw0rd')
	"""
	# first try to get params from CS

	cs = connectionString(cs, uid, pwd)
        args =  ("isql",) + tuple(cs.isqlArgs()) + ("-c", "-w", "-b")
	return isqlCnx(args)
