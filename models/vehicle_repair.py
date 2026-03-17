# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api
from datetime import date
from odoo.exceptions import UserError

class VehicleRepair(models.Model):
    _name = 'vehicle.repair'
    _description = "vehicle repair management"
    _rec_name = 'vehicle_type_id'
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
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.user.company_id,readonly=True)
    currency_id = fields.Many2one('res.currency',string='Currency',required=True, default=lambda self: self.env.user.company_id.currency_id)
    estimated_amount= fields.Monetary(string='Estimated Amount')
    customer_complaint= fields.Text(string='Customer Complaint')
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
    tag_ids = fields.Many2many(
        'vehicle.repair.tag',
        string='Tags',required=True)
    reference = fields.Char(string='Reference', default='New', readonly=True)
    service_type = fields.Selection([
        ('un paid', 'Un Paid'),
        ('paid', 'Paid'),
    ], string='Service Type', default='un paid', required=True, tracking=True)

    labor_line_ids = fields.One2many('service.labor.line', 'repair_id',
                                     string='Labor Tracking')
    total_labor_cost = fields.Float(
        string='Total Labor Cost',
        compute='compute_total_labor_cost',
        store=True
    )
    consumed_part_ids = fields.One2many('consumed.part', 'repair_id', string='Consumed Parts')
    total_parts_cost = fields.Monetary(string='Total Parts Cost', compute='_compute_total_parts_cost', store=True)

    """this function is used to compute the total labor cost"""
    @api.depends('labor_line_ids.subtotal')
    def compute_total_labor_cost(self):
        for record in self:
            record.total_labor_cost = sum(line.subtotal for line in record.labor_line_ids)

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

    """this function is for computing the sequence number"""
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('vehicle.repair.management')
        return super().create(vals_list)

    """this function is to check the vehicle number is unique"""
    @api.constrains('vehicle_number')
    def check_vehicle_number_unique(self):
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('vehicle_number', '=', record.vehicle_number),
            ]
            if self.search_count(domain) > 0:
                raise UserError("Vehicle number must be unique.")

    """this function is to check the total labor cost"""
    @api.depends('consumed_part_ids.subtotal')
    def _compute_total_parts_cost(self):
        for record in self:
            record.total_parts_cost = sum(line.subtotal for line in record.consumed_part_ids)

