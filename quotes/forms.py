from django import forms
from quotes.models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]