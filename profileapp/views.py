# Create your views here.
from profileapp.forms import *
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

 
def profile(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			user = 'hi'
			return HttpResponseRedirect('/home/')
	else:
		form = ProfileForm()
	variables = RequestContext(request, {'form': form})
	return render_to_response('profile.html',variables,)

