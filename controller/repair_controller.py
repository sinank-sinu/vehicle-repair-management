
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class SnippetController(http.Controller):
    @http.route('/repairs', type='json', auth="public", website=True)
    def get_top_repairs(self):
        """Fetch repair data and return it."""
        repairs = request.env['vehicle.repair'].sudo().search_read([('id', '!=', None)],
            fields=['partner_id', 'vehicle_type_id', 'vehicle_model_id', 'vehicle_number', 'image_1920', 'id'],
            order='id DESC')
        values = {
            'repairs': repairs
        }
        return values
