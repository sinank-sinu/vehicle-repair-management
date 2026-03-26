# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ConsumedPart(models.Model):
    _name = 'consumed.part'
    _description = 'Consumed Part'

    repair_id = fields.Many2one('vehicle.repair')
    product_id = fields.Many2one('product.product',string='parts',domain=[('type', 'in',['product','consu','service'])])
    qty=fields.Float(string='Quantity',default=1)
    unit_price = fields.Monetary(string='Price')
    currency_id = fields.Many2one('res.currency',string='Currency')
    subtotal = fields.Monetary(string='Subtotal',compute='compute_subtotal' ,store=True)
    @api.depends('qty', 'unit_price')
    def compute_subtotal(self):
        """this function is for computing the subtotal"""
        for line in self:
            line.subtotal = line.qty * line.unit_price


