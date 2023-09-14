from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .forms import OrderForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import *

class PlaceOrderView(View):
    template_name = 'dispatch_app/product_list.html'

    def get(self, request):
        form = OrderForm()
        products = Product.objects.all()
        return render(request, self.template_name, {'form': form, 'products': products})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            # Get or create a customer based on the provided customer name
            customer_name = form.cleaned_data['customer_name']
            customer, created = Customer.objects.get_or_create(name=customer_name, defaults={'email': '', 'phone_number': ''})

            # Get or create a dispatcher (you can modify this logic as needed)
            dispatcher_name = 'Default Dispatcher'  # Change this to the name of the dispatcher you want to assign
            dispatcher, created = Dispatcher.objects.get_or_create(name=dispatcher_name, defaults={'email': '', 'phone_number': ''})

            # Create a new Order instance and set its fields
            order = Order(customer=customer, dispatcher=dispatcher)
            order.save()
            

            # You can also perform other actions here, such as sending email notifications

            # Use reverse to generate the URL for 'order_placed'
            return redirect(reverse('dispatch_app:order_placed', args=[order.id]))
        else:
            # If the form is not valid, re-render the form page with errors
            products = Product.objects.all()
            return render(request, self.template_name, {'form': form, 'products': products})

class OrderPlacedView(TemplateView):
    template_name = 'dispatch_app/order_placed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs['order_id']  # Get the order_id from URL parameter
        order = Order.objects.get(id=order_id)
        context['order'] = order
        return context

class OrderListView(View):
    template_name = 'dispatch_app/order_list.html'

    def get(self, request):
        orders = Order.objects.all()
        context = {'orders': orders}  # Pass the orders queryset to the context
        return render(request, self.template_name, context)


class OrderStatusView(View):
    template_name = 'dispatch_app/order_status.html'

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None

        return render(request, self.template_name, {'order': order})