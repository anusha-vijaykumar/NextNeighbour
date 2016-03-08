from __future__ import unicode_literals
from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from profileapp.models import UserProfile
from geoposition.fields import GeopositionField
from geoposition import Geoposition



class Messages(models.Model):
	msgid = models.IntegerField(primary_key = True)
	textbody = models.TextField(blank = True)
	posted_by = models.IntegerField(blank = True)
	loccord = GeopositionField(blank = True)
	threadid = models.IntegerField(blank = True)
	title = models.TextField(blank = True)
	
	class Meta:
		managed = False
		db_table = 'messages'
		


# Create your models here.
class Blockmembers(models.Model):
	userid = models.ForeignKey('UserProfile', db_column='userid')
	bid = models.ForeignKey('Blocks', db_column='bid')
	isapproved = models.CharField(max_length=1, blank=True, null=True)
	auser1 = models.ForeignKey('Users', related_name='auser_1', db_column='auser1', blank=True, null=True)
	auser2 = models.ForeignKey('Users', related_name='auser_2', db_column='auser2', blank=True, null=True)
	auser3 = models.ForeignKey('Users', related_name='auser_3', db_column='auser3', blank=True, null=True)
	startdate = models.DateTimeField(blank=True, null=True)
	enddate = models.DateTimeField()
 
	class Meta:
		managed = False
		db_table = 'blockmembers'
		unique_together = (('userid', 'enddate'),)