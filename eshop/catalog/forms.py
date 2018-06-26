from django import forms

class CheckoutForm(forms.Form):
    person_name = forms.CharField(label="Ваше имя и фамилия", max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    person_email = forms.EmailField(label="Ваш E-Mail", widget=forms.EmailInput(attrs={"class": "form-control"}))
    person_phone = forms.CharField(label="Ваш номер телефона", max_length=30, widget=forms.TextInput(input_type="phone", attrs={"class": "form-control"}))
    person_address = forms.CharField(label="Адрес доставки (город, район, улица, дом, квартира или офис)", max_length=1024, widget=forms.Textarea(attrs={"rows": "3", "class": "form-control"}))
    notes = forms.CharField(label="Сообщение для оператора (можно не заполнять)", max_length=2048, required=False, widget=forms.Textarea(attrs={"rows": "5", "class": "form-control"}))