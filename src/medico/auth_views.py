from django.contrib.auth import authenticate, login
from .forms import MedecinLoginForm 
from django.shortcuts import render, redirect
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
