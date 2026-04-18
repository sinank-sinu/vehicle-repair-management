from odoo import models, fields,api

class RepairReportWizard(models.TransientModel):
    _name = 'repair.report.wizard'
    _description = 'Repair Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    partner_ids = fields.Many2many('res.partner', string="Customers")
    salesperson_id = fields.Many2many('res.users', string="Service Advisors")

    def action_print_report(self):
        domain = []
        if self.start_date:
            domain.append(('create_date', '>=', self.start_date))
        if self.end_date:
            domain.append(('create_date', '<=', self.end_date))
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        if self.salesperson_id:
            domain.append(('salesperson_id', 'in', self.salesperson_id.ids))

        repairs = self.env['vehicle.repair'].search(domain)

        data = {
            'form': self.read()[0],
            'repairs': repairs.ids,
            'multi_customer': len(self.partner_ids) > 1 or not self.partner_ids,
            'multi_advisor': len(self.salesperson_id) > 1 or not self.salesperson_id,
        }
        return self.env.ref('vehicle_repair_management.action_report_repair_wizard').report_action(self, data=data)
    