# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api
from datetime import date
from odoo.exceptions import UserError




class VehicleRepair(models.Model):
    _name = 'vehicle.repair'
    _description = "vehicle repair management"
    _inherit = ['mail.thread']

    image_1920 = fields.Image(string="vehicle image")

    mobile_no = fields.Char(related='partner_id.phone', readonly=True)

    active = fields.Boolean(default=True)
    start_date = fields.Date( string="Start date",required=True,default=lambda self: date.today() , copy=False )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, change_default=True, index=True,
        tracking=1,
        check_company=True)
    salesperson_id = fields.Many2one(
        'res.users',
        string=' service advisor',
        default=lambda self: self.env.user
    )
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.user.company_id)
    validity = fields.Integer(default=4)
    estimated_amount= fields.Float( )
    customer_complaint= fields.Text()
    vehicle_type_id = fields.Many2one(
        'fleet.vehicle.model.category',
        string='Vehicle Type',
        required=True,
    )
    vehicle_model_id = fields.Many2one(
        'fleet.vehicle.model',
        string='Vehicle Model',
        required=True,
        domain="[('category_id', '=', vehicle_type_id)]"
    )
    vehicle_number = fields.Char(string='Vehicle Number', required=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in progress', 'In Progress'),
        ('ready for delivery', 'Ready for Delivery'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ],default='draft', required=True, copy=False, tracking=True)

    def action_confirm(self):
        self.write({'state': 'in progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_ready_for_delivery(self):
        self.write({'state': 'ready for delivery'})


    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError("Cannot cancel a completed delivery.")
            record.state = 'cancel'

    tag_ids = fields.Many2many(
        'vehicle.repair.tag',
        string='Tags',required=True)

    reference = fields.Char(string='Reference', default='New', readonly=True)


    # this function is for computing the sequence number
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('vehicle.repair.management')
        return super().create(vals_list)


    # this function is to check the vehicle number is unique
    @api.constrains('vehicle_number')
    def check_vehicle_number_unique(self):
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('vehicle_number', '=', record.vehicle_number),
            ]

            if self.search_count(domain) > 0:
                raise UserError("Vehicle number must be unique.")