from django import forms
from .models import Medecin, Enregistrement

class MedecinLoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        try:
            user = Medecin.objects.get(email=email)
        except Medecin.DoesNotExist:
            raise forms.ValidationError("Email not registered.")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password.")

        return cleaned_data
class MedecinLogoutForm(forms.Form):
    confirm_logout = forms.BooleanField(
        label="Confirmer la déconnexion",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Cochez cette case pour confirmer que vous souhaitez vous déconnecter."
    )

    feedback = forms.CharField(
        label="Feedback (optionnel)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="Laissez un commentaire avant de vous déconnecter."
    )
class MedecinForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        min_length=8, 
        required=True 
    )
    class Meta:
        model = Medecin
        fields = ['email', 'password', 'specialite', 'nom_complet']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Medecin.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password

    def save(self, commit=True):
        medecin = super(MedecinForm, self).save(commit=False)
        medecin.set_password(self.cleaned_data['password']) 
        if commit:
            medecin.save()
        return medecin

class EnregistrementForm(forms.ModelForm):
    class Meta:
        model = Enregistrement
        fields = ['medecin', 'nomComplet', 'img1','img2','img3','img4','img5', 'naissance', 'admission', 'medication', 'notes']
        widgets = {
            'medecin': forms.Select(),
            'admission': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    medecin = forms.ModelChoiceField(queryset=Medecin.objects.all(), empty_label="Select a doctor")
    
    def clean_nomComplet(self):
        nomComplet = self.cleaned_data.get('nomComplet')
        if not nomComplet:
            raise forms.ValidationError("This field is required.")
        return nomComplet

class SearchForm(forms.Form):
    notes = forms.CharField(required=False, label='Notes')
    medication = forms.CharField(required=False, label='Medication')

    def clean(self):
        cleaned_data = super().clean()
        notes = cleaned_data.get("notes")
        medication = cleaned_data.get("medication")
        return cleaned_data

class FiltrerForm(forms.Form):
    medecin = forms.ModelChoiceField(queryset=Medecin.objects.all(), required=False, label='Médecin')
    notes = forms.CharField(required=False, label='Notes')
    medication = forms.CharField(required=False, label='Médication')
    def clean(self):
        cleaned_data = super().clean()
        medecin = cleaned_data.get("medecin")
        notes = cleaned_data.get("notes")
        medication = cleaned_data.get("medication")
        if not medecin and not notes and not medication:
            raise forms.ValidationError("Veuillez sélectionner au moins un critère de filtrage.")
        return cleaned_data

class ExportForm(forms.Form):
    FORMAT_CHOICES = [
        ('XLS', 'Excel'),
        ('PDF', 'PDF'),
        ('DOCX', 'Word Document'),
        ('HTML', 'HTML'),
    ]
    format = forms.ChoiceField(choices=FORMAT_CHOICES, label='Format d\'exportation')
    def clean_format(self):
        format = self.cleaned_data.get('format')
        if format not in dict(self.FORMAT_CHOICES):
            raise forms.ValidationError("Format d'exportation invalide.")
        return format