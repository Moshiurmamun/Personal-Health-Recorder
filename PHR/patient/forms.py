from django import forms
from .models import Patient
from ckeditor.widgets import CKEditorWidget

class StoryForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)


    class Meta:
        model = Patient
        fields = ('doctor_name','disease_name', 'content', 'image', 'publish', 'file')
