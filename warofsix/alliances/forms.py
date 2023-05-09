from django import forms
from .models import Alliances



class AllianceCreateForm(forms.ModelForm):

    BANNER_CHOICES = [
        ('a', 'banner_a'),
        ('b', 'banner_b'),
        ('c', 'banner_c'),
        ('d', 'banner_d'),
        ('e', 'banner_e'),
        ('f', 'banner_f'),
        ('g', 'banner_g'),
        ('h', 'banner_h'),
        ('i', 'banner_i'),
        ('j', 'banner_j')
    ]
    name = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Ally Name'
        })
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput2',
            'placeholder': 'Ally Description'
        })
    )
    banner = forms.ChoiceField(choices=BANNER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Alliances
        fields = ['name', 'description', 'banner']


class AlliancesForm(forms.ModelForm):
    class Meta:
        model = Alliances
        fields = ['description', 'banner']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }


class AllianceCreateForm2(forms.ModelForm):

    BANNER_CHOICES = [
        ('a', 'banner_a'),
        ('b', 'banner_b'),
        ('c', 'banner_c'),
        ('d', 'banner_d'),
        ('e', 'banner_e'),
        ('f', 'banner_f'),
        ('g', 'banner_g'),
        ('h', 'banner_h'),
        ('i', 'banner_i'),
        ('j', 'banner_j')
    ]


    name = forms.TextInput()

    description = forms.CharField(


    )

    banner = forms.ChoiceField(choices=BANNER_CHOICES, widget= forms.RadioSelect())

    class Meta:
        model = Alliances
        fields = ('name',)
        labels = {
            'name': 'Ally Name',
            'description': 'Ally Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',

            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput2',
                'placeholder': 'Ally Description'
            }),
            'banner': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }