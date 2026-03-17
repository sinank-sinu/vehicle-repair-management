# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models

class ServiceLaborLine(models.Model):
    _name = 'service.labor.line'
    _description = 'Service Labor Line'

    repair_id = fields.Many2one('vehicle.repair', string="Repair Reference", ondelete='cascade')
    detail = fields.Char(string='Labor Detail', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    hours_spent = fields.Float(string='Hours Spent')

    currency_id = fields.Many2one(related='repair_id.currency_id', store=True, readonly=True)

    hourly_cost = fields.Monetary(
        related='employee_id.hourly_cost',
        string='Hourly Rate'
    )

    subtotal = fields.Monetary(
        string='Subtotal',
        compute='compute_subtotal',
        store=True
    )
    @api.depends('hours_spent', 'hourly_cost')
    def compute_subtotal(self):
        """compute the subtotal of hourly cost"""
        for line in self:
            line.subtotal = line.hours_spent * line.hourly_cost
