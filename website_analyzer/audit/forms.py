from django import forms
import requests
from requests.exceptions import RequestException

class WebpageForm(forms.Form):

    url = forms.URLField(
        label='Website URL',
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.example.com',
            'class': 'form-control',
        },
        ),
        max_length=2048,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(WebpageForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = ''
    
    def clean_url(self):
        """Clean the URL with Django's built-in form verification
        Check if the URL exists on the Internet
        """
        url = self.cleaned_data.get('url')

        # check if the URL exists
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                raise forms.ValidationError("Could not access the URL. Please enter a valid, accessible URL.")
        except RequestException as e:
            raise forms.ValidationError("Could not access the URL. Please enter a valid, accessible URL.")
        
        return url