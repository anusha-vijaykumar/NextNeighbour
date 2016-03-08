from __future__ import unicode_literals
from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from time import time
from geoposition.fields import GeopositionField
from geoposition import Geoposition

#from login.views import nextvalue

# Create your models here.

# def nextvalue():
# 	cursor = connection.cursor()
# 	cursor.execute("select sequence_userid.nextval from dual")
# 	row = cursor.fetchone()
# 	return row[0]
# 
# 
# class Registration(models.Model):
# 	userid = models.IntegerField(primary_key=True, default = nextvalue)
# 	email = models.CharField(max_length=320)
# 	password = models.BinaryField(max_length=200)  # This field type is a guess.
# 	startdate = models.DateTimeField(blank=True, null=True)
# 	enddate = models.DateTimeField(blank=True, null=True)
# 
# 	class Meta:
# 		managed = False
# 		db_table = 'registration'
# 		unique_together = (('email', 'enddate'),)

def get_upload_file_name(instance, filename):
# 	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)
	return "uploaded_files/%s_%s_%s" % (instance.user, str(time()).replace('.','_'), filename)
# 	return "uploaded_files/%s_%s" % (instance.user, filename)

class UserProfile(models.Model):
# 	user = models.ForeignKey(User, unique=True, db_column = 'userid')
	user = models.OneToOneField(User, primary_key = True, db_column = 'userid')
	firstname = models.CharField(max_length = 50, blank = True)
	lastname = models.CharField(max_length = 50, blank = True)
	apt = models.CharField(max_length = 10, blank = True)
	street = models.CharField(max_length = 100, blank = True)
	city = models.CharField(max_length = 50, blank = True)
	state = models.CharField(max_length = 50, blank = True)
	zip = models.CharField(max_length = 5, blank = True)
	profle = models.TextField(blank = True)
	photopath = models.FileField(upload_to=get_upload_file_name, blank =True)
	loc = GeopositionField()
# 	loc = GeopositionField(default=Geoposition([40.77,73.98]))
	
	class Meta:
		managed = False
		db_table = ('users')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


# class Blocks(models.Model):
# 	bid = models.IntegerField(primary_key=True)
# 	blkdesc = models.CharField(max_length=100, blank=True, null=True)
# 	swc = models.TextField()  # This field type is a guess.
# 	nec = models.TextField()  # This field type is a guess.
# 	dateentered = models.DateTimeField(blank=True, null=True)
# 	isactive = models.CharField(max_length=1, blank=True, null=True)
#  
# 	class Meta:
# 		managed = False
# 		db_table = 'blocks'

# class Scope(models.Model):
#     scopeid = models.IntegerField(primary_key=True)
#     scopecd = models.CharField(max_length=1)
#     descr = models.CharField(max_length=20, blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'scope'
# 
# class Users(models.Model):
#     userid = models.ForeignKey(Registration, db_column='userid', primary_key=True)
#     firstname = models.CharField(max_length=50, blank=True, null=True)
#     lastname = models.CharField(max_length=50, blank=True, null=True)
#     apt = models.CharField(max_length=10, blank=True, null=True)
#     street = models.CharField(max_length=100)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     zip = models.CharField(max_length=5)
#     profle = models.TextField(blank=True, null=True)
#     photopath = models.CharField(max_length=300, blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'users'
		
		
# class Userrels(models.Model):
#     userid1 = models.ForeignKey('Users', related_name='userid_1', db_column='userid1')
#     userid2 = models.ForeignKey('Users',related_name='userid_2', db_column='userid2')
#     reltype = models.CharField(max_length=1)
#     isaccepted = models.CharField(max_length=1, blank=True, null=True)
#     startdate = models.DateTimeField(blank=True, null=True)
#     enddate = models.DateTimeField()
# 
#     class Meta:
#         managed = False
#         db_table = 'userrels'
#         unique_together = (('userid1', 'userid2', 'reltype', 'enddate'),)		
# 		
# 		
# class Neighbourhood(models.Model):
#     nid = models.IntegerField(primary_key=True)
#     hooddesc = models.CharField(max_length=100, blank=True, null=True)
#     swc = models.TextField()  # This field type is a guess.
#     nec = models.TextField()  # This field type is a guess.
#     dateentered = models.DateTimeField(blank=True, null=True)
#     isactive = models.CharField(max_length=1, blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'neighbourhood'
# 

