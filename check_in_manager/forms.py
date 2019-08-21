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
        exclude = (
            'order_creator', 'order_waiting_client_to_accept_offer', 'order_client_accepted_offer', 'order_accepted',
            'order_waiting_for_manager', 'order_accepted_by_guest', 'order_declined_by_guest', 'order_decline_reason')
        widgets = {
            'order_guest_check_in_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order_guest_check_out_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order_inclusions': forms.SelectMultiple(),
            'order_guest_name': forms.TextInput(attrs={'class': 'form-control'}),
            'order_guest_cell_number': forms.TextInput(attrs={'class': 'form-control'}),
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
        exclude = ('offer_order_id',)
