# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models

class VehicleRepairTag(models.Model):
    _name = 'vehicle.repair.tag'

    name = fields.Char()
    color = fields.Char(string="Color")