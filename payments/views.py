from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from .stripe_create_prices import st_price 
import stripe



class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"



class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        DOMAIN = 'http://127.0.0.1:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': st_price['id'],
                    }
                ]
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'error': str(e)})
