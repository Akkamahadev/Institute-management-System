from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from StudentApp.models import Course
from StudentApp.models import City
from StudentApp.models import Stuent
# Create your views here.
def login_fun(request):
    if request.method == "POST":
        user_name=request.POST['txtUsername']
        user_pwd=request.POST['txtPassword']
        u1=authenticate(username=user_name,password=user_pwd)
        if u1 is not None:
            if u1.is_superuser:#checking whrether data is superuser or not
                request.session['Uname']= user_name
                login(request,u1)
                return redirect('home')
        else:
            return render(request,'login.html',{'msg':'User name and password incorrect'})
    else:
        return render(request,'login.html')
def register_fun(request):#this code excute when click on submit button in registration page
    if request.method == 'POST':
        user_name=request.POST['txtUsername']
        user_pswd=request.POST['txtPassword']
        user_email=request.POST['txtemail']
        if User.objects.filter(username=user_name).exists():
            return render(request,'register.html',{'msg':'Use proper user name '})
        else:
            u1 = User.objects.create_superuser(username=user_name, password=user_pswd, email=user_email)
            u1.save()
            return redirect('log')
    else:#it will excute when
        return render(request,'register.html')
@login_required
@never_cache
def home_fun(request):
    return render(request,'home.html',{'data':request.session['Uname']})
@login_required
@never_cache
def addcourse_fun(request):
    if request.method =='POST':
        c1=Course()
        c1.course_name=request.POST['txtCourseName']
        c1.course_duration=request.POST['txtCourseDuration']
        c1.course_fees=int(request.POST['txtCourseFees'])
        c1.save()
        return render(request, 'addcourse.html',{'msg':'Sucessfully added'})
    else:
        return render(request,'addcourse.html')
@login_required
@never_cache
def display_course_fun(request):
    course_data=Course.objects.all()  #it will return list of objects
    return render(request,'displaycourse.html',{'data':course_data})
@login_required
@never_cache
def upadatecourse_fun(request,courseid):
    c1=Course.objects.get(id=courseid)
    if request.method == 'POST':
        c1.course_name = request.POST['txtCourseName']
        c1.course_duration=request.POST['txtCourseDuration']
        c1.course_fees=request.POST['txtCourseFees']
        c1.save()
        return redirect('display_course')
    else:
       return render(request,'updateCourse.html',{'data':c1})
@login_required
@never_cache
def delete_fun(request,courseid):
    c1 = Course.objects.get(id=courseid)
    c1.delete()
    return redirect('display_course')
@login_required
@never_cache
def addstudent_fun(request):
    if request.method == 'POST':
        s1 = Stuent()
        s1.stud_name = request.POST['txtName']
        s1.stud_phno = request.POST['txtphno']
        s1.stud_email = request.POST['txtemail']
        s1.stud_city = City.objects.get(city_name=request.POST['ddlcity']) #foregin key constraints
        s1.stud_couese = Course.objects.get(course_name=request.POST['ddlcourse'])
        s1.paid_fees = int(request.POST['txtpaid'])
        c1= Course.objects.get(course_name = request.POST['ddlcourse'])
        s1.pending_fees = c1.course_fees - s1.paid_fees
        s1.save()
        return redirect('addstudent')
    else:
        city=City.objects.all()
        course=Course.objects.all()
        return render(request,'addstudent.html',{'CityData':city,'CourseData':course})
@login_required
@never_cache
def displaystud_fun(request):
    s1=Stuent.objects.all()
    return render(request,'displaystudent.html',{'studentdata':s1})
@login_required
@never_cache
def updatestud_fun(request,studid):
    s1=Stuent.objects.get(id=studid)
    if request.method=='POST':
        s1.stud_name = request.POST['txtName']
        s1.stud_phno = int(request.POST['txtphno'])
        s1.stud_email = request.POST['txtemail']
        s1.stud_city = City.objects.get(city_name=request.POST['ddlcity'])  # foregin key constraints
        s1.stud_couese = Course.objects.get(course_name=request.POST['ddlcourse'])
        s1.paid_fees = s1.paid_fees+int(request.POST['txtpaid'])
        c1 = Course.objects.get(course_name=request.POST['ddlcourse'])
        if s1.pending_fees>0:
            s1.pending_fees = c1.course_fees - s1.paid_fees
        else:
            s1.pending_fees=0
        s1.save()
        return redirect('displaystudent')
    else:
        city = City.objects.all()
        course = Course.objects.all()
        return render(request,'updatestud.html',{'student':s1,'CityData':city,'CourseData':course})
@login_required
@never_cache
def deletestud_fun(request,studid):
    s1=Stuent.objects.get(id=studid)
    s1.delete()
    return redirect('displaystudent')
def logout_fun(request):
    logout(request)
    del request.session['Uname']
    return redirect('log')
