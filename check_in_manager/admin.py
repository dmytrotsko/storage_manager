from django.contrib import admin

from .models import (
    Source,
    SpecOccasion,
    Offer,
    Inclusion,
    Order,
)

from .forms import OrderForm


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'source_name',
    )
    search_fields = (
        'source_name',
    )


admin.site.register(Source, SourceAdmin)


class SpecOccasionAdmin(admin.ModelAdmin):
    list_display = (
        'spec_occasion_name',
    )
    search_fields = (
        'spec_occasion_name',
    )


admin.site.register(SpecOccasion, SpecOccasionAdmin)


class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'offer_villa', 'offer_price_per_night',
        'offer_tax',
    )
    search_fields = (
        'offer_villa',
    )


admin.site.register(Offer, OfferAdmin)


class InclusionAdmin(admin.ModelAdmin):
    list_display = (
        'inclusion_text',
    )


admin.site.register(Inclusion, InclusionAdmin)


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm

    def __init__(self, model, admin_site):
        super(OrderAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    list_display = [field.name for field in Order._meta.get_fields(
    ) if field.name != 'order_inclusions']
    search_fields = (
        'order_creator', 'order_guest_name',
        'order_guest_cell_number', 'order_guest_email',
        'order_guest_check_in_date', 'order_guest_check_out_date',
    )


admin.site.register(Order, OrderAdmin)
