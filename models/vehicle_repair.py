# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from pydoc import visiblename

from odoo import models, fields,api
from datetime import date
from dateutil.relativedelta import relativedelta
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
    company_id = fields.Many2one('res.company',string='Company',
                                 default=lambda self: self.env.user.company_id,readonly=True)
    currency_id = fields.Many2one('res.currency',string='Currency',required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
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
    total_parts_labor_cost = fields.Monetary(
        string='Total Combined Cost',
        compute='_compute_total_parts_labor_cost',
        store=True
    )
    status = fields.Selection([('archived','Archived')])
    duration=fields.Integer(string='Duration',default=0)
    estimated_date = fields.Date(string='Estimated Date',compute='_compute_estimated_date')
    invoice_id = fields.Many2one('account.move', string='Invoice', copy=False)
    invoice_count= fields.Char(compute='_compute_total_invoice_count', store=True)
    payment_state = fields.Selection(
        related='invoice_id.payment_state',
        string="Payment Status",
        store=True
    )
    deliver_date= fields.Date(string='Delivery Date',default=lambda self: date.today())
    def action_confirm(self):
        self.write({'state': 'in progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_ready_for_delivery(self):
        """this function is used to determine if the delivery is ready for delivery and send the mail to customer"""
        template = self.env.ref('vehicle_repair_management.repair_email_template')
        email_values = {'email_from': self.env.user.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)
        self.write({'state': 'ready for delivery'})

    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError("Cannot cancel a completed delivery.")
            record.state = 'cancel'

    @api.model_create_multi
    def create(self, vals_list):
        """this function is for computing the sequence number"""
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('vehicle.repair.management')
        return super().create(vals_list)

    @api.depends('labor_line_ids.subtotal')
    def compute_total_labor_cost(self):
        """this function is used to compute the total labor cost"""
        for record in self:
            record.total_labor_cost = sum(line.subtotal for line in record.labor_line_ids)

    @api.constrains('vehicle_number')
    def check_vehicle_number_unique(self):
        """this function is to check the vehicle number is unique"""
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('vehicle_number', '=', record.vehicle_number),
            ]
            if self.search_count(domain) > 0:
                raise UserError("Vehicle number must be unique.")

    @api.depends('consumed_part_ids.subtotal')
    def _compute_total_parts_cost(self):
        """this function is to compute the total parts consumed"""

        for record in self:
            record.total_parts_cost = sum(line.subtotal for line in record.consumed_part_ids)

    @api.depends('total_labor_cost', 'total_parts_cost')
    def _compute_total_parts_labor_cost(self):
        """this function is to compute the total labor cost and consumed parts"""
        for record in self:
            record.total_parts_labor_cost=  record.total_parts_cost + record.total_labor_cost

    @api.onchange('vehicle_type_id')
    def onchange_vehicle_type(self):
        """this function is to ,when vehicle type erased then related field is erased"""
        if self.vehicle_type_id or not self.vehicle_type_id:
            self.vehicle_model_id=False

    def action_create_invoice(self):
        """Creates the invoice and then returns the view of that specific invoice"""
        self.ensure_one()
        existing_invoice = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'draft'), ],limit=1)

        invoice_lines = []
        for labor in self.labor_line_ids:
            invoice_lines.append((0, 0, {
                'name': labor.employee_id.name or 'Labor',
                'quantity': labor.hours_spent,
                'price_unit': labor.hourly_cost,
            }))
        for part in self.consumed_part_ids:
            invoice_lines.append((0, 0, {
                'name': part.product_id.name,
                'quantity': part.qty,
                'price_unit': part.unit_price,
            }))
        if existing_invoice:
            existing_invoice.write({
                'invoice_line_ids': invoice_lines,
            })
            self.invoice_id = existing_invoice.id
        else:
            new_invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': invoice_lines,
             })
            self.invoice_id = new_invoice.id
        return self.action_view_invoice()

    def action_view_invoice(self):
        """this function is to display the invoice view"""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError("No products added.")

        return {
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    @api.depends('invoice_id','invoice_count')
    def _compute_total_invoice_count(self):
        """this function is to compute the total invoice count"""
        for record in self:
         if record.invoice_id:
            record.invoice_count = 1
         else:
            record.invoice_count = 0

    @api.model
    def action_cron(self):
        """this function is to create the cron job"""
        exact_record=self.search([
            ('state', '=', 'cancel'), ])
        for record in exact_record:
            exact_day=date.today()
            day_to_archive=record.start_date + relativedelta(days=30)
            if exact_day == day_to_archive:
              record.active=False

    @api.depends('start_date')
    def _compute_estimated_date(self):
        """this function is to compute the estimated date"""
        for record in self:
            record.estimated_date = record.start_date + relativedelta(days=record.duration)


