# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    service_count = fields.Integer(compute='_compute_service_count')
    def _compute_service_count(self):
        """this function is for updating the service count"""
        for partner in self:
            partner.service_count = self.env['vehicle.repair'].search_count([
                ('partner_id', '=', partner.id)
            ])
    def action_service_count(self):
        """this function is for actioning the service count"""
        self.ensure_one()
        return {
            'name': 'Service Count',
            'type': 'ir.actions.act_window',
            'res_model': 'vehicle.repair',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id, 'order': 'start_date desc'},
        }