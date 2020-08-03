from django import forms
from .models import Tournament, Tournament_state, Saison

class TounrmamentAddForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TounrmamentAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'input'})
        self.fields['slug'].widget.attrs.update({'class' : 'input'})
        self.fields['event'].widget.attrs.update({'class' : 'input'})
        self.fields['event_slug'].widget.attrs.update({'class' : 'input'})
        self.fields['state'].widget.attrs.update({'class' : 'select'})
        self.fields['saison'].widget.attrs.update({'class' : ''})
        
        self.fields['association'].widget.attrs.update({'class' : 'select'})

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)