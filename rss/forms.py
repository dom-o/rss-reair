from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URLList(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return [s.strip() for s in value.splitlines() if s.strip()]

    def validate(self, value):
        super().validate(value)
        error_list = []
        for link in value:
            try:
                URLValidator(message=f'\'{link}\' is not a valid url.')(link)
            except ValidationError as err:
                error_list.append(err)
        if error_list:
            raise ValidationError(error_list)


class RSSForm(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(label='Description', required=False)
    item_links = URLList(widget=forms.Textarea, label='Items')
    reverse = forms.BooleanField(label='Reverse', required=False)

class ConsumableForm(forms.Form):
    daily_items = forms.IntegerField(min_value=1, max_value=10, initial=1)
