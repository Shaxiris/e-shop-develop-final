from django.forms import ModelForm, ValidationError
from catalog.models import Product, Version


class ProductForm(ModelForm):
    """
    Форма для модели Product

    Проверяет поля name и description на присутствие запрещенных слов
    """

    forbidden_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')

    class Meta:
        model = Product
        exclude = ('creation_date', 'change_date', 'owner',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        cleaned_data_lower = cleaned_data.lower()
        for word in self.forbidden_words:
            if word in cleaned_data_lower:
                raise ValidationError('Название содержит запрещенные слова!')
        return cleaned_data.title()

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        cleaned_data_lower = cleaned_data.lower()
        for word in self.forbidden_words:
            if word in cleaned_data_lower:
                raise ValidationError('Описание содержит запрещенные слова!')
        return cleaned_data.capitalize()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionForm(ModelForm):
    """
    Форма для модели Version
    """

    class Meta:
        model = Version
        fields = ('number', 'name', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'checkbox-left'