from django.conf import settings
import stripe


stripe.api_key = 'sk_test_51MSdkYCvPYglVOw12nEHPQnxAOdwtP4An5vN3pWb985jRZ5yPA17Um5sVsTvCSmjsGJz7hzSfPtrpAGgRsPnl12z00wMcgwdgK'
st_price = {'id': None}


def create_stripe_price(price):
    new_price = stripe.Price.create(
        unit_amount=price*100,
        currency="usd",
        product="prod_ND6h6U3kt3YBrS",
        )
    st_price['id'] = new_price
    pass
