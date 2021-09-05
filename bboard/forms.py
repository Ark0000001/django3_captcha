from django.forms import modelform_factory, DecimalField, ModelForm
from django import forms
from django.forms.widgets import Select

from .models import Bb,Rubric


class BbForm(ModelForm):
    price = forms.DecimalField(label='Цена!',decimal_places=2)
    rubric=forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                  label='Рубрика!', help_text='Задайте рубрику',
                                  widget=forms.widgets.Select(attrs={'size':4}),empty_label='ХАЛВА')
    title=forms.CharField(label='Название продукта', label_suffix=':', initial='вводи здесь')




    class Meta:
        model=Bb
        fields=('title','content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


class SearchForm(forms.Form):
    keyword=forms.CharField(max_length=200,label='Искоемое')
    rubric=forms.ModelChoiceField(queryset=Rubric.objects.all(),label='Рубрика')



# class BbForm(ModelForm):
#     class Meta:
#         model=Bb
#         fields=('title','content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}
#         help_texts={'rubric':'Не забудьте выбрать рубрику'}
#         field_classes={'price':DecimalField}
#         widgets={'rubric':Select(attrs={'size':8})}

# BbForm = modelform_factory(Bb,fields=('title','content','price','rubric'),
#                            labels={'title':'Название товара'},
#                            help_texts={'rubric':'Не забудьте выбрать рубрику'},
#                            field_classes={'price':DecimalField},
#                            widgets={'rubric':Select(attrs={'size':8})})