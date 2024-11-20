from django import forms
from wishlists.models import Present


class NewPresentForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'profilePicInput', 'onchange': 'previewImage(event)'}), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название подарка (макс. 40 символов)'}), max_length=40)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите краткое описание/пожелание (макс. 40 символов)'}), required=False, max_length=40)
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на подарок'}), max_length=40)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену подарка (в рублях)'}), max_digits=9, decimal_places=2, required=False)


    class Meta:
        model = Present
        fields = ('image', 'title', 'description', 'link', 'price')
