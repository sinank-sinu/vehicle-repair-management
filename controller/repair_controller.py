from odoo import http
from odoo.http import request

class SnippetController(http.Controller):
    @http.route('/repairs', type='json', auth="public", website=True)
    def get_top_repairs(self):
        print("------- controller---")
        repairs = request.env['vehicle.repair'].sudo().search_read([],limit=4)
        print(repairs)
        return repairs
