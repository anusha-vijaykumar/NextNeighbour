# Create your views here.
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from login.models import Registration
from login.models import Users
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle



# Create your views here.

 
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

@login_required
def home(request):
    return render_to_response(
    'frame.html',
    { 'user': request.user }
    )

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
        return HttpResponse(row)
    else:
        response = HttpResponse()
        response.write(result[2])
        response.write(" ")
        response.write(result[3])
        return response
	
# def checkproc(request):
	# cursor = connection.cursor()
	# fn = ""
	# row = cursor.callproc('sample2', [21, fn])
	# return HttpResponse(row[1])

# def login_page(request):
	# if request.method != 'POST':
		# raise Http404('Only POSTs are allowed')
	# if request.method == 'POST':
		# form = LoginForm(request.POST)
		# if form.is_valid():
			# r = Registration.objects.get(email=form.cleaned_data['email'])
			# cursor = connection.cursor()
			# if r.password == cursor.callfunc('return_hash',cx_Oracle.BINARY, [form.cleaned_data['password']]):
				# request.session['user_id'] = r.userid
				# try:
					# u = Users.objects.get(userid = r.userid)
					# request.session['firstname'] = u.firstname
					# request.session['lastname'] = u.lastname
					# cursor.close()
					# return HttpResponseRedirect('/home/')
				# except Users.DoesNotExist:
					# cursor.close()
					# return HttpResponseRedirect('/accounts/profile')
			# else:
				# cursor.close()
				# return HttpResponse("Your username and password didn't match.")
	# else:
		# form = LoginForm()
	# variables = RequestContext(request, {
	# 'form': form
    # })
 
	# return render_to_response('registration/login.html', variables,)

# def profile(request):
	# return HttpResponse("Update your profile")
	
# def logout(request):
    # try:
        # del request.session['user_id']
    # except KeyError:
        # pass
    # return HttpResponse("You're logged out.")
