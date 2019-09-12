from django import forms
from django_ace import AceWidget
from .models import EmailTemplate


class EmailTemplateForm(forms.ModelForm):
    mjml_template = forms.CharField(
        label='MJML template',
        required=False,
        widget=AceWidget(
            wordwrap=False,
            mode='xml',
            width="100%",
            height="300px",
            showprintmargin=True,
        ),
    )

    class Meta:
        model = EmailTemplate
        fields = '__all__'
