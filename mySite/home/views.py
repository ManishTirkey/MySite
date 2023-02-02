from django.shortcuts import redirect, render as ren
from django.http import HttpResponse as res
from .models import Contact
from django.contrib import messages


# Create your views here.
def home(request):
    # return res("this is home index")
    return ren(request, 'home/home.html')


def contact(request):
    done = False
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phno = request.POST['phno']
        textarea = request.POST['textarea']

        if len(phno) >= 10 and len(email) > 10:
            contact = Contact(name=name, email=email, phno=phno, address=address, comment=textarea)
            contact.save()
            done = True
        else:
            messages.error(request, "Enter correct Phone Number!")

        if done:
            messages.success(request, "this is manish message")
            return ren(request, 'home/contact.html', {"done": done, "name": name})

        # messages.error(request, "Error occured")
    return ren(request, 'home/contact.html')


def about(request):
    return ren(request, 'home/about.html')


def search(request):
    # return res("this is search")
    return ren(request, "home/search.html")
