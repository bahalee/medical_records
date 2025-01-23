from django.test import TestCase
from django.urls import reverse
from .models import Medecin, Enregistrement, Exporter
from .forms import SearchForm, FiltrerForm
class MedecinModelTest(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.medecin.set_password('securepassword')  
        self.medecin.save() 

    def test_medecin_str(self):
        self.assertEqual(str(self.medecin), 'Dr. John Jobson')

    def test_medecin_creation(self):
        self.assertEqual(Medecin.objects.count(), 1)
        self.assertEqual(self.medecin.specialite, 'Cardiology')
        self.assertEqual(self.medecin.nom_complet, 'Dr. John Jobson')

    def test_medecin_password(self):
        self.assertTrue(self.medecin.check_password('securepassword'))


class EnregistrementModelTest(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.medecin.set_password('securepassword')
        self.medecin.save()
        self.enregistrement = Enregistrement.objects.create(
            nomComplet='Joe Doe',
            img=None,
            naissance='1990-01-01',
            admission='2023-01-01 10:00:00',
            medication='Aspirin',
            notes='No known allergies',
            medecin=self.medecin
        )

    def test_enregistrement_str(self):
        self.assertEqual(str(self.enregistrement), 'Joe Doe')

    def test_enregistrement_creation(self):
        self.assertEqual(Enregistrement.objects.count(), 1)
        self.assertEqual(self.enregistrement.medecin, self.medecin)


class MedecinViewTests(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.medecin.set_password('securepassword') 
        self.medecin.save()

    def test_create_medecin_view(self):
        response = self.client.post(reverse('create_medecin'), {
            'email': 'JohnDupont@gmail.com',
            'password': 'newpassword', 
            'specialite': 'Neurology'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Medecin.objects.count(), 2)  

    def test_lister_enregistrements_view(self):
        response = self.client.get(reverse('lister_enregistrements'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_records/lister_enregistrements.html')


class EnregistrementViewTests(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.medecin.set_password('securepassword') 
        self.medecin.save()
        self.enregistrement = Enregistrement.objects.create(
            nomComplet='Joe Doe',
            img=None,
            naissance='1990-01-01',
            admission='2023-01-01 10:00:00',
            medication='Aspirin',
            notes='No known allergies',
            medecin=self.medecin
        )

    def test_create_enregistrement_view(self):
        response = self.client.post(reverse('create_enregistrement'), {
            'nomComplet': 'Jane Doe',
            'naissance': '1992-02-02',
            'admission': '2023-01-02 11:00:52',
            'medication': 'Ibuprofen',
            'notes': 'No known allergies',
            'medecin': self.medecin.id
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Enregistrement.objects.count(), 2) 

    def test_exporter_enregistrement_pdf(self):
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'PDF']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Disposition', response)  
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=Joe_Doe.pdf'))  

    def test_exporter_enregistrement_xls(self):
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'XLS']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Disposition', response)  
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=Joe_Doe.xls'))  

    def test_exporter_enregistrement_docx(self):
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'DOCX']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Disposition', response) 
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=Joe_Doe.docx'))  

    def test_exporter_enregistrement_html(self):
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'HTML']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response)  
        self.assertTrue(response['Content-Type'].startswith('text/html'))  

    def test_invalid_export_format(self):
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'INVALID_FORMAT']))
        self.assertEqual(response.status_code, 400)  

    def test_export_failed(self):
        exporter = Exporter(formatsPrisEnCharge=['PDF'], fail_export=True)  
        response = self.client.get(reverse('exporter_enregistrement', args=[self.enregistrement.id, 'PDF']))
        self.assertEqual(response.status_code, 500)  
class SearchViewTests(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.enregistrement_1 = Enregistrement.objects.create(
            nomComplet='Joe Doe',
            img=None,
            naissance='1990-01-01',
            admission='2023-01-01 10:00:00',
            medication='Aspirin',
            notes='No known allergies',
            medecin=self.medecin
        )
        self.enregistrement_2 = Enregistrement.objects.create(
            nomComplet='Jane Doe',
            img=None,
            naissance='1992-02-02',
            admission='2023-01-02 11:00:00',
            medication='Ibuprofen',
            notes='Sensitive to cold',
            medecin=self.medecin
        )

    def test_effectuer_recherche_view_valid(self):
        response = self.client.get(reverse('effectuer_recherche') + '?notes=allergies&medication=Aspirin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Joe Doe')
        self.assertNotContains(response, 'Jane Doe')

    def test_effectuer_recherche_view_invalid(self):
        response = self.client.get(reverse('effectuer_recherche') + '?notes=nonexistent&medication=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aucune enregistrements trouver')

class FilterViewTests(TestCase):
    def setUp(self):
        self.medecin = Medecin.objects.create(
            nom_complet='Dr. John Jobson',
            email='johnjobson@gmail.com',
            specialite='Cardiology'
        )
        self.enregistrement_1 = Enregistrement.objects.create(
            nomComplet='Joe Doe',
            img=None,
            naissance='1990-01-01',
            admission='2023-01-01 10:00:00',
            medication='Aspirin',
            notes='No known allergies',
            medecin=self.medecin
        )
        self.enregistrement_2 = Enregistrement.objects.create(
            nomComplet='Jane Doe',
            img=None,
            naissance='1992-02-02',
            admission='2023-01-02 11:00:00',
            medication='Ibuprofen',
            notes='Sensitive to cold',
            medecin=self.medecin
        )

    def test_appliquer_filtres_view_valid(self):
        response = self.client.get(reverse('appliquer_filtres') + '?medecin=1&notes=allergies')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Joe Doe')
        self.assertNotContains(response, 'Jane Doe')

    def test_appliquer_filtres_view_no_criteria(self):
        response = self.client.get(reverse('appliquer_filtres') + '?')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Veuillez sélectionner au moins un critère de filtrage.')