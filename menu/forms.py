from django import forms
from .models import Menu, Item


class MenuForm(forms.ModelForm):
    """Edit Menu Model Form"""
    expiration_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
                                           required=False,
                                           widget=forms.CheckboxSelectMultiple)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        '''Added honeypot'''
        honeypot = self.cleaned_data['honeypot']
        if len(honeypot):
            raise forms.ValidationError('Error: Honeypot should be left empty.')
        else:
            return honeypot

    class Meta:
        model = Menu
        exclude = ('created_date',)


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('created_date',)
