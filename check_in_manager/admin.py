from django.contrib import admin

from .models import (
    Source,
    SpecOccasion,
    Offer,
    Inclusion,
    Order,
    # Call
)


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
    list_display = (
        'order_creator', 'order_guest_name',
        'order_guest_cell_number', 'order_guest_email',
        'order_guest_whatsapp', 'order_guest_check_in_date',
        'order_guest_check_out_date', 'order_early_check_in_required',
        'order_late_check_out_required', 'order_number_of_adults',
        'order_number_of_kids', 'order_source',
        'order_spec_occasion', 'order_waiting_for_manager',
        'order_accepted', 'order_accepted_by_guest',
        'order_declined_by_guest', 'order_offer',
        'order_decline_reason', 'order_chosen_villa',
        'order_guest_balance', 'order_price',
        'order_alerted', 'order_comment',
        'order_notes',
    )
    search_fields = (
        'order_creator', 'order_guest_name',
        'order_guest_cell_number', 'order_guest_email',
        'order_guest_check_in_date', 'order_guest_check_out_date',
    )


admin.site.register(Order, OrderAdmin)


# class CallAdmin(admin.ModelAdmin):
#     list_display = (
#         'call_date', 'call_message',
#         'call_order',
#     )
#     search_fields = (
#         'call_date',
#     )
#
#
# admin.site.register(Call, CallAdmin)
