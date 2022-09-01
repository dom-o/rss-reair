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
                print(err)
        if error_list:
            raise ValidationError(error_list)

class RSSForm(forms.Form):
    title = forms.CharField(label='Name your list:')
    description = forms.CharField(label='Optionally describe your content (this will appear in the description section of the rss feed):', required=False)
    item_links = URLList(widget=forms.Textarea, label='URLs go here:')
    reverse = forms.BooleanField(label='Publish in reverse.', required=False)

class DynamicForm(RSSForm):
    origin_link = forms.URLField(label="Origin link")

    def clean_origin_link(self):
        data = self.cleaned_data['origin_link']
        return data

class ConsumableForm(forms.Form):
    daily_items = forms.IntegerField(min_value=1, max_value=10, initial=1)
