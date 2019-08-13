from django import forms

from .models import Order


class EditOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditOrderForm, self).__init__(*args, **kwargs)
        # TODO: add help_text to some fields
        # self.fields['order_guest_email'].help_text = "Example youremail@gmail.com"

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('order_creator',)
        widgets = {
            'order_guest_check_in_date': forms.SelectDateWidget(),
            'order_guest_check_out_date': forms.SelectDateWidget()
        }
