# coding=utf-8

import logging
import json

from django.shortcuts import get_object_or_404, render
from django.views.generic import RedirectView, TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin # View Baseada em Classe
from django.forms import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from time import sleep
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse

from catalog.models import Product

import pagseguro

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED, ST_PP_FAILED, ST_PP_DENIED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import CartItem, Order, OrderItem

logger = logging.getLogger('checkout.views')

class CreateCartItemView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        # logger.debug(f'Produto {product} adicionado ao carrinho.')
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)
        if created:
            message = f'Produto "{product}" adicionado ao carrinho de compras!'
        else:
            message = f'Produto "{product}" atualizado no carrinho de compras!'
        if request.is_ajax():
            return HttpResponse(
                json.dumps({'message': message}), content_type='application/javascript'
                )
        messages.success(self.request, message)
        return redirect('checkout:cart_item')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',), can_delete=True, extra=0)
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
            else:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key), data=self.request.POST or None)
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Carrinho atualizado com sucesso.')
            context['formset'] = self.get_formset(clear=True)

        return self.render_to_response(context)


class ClearCartItemsView(View):

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(user=request.user, cart_items=cart_items)
            cart_items.delete()
            messages.success(self.request, f'O carrinho de compras foi limpo.')
            return redirect('checkout:cart_item')
        messages.info(self.request, f'O carrinho de compras está vazio.')
        return redirect('checkout:cart_item')
        
        #     return HttpResponse(f'O carrinho de compras foi limpo.')
        # return HttpResponse(f'O carrinho de compras foi limpo.')




class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'
    
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(user=request.user, cart_items=cart_items)
            # cart_items.delete()
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response

class OrderListView(LoginRequiredMixin, ListView):

    template_name = 'checkout/order_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):

    template_name = 'checkout/order_detail.html'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class PagSeguroView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        )
        pg = order.pagseguro()
        pg.redirect_url = self.request.build_absolute_uri(
            reverse('accounts:order_detail', args=[order.pk])
        )
        pg.notification_url = self.request.build_absolute_uri(
            reverse('checkout:pagseguro_notification_view')
        )
        response = pg.checkout()
        return response.payment_url


@csrf_exempt
def pagseguro_notification_view(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = pagseguro.PagSeguro(token=settings.PAGSEGURO_TOKEN, 
                       email=settings.PAGSEGURO_EMAIL,
                       config={'sandbox': settings.PAGSEGURO_SANDBOX})
        # print(f'notification_code --> {notification_code}')
        notification_data = pg.check_notification(notification_code)
        # print(f'notification_data --> {notification_data}')
        status = notification_data.status
        # print(f'status --> {status}')
        reference = notification_data.reference
        # print(f'reference --> {reference}')

        try:
            order = Order.objects.get(id=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.update_pagseguro_status(status)
        return HttpResponse('Ok')

class PaypalView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/paypal.html'

    def get_context_data(self, **kwargs):
        context = super(PaypalView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(Order.objects.filter(user=self.request.user), pk=order_pk)
        paypal_dict = order.paypal()
        paypal_dict['return_url'] = self.request.build_absolute_uri(reverse('accounts:order_detail', args=[order.pk]))
        paypal_dict['cancel_return'] = self.request.build_absolute_uri(reverse('checkout:cart_item'))
        paypal_dict['notify_url'] = self.request.build_absolute_uri(reverse('paypal-ipn'))
        context['form'] = PayPalPaymentsForm(initial=paypal_dict)
        return context


@csrf_exempt
def paypal_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED and ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.status = '3'
            order.save()
        except Order.DoesNotExist:
            pass
    elif ipn_obj.payment_status == ST_PP_FAILED or ipn_obj.payment_status == ST_PP_DENIED and ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.status = '7'
            order.save()
        except Order.DoesNotExist:
            pass
    else:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.status = '2'
            order.save()
        except Order.DoesNotExist:
            pass

### Signal PayPal
valid_ipn_received.connect(paypal_notification)


### Calls
create_cart_item = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
checkout_order = CheckoutView.as_view()
order_list = OrderListView.as_view()
order_detail = OrderDetailView.as_view()
pagseguro_view = PagSeguroView.as_view()
paypal_view = PaypalView.as_view()
clear_cart_items = ClearCartItemsView.as_view()
