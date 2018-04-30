from django import forms
from .models import Menu, Item


class MenuForm(forms.ModelForm):
    """Edit Menu Model Form"""
    expiration_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
                                           required=False,
                                           widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Menu
        exclude = ('created_date',)


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('created_date',)
