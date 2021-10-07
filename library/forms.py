from django import forms
from django.contrib.auth.models import User
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class UserExtraForm(forms.ModelForm):
    class Meta:
        model=models.UserExtra
        fields=['enrollment','branch']



class KnigiForm(forms.ModelForm):
    class Meta:
        model = models.Knigi
        fields = ['knigaid', 'naslov', 'kformat', 'kopis', 'izdavacid']


class IssuedBookForm(forms.Form):
    knigaid = forms.ModelChoiceField(queryset=models.Instancakniga.objects.all(), empty_label="knigaid",
                                   to_field_name="knigaid", label='ID Kniga')
    seriskibr = forms.ModelChoiceField(queryset=models.Instancakniga.objects.all(), empty_label="seriskibr",
                                         to_field_name='seriskibr', label='Seriski Broj')

class PozajmiKnigaForm(forms.Form):
    # id = kompoziten kluc (knigaid, seriskibr)
    id = forms.ModelChoiceField(queryset=models.Instancakniga.objects.all(),
                                   to_field_name="id", label='Kniga Instanca')



class PozajmiKnigaFormExtra(forms.ModelForm):
    class Meta:
        model = models.Pozajmica
        fields = ['pstatus', 'pocetokdatum', 'krajdatum']


class TestPozajmiFormZaedno(forms.ModelForm):
    class Meta:
        model1 = models.Pozajmica
        model2 = models.Instancakniga
        fields = ['pstatus', 'pocetokdatum', 'krajdatum']