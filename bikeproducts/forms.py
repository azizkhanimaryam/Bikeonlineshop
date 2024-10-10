from django import forms


class productForm(forms.Form):
    name=forms.CharField(max_length=100, label="Title")
    description=forms.CharField(label="Description", widget=forms.Textarea())
    image = forms.ImageField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PaymentForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput)
