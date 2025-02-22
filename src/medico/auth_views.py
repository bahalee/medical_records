from django.contrib.auth import authenticate, login,logout
from .forms import MedecinLoginForm , MedecinLogoutForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Feedback
from django.contrib import messages

def login_medecin(request):
    if request.method == 'POST':
        form = MedecinLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # This creates the session
                print(f"User authenticated: {user.email}")  # Debug print
                print(f"Session key: {request.session.session_key}")  # Debug print
                return redirect('home')
            else:
                messages.error(request, "Identifiants incorrects, veuillez réessayer.")
        else:
            messages.error(request, "S'il vous plaît corrigez les erreurs ci-dessous.")
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
            logout(request)  # Clear the server-side session
            return redirect('login')  # Redirect to login page after logout
    else:
        form = MedecinLogoutForm()
    return render(request, 'medical_records/logout.html', {'form': form})