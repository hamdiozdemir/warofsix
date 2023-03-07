from django import forms
from main.models import Messages


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ["target", "header", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target'].widget.attrs.update({'class': 'form-control'})
        self.fields['header'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})