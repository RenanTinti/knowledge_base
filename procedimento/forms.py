from urllib import request
from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    sugestao = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your suggestion here...', 'rows': '5'}), label = '')
    class Meta:
        model = Suggestion
        
        fields = ['sugestao']