from django import forms

class SalesForm(forms.Form):
    sales_data = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter sales data (e.g., 1000, 2000, 3000)'}
        ),
        label='Sales Data (comma-separated values)'
    )
    expenses_data = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter expenses data (optional, e.g., 500, 600, 700)'}
        ),
        required=False,
        label='Expenses Data (optional, comma-separated values)'
    )
    months = forms.IntegerField(
        min_value=1,
        label='Projection Period (Months)',
        widget=forms.NumberInput(
            attrs={'placeholder': 'Enter number of months for projection'}
        )
    )
    graph_type = forms.ChoiceField(
        choices=[('line', 'Line'), ('bar', 'Bar'), ('scatter', 'Scatter')],
        label='Graph Type'
    )