# 
# 
# 
# class Blockmembers(models.Model):
# 	userid = models.ForeignKey('Users', db_column='userid')
# 	bid = models.ForeignKey('Blocks', db_column='bid')
# 	isapproved = models.CharField(max_length=1, blank=True, null=True)
# 	auser1 = models.ForeignKey('Users', related_name='auser_1', db_column='auser1', blank=True, null=True)
# 	auser2 = models.ForeignKey('Users', related_name='auser_2', db_column='auser2', blank=True, null=True)
# 	auser3 = models.ForeignKey('Users', related_name='auser_3', db_column='auser3', blank=True, null=True)
# 	startdate = models.DateTimeField(blank=True, null=True)
# 	enddate = models.DateTimeField()
# 
# 	class Meta:
# 		managed = False
# 		db_table = 'blockmembers'
# 		unique_together = (('userid', 'enddate'),)
# 
# 
# 
# 
# # class DjangoMigrations(models.Model):
#     # id = models.IntegerField(primary_key=True)  # AutoField?
#     # app = models.CharField(max_length=510, blank=True, null=True)
#     # name = models.CharField(max_length=510, blank=True, null=True)
#     # applied = models.DateTimeField()
# 
#     # class Meta:
#         # managed = False
#         # db_table = 'django_migrations'
# 
# 
# class Locality(models.Model):
#     nid = models.ForeignKey('Neighbourhood', db_column='nid')
#     bid = models.ForeignKey(Blocks, db_column='bid')
#     dateentered = models.DateTimeField(blank=True, null=True)
#     isactive = models.CharField(max_length=1, blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'locality'
#         unique_together = (('nid', 'bid'),)
# 
# class Threads(models.Model):
#     threadid = models.IntegerField(primary_key=True)
#     scopeid = models.ForeignKey(Scope, db_column='scopeid')
#     startdate = models.DateTimeField(blank=True, null=True)
#     enddate = models.DateTimeField(blank=True, null=True)
#     posted_by = models.ForeignKey('Users', db_column='posted_by')
#     subject = models.TextField(blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'threads'
# 		
# 		
# class Messages(models.Model):
#     msgid = models.IntegerField(primary_key=True)
#     textbody = models.TextField()
#     posted_by = models.ForeignKey('Users', db_column='posted_by')
#     startdate = models.DateTimeField(blank=True, null=True)
#     enddate = models.DateTimeField(blank=True, null=True)
#     loccord = models.TextField(blank=True, null=True)  # This field type is a guess.
#     threadid = models.ForeignKey('Threads', db_column='threadid')
#     title = models.TextField(blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'messages'
# 
# 
# class Msgrecipientcustom(models.Model):
#     threadid = models.ForeignKey('Threads', db_column='threadid')
#     userid = models.ForeignKey('Users', db_column='userid')
#     startdate = models.DateTimeField(blank=True, null=True)
#     enddate = models.DateTimeField()
# 
#     class Meta:
#         managed = False
#         db_table = 'msgrecipientcustom'
#         unique_together = (('threadid', 'userid', 'enddate'),)
# 
# 
# 
# 
# 
# class Notification(models.Model):
#     userid = models.ForeignKey('Users', db_column='userid')
#     scopeid = models.ForeignKey('Scope', db_column='scopeid')
#     startdate = models.DateTimeField(blank=True, null=True)
#     enddate = models.DateTimeField()
# 
#     class Meta:
#         managed = False
#         db_table = 'notification'
#         unique_together = (('userid', 'scopeid', 'enddate'),)
# 
# 
# 
# 
# 
# 
# 
# 
# class Useraccess(models.Model):
#     userid = models.ForeignKey('Users', db_column='userid', primary_key=True)
#     lastaccesstime = models.DateTimeField(blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'useraccess'
# 
# 
# 



