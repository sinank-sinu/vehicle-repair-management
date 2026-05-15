from odoo import http
from odoo.http import request


class WebsiteSaleClearCart(http.Controller):

    @http.route(['/shop/clear_cart'], type='json', auth="public", website=True)
    def clear_cart(self):
        order = request.cart
        order.unlink()
        return True
