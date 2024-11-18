from django.shortcuts import render,redirect,get_object_or_404
from cart.models import Cart
from .models import Order,OrderItem
from account.forms import AddressFrom
from django.conf import settings
from django.db.models import Sum

# Create your views here.
def order_create(request):

    cart_list = Cart.objects.filter(user=request.user)
    if request.method == 'POST':

        order = Order.objects.create(user=request.user)
        for cart in cart_list:
            OrderItem.objects.create(order=order,
                                     product=cart.products,
                                     price=cart.products.price,
                                     quantity=cart.quantity,
                                     )
        form = AddressFrom(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            order.address = address
            order.save()
            request.session['order_id'] = order.id
        # return redirect('create-checkout-session')
        # return render(request,'order/thanks_mgs.html',{'order':order})
    else:
        form = AddressFrom()
    all_total_sub_price = sum(cart.total() for cart in cart_list)

    shipping_fe = settings.DELIVERY_FEES
    all_total_price = shipping_fe + all_total_sub_price

    return render(request,'order/create_order.html',{'cart_list':cart_list,
                                                     'all_total_sub_price':all_total_sub_price,
                                                     'all_total_price':all_total_price,
                                                     'form': form,
                                                     })


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response



from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = "order/success.html"

class CancelView(TemplateView):
    template_name = "order/cancel.html"

from django.views import View
import stripe
class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """
    # order = Cart.objects.get(id=)
    def post(self, request, *args, **kwargs):
        order_id = request.session.get('order_id', None)
        orders = Cart.objects.filter(user=request.user)

        line_items = []

        for order in orders:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(order.products.price * order.quantity) * 100,  # Assuming order.products.price is the unit amount
                    "product_data": {
                        "name": order.products.name,
                        "description": f'Quantity : {order.quantity}',
                        "images": [
                            "http://127.0.0.1:8000/media/product_images/download_2_71UyFGv.jpeg"
                        ],
                    },
                },
                "quantity": 1,  # Adjust this according to your use case, e.g., order.quantity
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            metadata={"order_id": order_id},
            mode="payment",
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return redirect(checkout_session.url)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = "whsec_d6e1dd28aa02ba70e1c2c35da87424d00fea030389f7b234b33bc0bbdf3ab3a4"
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event['data']['object']['metadata']
            print(session)

        # Can handle other events here.

        return HttpResponse(status=200)