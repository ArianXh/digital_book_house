from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from digital_book_house.settings import EMAIL_HOST_USER


from django.views import generic
from .models import Knigi, UserExtra, Clen, Lugje


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


def userclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/user.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/admin.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})



def usersignup_view(request):
    form1=forms.UserForm()
    form2 = forms.UserExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.UserForm(request.POST)
        form2=forms.UserExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():

            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_user_group = Group.objects.get_or_create(name='USER')
            my_user_group[0].user_set.add(user)

        return HttpResponseRedirect('userlogin')
    return render(request,'library/usersignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/userafterlogin.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addkniga_view(request):
    #now it is empty book form for sending to html
    form=forms.KnigiForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.KnigiForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewkniga_view(request):
    knigi=models.Knigi.objects.all()
    return render(request,'library/viewbook.html',{'knigi':knigi})





# Originalniot view za pozajmici

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_pozajmica_kniga_view(request):
    form1=forms.PozajmiKnigaForm()
    form2=forms.PozajmiKnigaFormExtra()
    mydict = {'form1': form1, 'form2': form2}
    if request.method=='POST':
        #now this form have data from html
        form1 = forms.PozajmiKnigaForm(request.POST)
        form2 = forms.PozajmiKnigaFormExtra(request.POST)
        if form1.is_valid() and form2.is_valid():
            obj=models.Pozajmica()
            obj.fk=request.POST.get(id)
            obj.save()
            #obj = form1.save()


            obj1 = form2.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',context=mydict)



############## TESTING POZAJMICA KNIGA ##############

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def pozajmica_kniga_view(request):
    knigi=models.Knigi.objects.all()
    return render(request,'library/issuedbook.html',{'knigi':knigi})

class KnigaDetailView(generic.DetailView):
    model = Knigi


class LugjeDetailView(generic.DetailView):
    model = Lugje



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewuser_view(request):
    #clenovi = Lugje.objects.all()
    clenovi = Lugje.objects.raw('SELECT lugjeid, ime, prezime, adresa, email from lugje as l inner join clen as c on l.lugjeid = c.clenskibr')
    return render(request, 'library/viewuser.html', {'clenovi': clenovi})


def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['arian14@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})



def kot_form(request):
    kot = kot_form()