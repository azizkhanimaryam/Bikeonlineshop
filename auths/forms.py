from django import forms


class Login(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        for item in Login.visible_fields(self):
            item.field.widget.attrs["class"] = "form-control"

    UserName = forms.CharField(required=True, label="Username")
    Password = forms.CharField(required=True, label="Password")
class Register(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        for item in Login.visible_fields(self):
            item.field.widget.attrs["class"] = "form-control"

    Name = forms.CharField(required=True, label="Name")
    Family = forms.CharField(required=True, label="SurName")
    UserName = forms.CharField(required=True, label="Username")
    Password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput)

