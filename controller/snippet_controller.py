from odoo import http
from odoo.http import request

class VehicleRepairDashboard(http.Controller):
    @http.route('/repair/get_top_services', type='json', auth="public", website=True)
    def get_top_repairs(self):
        repairs = request.env['vehicle.repair'].sudo().search_read(
            [], ['name', 'id', 'total_parts_labor_cost'], limit=4, order="total_parts_labor_cost desc"
        )
        return repairs


