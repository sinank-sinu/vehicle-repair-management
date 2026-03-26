# -*- coding: utf-8 -*-

from odoo import fields,models

class VehicleRepairTag(models.Model):
    _name = 'vehicle.repair.tag'

    name = fields.Char()
    color = fields.Char(string="Color")

