ORDER_STATUS_CHOICES = (
    ('waiting_to_send_offer', 'Client is waiting for offers.'),
    ('waiting_for_client_to_accept_offer', 'Waiting for client to accept offer.'),
    ('client_accepted_offer', 'Client accepted the offer.'),
    ('order_accepted', 'Order is accepted.'),
    ('order_waiting_for_manager', 'Order is waiting manager to to some stuff.'),
    ('order_accepted_by_guest', 'Client completely accepted the order.'),
    ('order_declined_by_guest', 'Client declined the order due to some reason')
)
