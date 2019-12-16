# coding=utf-8

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin # View Baseada em Classe
from django.forms import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from time import sleep
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from catalog.models import Product

from .models import CartItem, Order, OrderItem


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)
        if created:
            messages.success(self.request, f'Produto "{product}" adicionado ao carrinho de compras!')
        else:
            messages.success(self.request, f'Produto "{product}" atualizado no carrinho de compras!')

        sleep(0.5)        
        return reverse('checkout:cart_item')

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

class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'
    
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(user=request.user, cart_items=cart_items)
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
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), id=order_id
        )
        pg = order.pagseguro()
        data = pg.checkout()
        if data['success']:
            return data['redirect_url']

@csrf_exempt
def pagseguro_notification_view(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        return HttpResponse('Ok')


create_cart_item = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
checkout_order = CheckoutView.as_view()
order_list = OrderListView.as_view()
order_detail = OrderDetailView.as_view()
pagseguro_view = PagSeguroView.as_view()