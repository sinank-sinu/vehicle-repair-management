# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class HelloWorld(http.Controller):
    @http.route('/hello-odoo', type='http', auth='public', website=True)
    def hello_page(self, **kwargs):
        """
        This controller handles the request for the /hello-odoo page.
        It renders a QWeb template and passes a dynamic value.
        """
        user_name = request.env.user.name if request.env.user.id else 'Guest'

        return request.render('vehicle_repair_management.repair_page_template', {
            'user_name': user_name,
        })

    @http.route('/website/customer/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        """Handle form submission"""
        name = post.get('name')
        types = post.get('vehicle_type')
        model = post.get('vehicle_model')
        vehicle_no = post.get('vehicle_no')

        existing = request.env['vehicle.repair'].sudo().search([('vehicle_number', '=', vehicle_no)], limit=1)
        if existing:
            return request.render('vehicle_repair_management.customer_error', {
                'error_msg': 'This vehicle number is already registered!',
            })

        file1 = post.get('file1')
        image_base64 = False

        if file1:
            image_base64 = base64.b64encode(file1.read())

        request.env['vehicle.repair'].sudo().create({
            'partner_id': (name),
            'vehicle_model_id': (model),
            'vehicle_type_id': (types),
            'vehicle_number': vehicle_no,
            'image_1920': image_base64,
        })
        return request.render('vehicle_repair_management.customer_success_template')





