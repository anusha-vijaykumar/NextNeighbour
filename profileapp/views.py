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
# from login.models import Registration
# from login.models import Users
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle
import requests
from django.core.exceptions import ValidationError
import os
from nextnbr.settings import MEDIA_URL




# Create your views here.
@login_required
def viewownprofile(request):
#     filename = "C:\Users\Vasundhara Patil\Documents\GitHub\next\media\uploaded_files\ab1_1449302455_874656_Frozen_Queen_Elsa_Wallpaper.jpg"
    u = User.objects.get(username = request.user)
    request.session['userid'] = u.id
    prfl = request.user.profile
    return render_to_response('viewprofile.html',{ 'user': request.user, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })

@login_required
def viewfrndprofile(request, x):
#     filename = "C:\Users\Vasundhara Patil\Documents\GitHub\next\media\uploaded_files\ab1_1449302455_874656_Frozen_Queen_Elsa_Wallpaper.jpg"
	u = User.objects.get(id = x)
	prfl = u.profile
	return render_to_response('viewprofile.html',{ 'user': u, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })
    
@login_required
def viewmapprofile(request, x):
#     filename = "C:\Users\Vasundhara Patil\Documents\GitHub\next\media\uploaded_files\ab1_1449302455_874656_Frozen_Queen_Elsa_Wallpaper.jpg"
    u = User.objects.get(id = x)
    prfl = u.profile
    return render_to_response('viewmapprofile.html',{ 'user': u, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })


def profile(request):
	u = User.objects.get(username = request.user)
	alert = False
	if request.method == 'POST':
		usern_form = UserForm(request.POST, request.FILES, prefix = "usern", initial = {'username' : request.user, 'email' : u.email})
		up_form = ProfileForm(request.POST, request.FILES, prefix = "up", instance=request.user.profile, initial = {'use_map' : False})
# 		form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
# 		return HttpResponse(request.FILES.get('photopath', False).name)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/home/')
# 		r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=270%20Marin%20Blvd%20Jersey%20City%20NJ%2007302&sensor=false')
# 		return HttpResponse(r.json()['results'][0]['geometry']['location']['lat'])
# 		return HttpResponse(request.POST)
######### To check if user has used map to give address #####################
		try:
			chk = request.POST['up-use_map']
		except:
			request.POST['up-use_map'] = 'off'
			chk = request.POST['up-use_map']

		try:
			if chk == 'on':
				r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng=' + request.POST['up-loc_0'] + ',' + request.POST['up-loc_1'] + '&sensor=false')
# 				return HttpResponse(r.text)
				if r.json()['status'] != 'OK':
					msg = 'Select proper location'
					html = "<html><body>ERROR %s. <a href='/accounts/profile/'>Home</a></body></html>" % msg
					return HttpResponse(html)
				addr = r.json()['results'][0]['address_components']
# 				return HttpResponse(addr)
				apt = ''
				street1 = ''
				street2 = ''
				city = ''
				state = ''
				zip = ''
				for x in addr:
					if 'subpremise' in x['types']:
						apt = x['long_name']
					if 'street_number' in x['types']:
						street1 = x['long_name']
					if 'route' in x['types']:
						street2 = x['long_name']
					if 'locality' in x['types']:
						city = x['long_name']
					if 'administrative_area_level_1' in x['types']:
						state = x['long_name']
					if 'postal_code' in x['types']:
						zip = x['long_name']																						
				
				request.POST['up-apt'] = apt
				request.POST['up-street'] = street1 + " " + street2
				request.POST['up-city'] = city
				request.POST['up-state'] = state
				request.POST['up-zip'] = zip																
# 				return HttpResponse(street1)
			else:
# 				r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=270%20Marin%20Blvd%20Jersey%20City%20NJ%2007302&sensor=false')
				addr = request.POST['up-street'] + " " + request.POST['up-apt'] + " " + request.POST['up-city'] + " " + request.POST['up-state'] + " " + request.POST['up-zip']
				r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=' + addr + '&sensor=false')
				if r.json()['status'] != 'OK':
					msg = 'Enter proper address'
					html = "<html><body>ERROR %s. <a href='/accounts/profile/'>Home</a></body></html>" % msg
					return HttpResponse(html)
# 				return HttpResponse(r.json()['results'][0]['geometry']['location']['lat'])
				request.POST['up-loc_0'] = r.json()['results'][0]['geometry']['location']['lat']
				request.POST['up-loc_1'] = r.json()['results'][0]['geometry']['location']['lng']
# 				return HttpResponse(request.POST['up-loc_0'])
				
		except:
			msg = 'Error in converting address'
			html = "<html><body>ERROR %s. <a href='/home/'>Home</a></body></html>" % msg
			return HttpResponse(html)
		if usern_form.is_valid() and up_form.is_valid():
# 			return HttpResponse("Hi")
			if usern_form.has_changed():
				usern_form.save()
# 			up_form.getAddrs()
# 			ext = os.path.splitext('uploaded_files/ab1_1449886450_224647_20130930135435!Download_square.pdf')[1]
# 			return HttpResponse(ext)
			up_form.clean_photopath
			up_form.save()
			return HttpResponseRedirect('/homepage/')
		else:
			msg = 'Error in saving profile. Please enter correct details'
			html = "<html><body>ERROR %s. <a href='/home/'>Home</a></body></html>" % msg
			return HttpResponse(html)
	else:
		user = request.user
		profile = user.profile
		# Set default value for location if not set for new user
		if not profile.loc:
			profile.loc = [40.692224, -73.987685]
		if not profile.firstname:
			alert = True
# 		form = ProfileForm(iuest.unitial={'username' : reqser})
		usern_form = UserForm(prefix = "usern", initial = {'username' : request.user, 'email' : u.email})
		up_form = ProfileForm(prefix = "up", instance = profile)	
# 		form = ProfileForm(instance = profile)
	variables = RequestContext(request, {'username': request.user, 'up_form': up_form, 'usern_form': usern_form, 'alert' : alert})
	return render_to_response('profile.html',variables)

