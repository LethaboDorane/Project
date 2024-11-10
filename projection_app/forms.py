# from django import forms

# class SalesForm(forms.Form):
#     sales_data = forms.CharField(label="Sales Data (comma-separated)", widget=forms.Textarea)
#     months = forms.IntegerField(label="Projection Period")
#     graph_type = forms.ChoiceField(choices=[('bar', 'Bar'), ('line', 'Line'), ('scatter', 'Scatter')])
#     data_frequency = forms.ChoiceField(
#         label="Data Frequency",
#         choices=[('monthly', 'Monthly')],
#         initial='monthly'
#     )

from django import forms

class SalesForm(forms.Form):
    sales_data = forms.CharField(widget=forms.Textarea, label='Sales Data (comma-separated values)')
    expenses_data = forms.CharField(widget=forms.Textarea, required=False, label='Expenses Data (optional, comma-separated values)')
    months = forms.IntegerField(min_value=1, label='Projection Period (Months)')
    graph_type = forms.ChoiceField(choices=[('line', 'Line'), ('bar', 'Bar'), ('scatter', 'Scatter')], label='Graph Type')
