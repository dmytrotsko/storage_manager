from django import forms

from .models import Order, SpecOccasion, Inclusion, Source, Offer


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
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


class SpecOccasionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpecOccasionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SpecOccasion
        fields = '__all__'


class SourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Source
        fields = '__all__'


class InclusionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InclusionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Inclusion
        fields = '__all__'


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Offer
        fields = '__all__'