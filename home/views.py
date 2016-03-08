# Create your views here.
from login.forms import *
from home.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from login.models import Blocks
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle
from nextnbr.settings import MEDIA_URL
from decimal import Decimal
from profileapp.models import UserProfile
from home.models import Blockmembers
from home.models import Messages

# from django.contrib.gis.geos import polygon



# Create your views here.
@login_required
def homepage(request):
	cursor = connection.cursor()
	m = request.session['userid']
	prfl = request.user.profile
	if not prfl.firstname:
		return HttpResponseRedirect('/accounts/profile/', {'alert' : True})
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allthreads', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('home.html',{'row':row,'user': request.user})
	#n = notification.objects.filter(user=request.user, viewed=False)
	#return render_to_response(
	#'home.html',
	#{ 'user': request.user,#'notification':n 
	#}
	#)
@login_required	
def msg(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allfeeds', [m,x,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('msg.html',{'row':row,'user': request.user})


	
@login_required
def home(request):
	u = User.objects.get(username = request.user)
	request.session['userid'] = u.id
	return render_to_response('frame.html',{ 'user': request.user})
	
@login_required
def ho(request):
	prfl = request.user.profile
	return render_to_response('ho.html',{ 'user': request.user, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })

	

	
def allfeeds(request):
	return render_to_response(
    'allfeeds.html',
    { 'user': request.user }
    )

#def getid(request):
#	cursor=connection.cursor()
#	cursor.execute("select id from auth_user where username=request.user")
#	row=cursor.fetchone()
#	return HttpResponse(row)
	
def friends(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndscur = cursor.var(cx_Oracle.CURSOR).var
 #     cursor.callproc('showfriends', [21, 'frnds_cursor', err_cd, err_msg])
	result = cursor.callproc('showfriends', [m,frndscur, err_cd, err_msg])
	if result[2] == '0':
		row = result[1].fetchall()
	#	return HttpResponse(row)
		#variables = RequestContext(request, {'id': row})
		#return render_to_response('friends.html',variables,)
		#return render_to_response('friends.html',{'id':row})
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
		#return response
	return render_to_response('friends.html',{'id':row})

	
def neighbours(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	neighscur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showneighbours', [m,neighscur, err_cd, err_msg])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbours.html',{'id':row})
	

def blocks(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	neighscur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showblocks', [m, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[1] == '1':
		return render_to_response('blocks.html',{'row':result[2]})
	if result[1] == '2':
		return render_to_response('blocks.html',{'row':result[2]})
	if result[1] == '3':
		return render_to_response('blocks.html',{'row':result[2]})
	if result[1] == '0':
		lat = request.user.profile.loc.latitude
		lng = request.user.profile.loc.longitude
		listblks = []
		blks = Blocks.objects.all()
		for x in blks:
			ymax = Decimal(x.nec.latitude)
			xmax = Decimal(x.nec.longitude)
			ymin = Decimal(x.swc.latitude)
			xmin = Decimal(x.swc.longitude)
#         rx = range(xmax, xmin)
#         ry = range(ymax, ymin)
			if lng >= xmax and lng <= xmin and lat >= ymax and lat <= ymin :
				listblks.append(x)
# 		return HttpResponse(listblks[0].bid)
#     ne =nec.split(',')[0] request.user.profile.loc.latitude
#     sw = request.user.profile.loc.longitude
#     bbox = ("XMIN = " ,xmin," YMIN = ", ymin, " XMAX  = ", xmax, " YMAX ",  ymax)
#     geom = Polygon.from_bbox(bbox)
#     return HttpResponse(bbox)
		return render_to_response('blocklist.html',{'row':listblks})
		

def friendrequest(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	notifycur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showfrndreq', [m,notifycur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('friendrequest.html',{'row':row})
	
def addnbrlist(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkmembrs = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showblkmembers', [m,blkmembrs, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('nbrlist.html',{'row':row})

def addnbr(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('addnbr', [m,x, err_cd, err_msg])
	if result[2] == '0':
		msg = 'Neighbour added'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})
	
def notifications(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	notifycur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('notificationdisplay', [m,notifycur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
		msg=''
	else:
# 		response = HttpResponse()
# 		response.write(result[2])
# 		response.write(" ")
# 		response.write(result[3])
		row = ''
		msg='Error in displaying notifications'
	return render_to_response('notifications.html',{'row':row, 'msg':msg})
	
	
def acceptfrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('friendaccept', [x,m,'Y', err_cd, err_msg])
	if result[3] == '0':
		msg = 'Accept request completed'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})
	
	
	
def acceptblkreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT bid FROM blockmembers where userid = %s", [m])
		bid = int(cursor.fetchone()[0])
# 		return HttpResponse(bid[0])
# 	return HttpResponse(row)
	except:
		msg = 'Error selecting BlockId'
		html = "<html><body>ERROR %s. <a href='/homepage/'>Home</a></body></html>" % msg
		return HttpResponse(html)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('blockapproval', [x,bid,m,err_cd,err_msg ])
	if result[3] == '0':
		msg = 'Request completed'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})
	
	
def sendblkreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('blockrequest', [m,x, err_cd, err_msg])
# 	return HttpResponse(result[2])
	if result[2] == '0':
		msg = 'Block request sent'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})

	
def unjoinblkreq(request, x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('unjoinblk', [m, err_cd, err_msg])
	if result[1] == '0':
		msg = 'Unjoin request completed'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})
	
def declinefrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('friendaccept', [x, m, 'D', err_cd, err_msg])
	if result[3] == '0':
		msg = 'Decline request completed'
#         return HttpResponse(row)
	else:
		msg = 'Error in completing your request'
	return render_to_response('template2.html', {'msg' : msg})

	
def messages(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		choice = request.POST['choice']
		#return HttpResponse(choice)
		request.session['ch'] = choice
		if choice == 'R' or choice == 'E':
			return HttpResponseRedirect("/newmsg/")
		else:
			return HttpResponseRedirect("/newms/")
		
	else:
		form = MessageForm()
	variables = RequestContext(request, {
	'form': form,
	})
	return render_to_response(
	'msgsuccess.html',
	variables,
	)
	
def newmsg(request):
	error = request.session['ch']
	if request.method == 'POST':
		form = NewmessageForm(request.POST)
		username = request.POST['username']
		title = request.POST['title']
		textbody = request.POST['textbody']
		if request.POST['loccord_0']:
			loccord  = request.POST['loccord_0']  + "," +  request.POST['loccord_1']
		else:
			loccord = None
		request.session['uname']=username
		request.session['title']=title
		request.session['text']=textbody
		request.session['loccord']=loccord
		#return HttpResponse(user)
		#choice = request.POST['choice']
		if form.is_valid:
			#form.save()
			return HttpResponseRedirect('/message/')
	else:
		form = NewmessageForm()
		
	variables = RequestContext(request, {
	'form': form
	})

	return render_to_response(
	'messages.html',
	variables,
	)
	
def message(request):
	choice = request.session['ch']
	username = request.session['uname']
	title = request.session['title']
	textbody = request.session['text']
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('chkfrndnbr', [m,username,choice,err_cd, err_msg])
	#return HttpResponse(result[3])
	if result[3] == '2':
		return HttpResponseRedirect('/newestmessage/')
	if result[3] == '3':
		return render_to_response('error.html',{'err_msg':err_msg})
	else:
		msg = 'You cant send message to this user!!!!!SORRY(your are neither friends or neighbours with the mentioned user'
		html = "<html><body>ERROR %s. <a href='/homepage/'>Home</a></body></html>" % msg
		return HttpResponse(html)

	
	
def newms(request):
	if request.method == 'POST':
		form = NewmessagesForm(request.POST)
		title = request.POST['title']
		textbody = request.POST['textbody']
		if request.POST['loccord_0']:
			loccord  = request.POST['loccord_0']  + "," +  request.POST['loccord_1']
		else:
			loccord = None
		request.session['loccord']=loccord
		request.session['title'] = title
		request.session['textbody'] = textbody
		return HttpResponseRedirect('/blknbrmsg/')
	else:
		form = NewmessagesForm()
	variables = RequestContext(request, {
	'form': form,
	})
 
	return render_to_response(
	'messagemany.html',
	variables,
	)
	
	
def blknbrmsg(request):
	choice = request.session['ch']
	cursor = connection.cursor()
	#return HttpResponse(choice)
	m = request.session['userid']
	title = request.session['title']
	textbody = request.session['textbody']
	loccord = request.session['loccord']
	n = None
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	result = cursor.callproc('newmsg', [m,title,textbody,choice,n, loccord, err_cd, err_msg])
# 	return HttpResponse(result[6])
	if result[5] == '0':
		return render_to_response('newbnmsgsent.html')
	else:
		response = HttpResponse()
		response.write(result[5])
		response.write(" ")
		response.write(result[6])
		row=''
	return render_to_response('newbnmsgsent.html')
	
def newestmessage(request):
	cursor = connection.cursor()
	choice = request.session['ch']
	#return HttpResponse(choice)
	m = request.session['userid']
	username = request.session['uname']
	title = request.session['title']
	textbody = request.session['text']
	loccord = request.session['loccord']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('newmsg', [m,title,textbody,choice,username, loccord, err_cd, err_msg])
	#return HttpResponse(result[5])
	if result[5] == '0':
		return render_to_response('newmsgsent.html')
	else:
		response = HttpResponse()
		response.write(result[5])
		response.write(" ")
		response.write(result[6])
		row=''
	return render_to_response('newmsgsent.html')
	
def frequest(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	cursor.callproc('updatefrnd', [m,x, err_cd, err_msg])
	variables = RequestContext(request, {'x':x})
	return render_to_response('template.html')
	#return HttpResponse(result[2])
	
	
def reply(request,x):
	request.session['x']=x
	if request.method == 'POST':
		form = NewmessagesForm(request.POST)
		title = request.POST['title']
		textbody = request.POST['textbody']

		if request.POST['loccord_0']:
			loccord  = request.POST['loccord_0']  + "," +  request.POST['loccord_1']
		else:
			loccord = None
		request.session['loccord']=loccord
		#return HttpResponse(textbody)
		request.session['title']=title
		request.session['text']=textbody
			#form.save()
		return HttpResponseRedirect('/replymessage/')
	else:
		form = NewmessagesForm()
	variables = RequestContext(request, {
	'form': form,
	})
	return render_to_response(
	'reply.html',
	variables,
	)
	
	
def replymessage(request):
	cursor = connection.cursor()
	m = request.session['userid']
	x = request.session['x']
	title = request.session['title']
	textbody = request.session['text']
	loccord = request.session['loccord']
	#return HttpResponse(request.session['title'])
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('replymsg', [x,m,title,textbody, loccord, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[4] == '0':
		return render_to_response('replymsgsent.html')
	else:
		response = HttpResponse()
		response.write(result[4])
		response.write(" ")
		response.write(result[5])
		row=''
	return render_to_response('replymsgsent.html')
	# cursor = connection.cursor()
	# m = request.session['userid']
	# #return HttpResponse(m)
	# err_cd = cursor.var(cx_Oracle.NUMBER).var
	# err_msg = cursor.var(cx_Oracle.STRING).var
	# frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	# result = cursor.callproc('replymsg', [x,m,frndthreadcur, err_cd, err_msg])
	# #return HttpResponse(result[1])
	# if result[2] == '0':
		# row = result[1].fetchall()
	# else:
		# response = HttpResponse()
		# response.write(result[2])
		# response.write(" ")
		# response.write(result[3])
		# row=''
	# return render_to_response('.html',{'row':row})
	
	
#def reply(request):
#	if request.method == 'POST':
#		form = NewmessagesForm(request.POST)
#		return HttpResponseRedirect('/messages.html/')
#	else:
#		form = NewmessagesForm()
#	variables = RequestContext(request, {
#	'form': form,
#	})
#
#	return render_to_response(
#	'messages.html',
#	variables,
#	)
	
	
#def msgsuccess(request):
#	cursor = connection.cursor()
#	m = request.session['userid']
#	err_cd = cursor.var(cx_Oracle.NUMBER).var
#	err_msg = cursor.var(cx_Oracle.STRING).var
#	showcur = cursor.var(cx_Oracle.CURSOR).var
#	result = cursor.callproc('newmsg', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
#	if result[2] == '0':
#		row = result[1].fetchall()
#	else:
#		response = HttpResponse()
#		response.write(result[2])
#		response.write(" ")
#		response.write(result[3])
#		row=''
#	return render_to_response('success.html',{'row':row})
	
	
def blockthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('blockthreads', [m,blkthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('blockthreads.html',{'row':row})
	
	
def friendthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('friendthreads', [m,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
# 		return HttpResponse(row)
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('friendthreads.html',{'row':row})
	
	
def next(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('blockfeeds', [m,x,blkthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('next.html',{'row':row,'x':x})
	
def togo(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('friendfeeds', [m,x,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('togo.html',{'row':row,'x':x})
	
	
def neighbourhoodthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourhoodthreads', [m,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[0])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbourhoodthreads.html',{'row':row})
	
	
	
def neighbourthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourthreads', [m,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbourthreads.html',{'row':row})
	
def allthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	allthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allthreads', [m,allthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('allthreads.html',{'row':row})
	
	
def to(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourfeeds', [m,x,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('nbrfeeds.html',{'row':row,'x':x})
	
	
def go(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourhoodfeeds', [m,x,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('go.html',{'row':row,'x':x})
	
	
def oo(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	allthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allfeeds', [m,x,allthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('oo.html',{'row':row,'x':x})

	
def show(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('show', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('home.html',{'row':row})
	
	
def newmessage(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		answer = form.cleaned_data['choices']
		variables = RequestContext(request, {'form': form})
		return render_to_response('next.html',variables)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            request.session['email'] = form.cleaned_data['email']       
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )


def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

# @login_required
# def home_1(request):
# #     filename = "C:\Users\Vasundhara Patil\Documents\GitHub\next\media\uploaded_files\ab1_1449302455_874656_Frozen_Queen_Elsa_Wallpaper.jpg"
#     u = User.objects.get(username = request.user)
#     request.session['userid'] = u.id
#     prfl = request.user.profile
#     if not prfl.firstname:
#         return HttpResponseRedirect('/accounts/profile/', {'alert' : True})
# #     image_name = "uploaded_files/Frozen_Queen_Elsa_Wallpaper.jpg"
#     return render_to_response('home_1.html',{ 'user': request.user, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })


# def blockrequest(request):
#     lat = request.user.profile.loc.latitude
#     lng = request.user.profile.loc.longitude
#     listblks = []
#     blks = Blocks.objects.all()
#     for x in blks:
#         ymax = Decimal(x.nec.split(',')[0])
#         xmax = Decimal(x.nec.split(',')[1])
#         ymin = Decimal(x.swc.split(',')[0])
#         xmin = Decimal(x.swc.split(',')[1])
# #         rx = range(xmax, xmin)
# #         ry = range(ymax, ymin)
#         if lng >= xmax and lng <= xmin and lat >= ymax and lat <= ymin :
#              listblks.append(x)
# #     ne =nec.split(',')[0] request.user.profile.loc.latitude
# #     sw = request.user.profile.loc.longitude
# #     bbox = ("XMIN = " ,xmin," YMIN = ", ymin, " XMAX  = ", xmax, " YMAX ",  ymax)
# #     geom = Polygon.from_bbox(bbox)
# #     return HttpResponse(bbox)
#     return HttpResponse(listblks)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            err_cd = cursor.var(cx_Oracle.NUMBER).var
            err_msg = cursor.var(cx_Oracle.STRING).var
            findmsgcur = cursor.var(cx_Oracle.CURSOR).var
#             return HttpResponse(request.POST['search'])
#     cursor.callproc('showfriends', [21, 'frnds_cursor', err_cd, err_msg])
            result = cursor.callproc('findmsg', [request.POST['search'],request.session['userid'], findmsgcur, err_cd, err_msg])
#             result = cursor.callproc('showfriends', [request.session['userid'], findmsgcur, err_cd, err_msg])
#             return HttpResponse(result[2]['msgid'])
            if result[3] == '0':
                row = result[2].fetchall()
#                 return HttpResponse(row[0][0])
                return render_to_response('search_msgs.html', {'msgs' : row})

            else:
                response = HttpResponse()
                response.write(result[3])
                response.write(" ")
                response.write(result[4])
                row = ''
#                 return response
                return render_to_response('search_msgs.html', {'msgs' : row})
    else:
        form = SearchForm(initial = {'search' : ""})
    variables = RequestContext(request, {
    'form': form
    })
  
    return render_to_response(
    'search.html',
    variables,
    )
    
def mapview(request):
# 	msg = Messages.objects.exclude(loccord=None)	
# 	for x in msg:
# 		x.textbody = (x.textbody).replace('\n', ' ').replace('\r', '')
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allfeedsMap', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		msg = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		msg=''
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkmembrs = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showallblkmembersaddr', [m,blkmembrs, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		blkmbr = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		blkmbr=''
	listblk = []
	blks = Blocks.objects.all()
# 	return HttpResponse(blks[0].swc.latitude)
	for x in blks:
# 		north = x.nec.split(',')[0]
# 		east = x.nec.split(',')[1]
# 		south = x.swc.split(',')[0]
# 		west = x.swc.split(',')[1]
		listblk.append(x)
# 		listblk.append({'north': north, 'south' : south, 'east' : east, 'west' : west})
# 	return HttpResponse(listblk[0]['north'])
# 	return HttpResponse(blkmbr[0][4])		
# 	return HttpResponse(msg)
	return render_to_response('mapview.html', {'msg' : msg, 'blkmbr' : blkmbr, 'listblk' : listblk, 'MEDIA_URL' : MEDIA_URL} )

def msgmap(request, x):
	msg = Messages.objects.get(msgid = x)
	u = User.objects.get(id = msg.posted_by)
	return render_to_response('viewmsg.html', {'msg' : msg, 'u' : u})
		

#     
# def viewmsg(request):
#         if request.method == 'POST':
#             return HttpResponse(request.POST)
#         f = 0
#         variables = RequestContext(request, {'form': f})
#   
#     return render_to_response('viewmsg.html',variables,)
        

def checkproccur(request):
    cursor = connection.cursor()
	# l_cursor = cx_Oracle.CURSOR
    err_cd = cursor.var(cx_Oracle.NUMBER).var
    err_msg = cursor.var(cx_Oracle.STRING).var
    frndscur = cursor.var(cx_Oracle.CURSOR).var
#     cursor.callproc('showfriends', [21, 'frnds_cursor', err_cd, err_msg])
    result = cursor.callproc('showfriends', [2,frndscur, err_cd, err_msg])
    if result[2] == '0':
        row = result[1].fetchall()
#         return HttpResponse(row)
    else:
        response = HttpResponse()
        response.write(result[2])
        response.write(" ")
        response.write(result[3])
        row = ''
#         return response
    return render_to_response('checkproccur.html',{'row': row}
    )

	
# def checkproc(request):
	# cursor = connection.cursor()
	# fn = ""
	# row = cursor.callproc('sample2', [21, fn])
	# return HttpResponse(row[1])


# def profile(request):
	# return HttpResponse("Update your profile")
	
# def logout(request):
    # try:
        # del request.session['user_id']
    # except KeyError:
        # pass
    # return HttpResponse("You're logged out.")
