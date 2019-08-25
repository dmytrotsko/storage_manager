from django import forms

from .models import Order, SpecOccasion, Inclusion, Source, Offer

from django.contrib.admin.widgets import RelatedFieldWidgetWrapper



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_source'].widget = RelatedFieldWidgetWrapper(
            self.fields['order_source'].widget,
            Order._meta.get_field('order_source').remote_field,
            self.admin_site,
            can_add_related=True)
        self.fields['order_source'].queryset = Source.objects.all()

        self.fields['order_spec_occasion'].widget = RelatedFieldWidgetWrapper(
            self.fields['order_spec_occasion'].widget,
            Order._meta.get_field('order_spec_occasion').remote_field,
            self.admin_site,
            can_add_related=True)
        self.fields['order_spec_occasion'].queryset = SpecOccasion.objects.all()

        self.fields['order_inclusions'].widget = RelatedFieldWidgetWrapper(
            forms.SelectMultiple(),
            Order._meta.get_field('order_inclusions').remote_field,
            self.admin_site,
            can_add_related=True)
        self.fields['order_inclusions'].queryset = Inclusion.objects.all()

    class Meta:
        model = Order
        fields = '__all__'
        exclude = (
            'order_creator', 'order_status')
        widgets = {
            'order_guest_check_in_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order_guest_check_out_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
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
