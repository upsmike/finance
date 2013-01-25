__author__ = 'Joao'

from datetime import date
from django import forms
from django.contrib.auth.models import User
from models import ContaPagar, ContaReceber
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext as _

class FormPagamento(forms.Form):
    valor = forms.DecimalField(max_digits=15, decimal_places=2)

    def salvar_pagamento(self, conta):
        return conta.lancar_pagamento(
            data_pagamento=date.today(),
            valor=self.cleaned_data['valor'],
        )

class FormContaPagar(forms.ModelForm):
    class Meta:
        model = ContaPagar
        exclude = ('usuario', 'operacao', 'data_pagamento')
        def __init__(self, *args, **kwargs):
            self.base_fields['data_vencimento'].widget = SelectDateWidget()
            super(FormContaPagar, self).__init__(*args, **kwargs)


class FormContaReceber(forms.ModelForm):
    class Meta:
        model = ContaReceber
        exclude = ('usuario','operacao','data_pagamento')

        def __init__(self, *args, **kwargs):
            self.base_fields['data_vencimento'].widget = SelectDateWidget()
            super(FormContaReceber, self).__init__(*args, **kwargs)

class FormRegistro(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    confirme_a_senha = forms.CharField(
        max_length=30, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormRegistro, self).__init__(*args, **kwargs)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'],).count():
            raise forms.ValidationError('Ja existe um usuario com este nome!')

        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este e-mail!')

        return self.cleaned_data['email']

    def clean_confirme_a_senha(self):
        if self.cleaned_data['confirme_a_senha'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere!')

        return self.cleaned_data['confirme_a_senha']

    def save(self, commit=True):
        usuario = super(FormRegistro, self).save(commit=False)

        usuario.set_password(self.cleaned_data['password'])

        if commit:
            usuario.save()

        return usuario