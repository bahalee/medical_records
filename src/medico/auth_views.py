from django.contrib.auth import authenticate, login,logout
from .forms import MedecinLoginForm , MedecinLogoutForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Feedback
def login_medecin(request):
    if request.method == 'POST':
        form = MedecinLoginForm(data=request.POST) 
        if form.is_valid():
            email = form.cleaned_data.get('email')  
            password = form.cleaned_data.get('password')
            medecin = authenticate(request, email=email, password=password)
            if medecin is not None:
                login(request, medecin)  
                return redirect('home') 
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = MedecinLoginForm() 
    return render(request, 'medical_records/login.html', {'form': form}) 

def logout_medecin(request):
    if request.method == 'POST':
        form = MedecinLogoutForm(request.POST)
        if form.is_valid():
            feedback_message = form.cleaned_data.get('feedback')
            if feedback_message:
                Feedback.objects.create(user=request.user, message=feedback_message)
            logout(request)
            response = redirect('login')
            response.delete_cookie('sessionid')  
            return response
    else:
        form = MedecinLogoutForm()

    return render(request, 'medical_records/logout.html', {'form': form})