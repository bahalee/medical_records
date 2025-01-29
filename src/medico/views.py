from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Medecin, Enregistrement, Exporter
from .forms import MedecinForm, EnregistrementForm, SearchForm, FiltrerForm

def home(request):
    return render(request, 'medical_records/home.html')

def create_medecin(request):
    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = MedecinForm()
    return render(request, 'medical_records/create_medecin.html', {'form': form})

def lister_enregistrements(request):
    enregistrements = Enregistrement.objects.all()  
    return render(request, 'medical_records/lister_enregistrements.html', {'enregistrements': enregistrements})

def create_enregistrement(request):
    medecins = Medecin.objects.all()
    if request.method == 'POST':
        form = EnregistrementForm(request.POST, request.FILES)
        if form.is_valid():
            enregistrement = form.save(commit=False)
            for i in range(1, 6):
                img_field = f'img{i}'
                if img_field in request.FILES:
                    setattr(enregistrement, img_field, request.FILES[img_field])
            enregistrement.save()
            return redirect('success') 
        else:
            print(form.errors) 
    else:
        form = EnregistrementForm()
    return render(request, 'medical_records/create_enregistrement.html', {'form': form,'medecins': medecins })

def effectuer_recherche(request):
    form = SearchForm(request.GET or None)
    results = []
    if form.is_valid():
        notes = form.cleaned_data.get('notes')
        medication = form.cleaned_data.get('medication')
        results = Enregistrement.objects.filter(
            notes__icontains=notes,
            medication__icontains=medication
        )
    return render(request, 'medical_records/effectuer_recherche.html', {'form': form, 'results': results})

def appliquer_filtres(request):
    form = FiltrerForm(request.GET or None)
    filtered_results = []
    if form.is_valid():
        criteres = {k: v for k, v in form.cleaned_data.items() if v}  
        filtered_results = Enregistrement.objects.filter(**criteres)  
    return render(request, 'medical_records/appliquer_filtres.html', {'form': form, 'filtered_results': filtered_results})

def exporter_enregistrement(request, idenreg, format):
    enregistrement = get_object_or_404(Enregistrement, idenreg=idenreg)
    exporter = Exporter(formatsPrisEnCharge=['PDF', 'XLS', 'DOCX', 'HTML'])
    
    if exporter.vérifierFormat(format):
        result = exporter.exporterEnregistrement(enregistrement, format)
        if isinstance(result, HttpResponse):
            return result
        else:
            return HttpResponse("Export failed", status=500)
    else:
        return HttpResponse("Invalid format", status=400)

def modifier_enregistrement(request, pk):
    enregistrement = get_object_or_404(Enregistrement, pk=pk)
    if request.method == 'POST':
        form = EnregistrementForm(request.POST, request.FILES, instance=enregistrement)
        if form.is_valid():
            form.save()
            return redirect('lister_enregistrements')
    else:
        form = EnregistrementForm(instance=enregistrement)
    return render(request, 'medical_records/modifier_enregistrement.html', {'form': form})

def supprimer_enregistrement(request, pk):
    enregistrement = get_object_or_404(Enregistrement, pk=pk)
    enregistrement.delete()
    return redirect('lister_enregistrements')

def success(request):
    return render(request, 'medical_records/success.html')