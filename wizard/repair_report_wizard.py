from odoo import models, fields

class RepairReportWizard(models.TransientModel):
    _name = 'repair.report.wizard'
    _description = 'Vehicle Repair Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    partner_ids = fields.Many2many('res.partner', string='Customers')
    salesperson_ids = fields.Many2many('res.users', string='Service Advisors')

    def action_print_report(self):
       data = {'form': self.read()[0]}
       return self.env.ref('vehicle_repair_management.action_report_repair_wizard' ).report_action(self, data=data)