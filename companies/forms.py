from django import forms
import re
from .models import CompanyApplication, Category


class CompanyApplicationForm(forms.ModelForm):
    class Meta:
        model = CompanyApplication
        fields = [
            'company_name', 'contact_person', 'phone', 'email', 'website',
            'description', 'address', 'category',
            'charity_description', 'charity_amount', 'charity_frequency',
            'additional_info'
        ]
        
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название вашей компании'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО контактного лица'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@company.ru'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://company.ru'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о вашей компании, чем занимаетесь, сколько лет работаете...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'г. Махачкала, ул. Примерная, 123'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'charity_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Подробно опишите вашу благотворительную деятельность, кому и как вы помогаете...'
            }),
            'charity_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50000'
            }),
            'charity_frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация, которую хотите сообщить (необязательно)'
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?[0-9\s\-\(\)]{10,15}$', phone):
            raise forms.ValidationError('Некорректный формат телефона')
        return phone