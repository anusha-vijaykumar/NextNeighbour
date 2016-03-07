from django.http import HttpResponse
import logging
import cx_Oracle

def run():
	con = cx_Oracle.connect(dsn=cx_Oracle.makedsn('localhost', '1521', 'orcl'), user='SYS', password='Passw0rd', mode=cx_Oracle.SYSDBA)
	cur=con.cursor()
	cur.execute("ALTER PLUGGABLE DATABASE pdborcl OPEN read write force")
	con.close()
	print("Hello")