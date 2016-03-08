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
from login.models import Blocks
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle
from nextnbr.settings import MEDIA_URL
from decimal import Decimal
from profileapp.models import UserProfile
# from django.contrib.gis.geos import polygon



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

@login_required
def home_1(request):
#     filename = "C:\Users\Vasundhara Patil\Documents\GitHub\next\media\uploaded_files\ab1_1449302455_874656_Frozen_Queen_Elsa_Wallpaper.jpg"
    u = User.objects.get(username = request.user)
    request.session['userid'] = u.id
    prfl = request.user.profile
    if not prfl.firstname:
        return HttpResponseRedirect('/accounts/profile/', {'alert' : True})
#     image_name = "uploaded_files/Frozen_Queen_Elsa_Wallpaper.jpg"
    return render_to_response('home_1.html',{ 'user': request.user, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })


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
