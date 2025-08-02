# orders/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from menu.models import Product
from .forms import OrderForm
from .models import Order

def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket = request.session.get('basket', {})

    if str(product_id) in basket:
        basket[str(product_id)] += 1
    else:
        basket[str(product_id)] = 1

    request.session['basket'] = basket
    return redirect('view_basket')

def view_basket(request):
    basket = request.session.get('basket', {})
    items = []
    total = 0

    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'booking/basket.html', {'items': items, 'total': total})


def delete_from_basket(request, product_id):
    basket = request.session.get('basket', {})

    product_id_str = str(product_id)
    if product_id_str in basket:
        del basket[product_id_str]
        request.session['basket'] = basket

    return redirect('view_basket')

@login_required
def place_order_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_price = quantity * product.price
            Order.objects.create(
                product=product,
                quantity=quantity,
                total_price=total_price,
                user=request.user
            )
            return redirect('product_list')  
    else:
        form = OrderForm()

    return render(request, 'booking/place_order.html', {'form': form, 'product': product})


@login_required
def create_orders_from_basket(request):
    basket = request.session.get('basket', {})

    if not basket:
        return redirect('view_basket')

    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity

        Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            user=request.user
        )

    request.session['basket'] = {}

    return redirect('order_success')

def order_success_view(request):
    return render(request, 'booking/order_success.html')