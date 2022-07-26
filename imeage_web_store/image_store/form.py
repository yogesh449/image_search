from django import forms


class ImageForm(forms.Form):
    image_name = forms.CharField(max_length=100)
