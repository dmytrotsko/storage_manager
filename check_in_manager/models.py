from django.db import models
from indussystem.models import Villa, User


class Source(models.Model):
    source_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.source_name

    class Meta:
        db_table = 'Source'


class SpecOccasion(models.Model):
    spec_occasion_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.spec_occasion_name

    class Meta:
        db_table = 'SpecOccasion'


class Offer(models.Model):
    offer_villa = models.ForeignKey(Villa, on_delete=models.CASCADE)
    offer_price_per_night = models.IntegerField()
    offer_tax = models.IntegerField()
    offer_order_id = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Offer'


class Inclusion(models.Model):
    inclusion_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.inclusion_text

    class Meta:
        db_table = 'Inclusion'


class Order(models.Model):
    order_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    order_guest_name = models.CharField(max_length=255)
    order_guest_cell_number = models.CharField(max_length=255)
    order_guest_email = models.EmailField()
    order_guest_whatsapp = models.CharField(max_length=255)
    order_guest_check_in_date = models.DateField(auto_now_add=False, null=True, blank=True)
    order_guest_check_out_date = models.DateField(auto_now_add=False, null=True, blank=True)
    order_early_check_in_required = models.NullBooleanField(null=True, blank=True)
    order_late_check_out_required = models.NullBooleanField(null=True, blank=True)
    order_number_of_adults = models.PositiveIntegerField(null=True, blank=True)
    order_number_of_kids = models.PositiveIntegerField(null=True, blank=True)
    order_source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    order_spec_occasion = models.ForeignKey(SpecOccasion, on_delete=models.CASCADE, null=True, blank=True)
    order_guest_balance = models.IntegerField(null=True, blank=True)
    order_price = models.IntegerField(null=True, blank=True)
    order_comment = models.TextField(blank=True, null=True)
    order_notes = models.TextField(null=True, blank=True)
    order_inclusions = models.ManyToManyField(Inclusion, blank=True)

    ORDER_STATUS_CHOICES = [
        ('waiting_to_send_offer', 'Client is waiting for offers.'),
        ('waiting_for_client_to_accept_offer', 'Waiting for client to accept offer.'),
        ('client_accepted_offer', 'Client accepted the offer.'),
        ('order_accepted', 'Order is accepted.'),
        ('order_waiting_for_manager', 'Order is waiting manager to to some stuff.'),
        ('order_accepted_by_guest', 'Client completely accepted the order.'),
        ('order_declined_by_guest', 'Client declined the order due to some reason')
    ]
    order_status = models.CharField(
        max_length=50,
        choices=ORDER_STATUS_CHOICES,
        default='waiting_to_send_offer'
    )

    order_chosen_villa = models.ForeignKey(Villa, on_delete=models.CASCADE, null=True, blank=True)
    order_decline_reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'Order'
