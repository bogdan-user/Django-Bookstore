from .models import Basket


def basket_middleware(get_response):
    def middleware(request):
        user = request.user
        if 'basket_id' in request.session:
            basket_id = request.session['basket_id']
            try:
                basket = Basket.objects.get(id=basket_id)
                request.basket = basket
            except:
                try:
                    basket = Basket.objects.get(user=user, status=Basket.OPEN)
                    request.basket = basket
                except:
                    del request.session['basket_id']
        else:
            try:
                basket = Basket.objects.get(user=user, status= Basket.OPEN)
                request.basket = basket
            except:
                request.basket = None

        response = get_response(request)
        return response
    return middleware
