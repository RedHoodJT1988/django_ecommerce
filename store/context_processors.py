def cart_quantity(request):
    cart = request.session.get("cart", {})
    total = 0
    for item in cart.values():
        if isinstance(item, dict):
            total += item.get("quantity", 0)
        else:
            total += item
    return {"cart_total_quantity": total}
