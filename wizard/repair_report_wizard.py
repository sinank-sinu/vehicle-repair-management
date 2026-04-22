# -*- coding: utf-8 -*-
import json
from odoo import models, fields
import io
import xlsxwriter
from odoo.tools import json_default


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

    def action_print_xlsx(self):
        report_model = self.env['report.vehicle_repair_management.report_repair_details_template']
        data = {'form': self.read()[0]}

        report_values = report_model._get_report_values(None, data=data)

        report_data = {
            'model_id': self.id,
            'docs': report_values['docs'],
            'start_date': data['form']['start_date'],
            'end_date': data['form']['end_date'],
            'single_customer': report_values.get('single_customer'),
            'single_advisor': report_values.get('single_advisor'),
        }

        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'repair.report.wizard',
                'options': json.dumps(report_data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Vehicle Repair Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Repairs')

        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '18px'})
        table_head = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#EEEEEE'})
        txt = workbook.add_format({'font_size': '10px', 'border': 1})
        date_txt = workbook.add_format({'font_size': '10px', 'border': 1, 'num_format': 'yyyy-mm-dd'})

        sheet.merge_range('A3:G3', 'VEHICLE REPAIR REPORT', head)

        if data.get('single_customer'):
            sheet.write('A4', 'CUSTOMER:', table_head)
            sheet.write('B4', data['single_customer'], txt)

        if data.get('single_advisor'):
            sheet.write('C4', 'ADVISOR:', table_head)
            sheet.write('D4', data['single_advisor'], txt)

        columns = ['Model', 'Vehicle No', 'Customer', 'Advisor', ' Start Date','End date', 'State',
                   'Vehicle Type','Service Type','Amount']
        for col, title in enumerate(columns):
            sheet.write(6, col, title, table_head)

        row = 7
        for line in data.get('docs', []):
            sheet.write(row, 0, line.get('model'), txt)
            sheet.write(row, 1, line.get('vehicle_number'), txt)
            sheet.write(row, 2, line.get('customer'), txt)
            sheet.write(row, 3, line.get('advisor'), txt)
            sheet.write(row, 4, str(line.get('start_date')), date_txt)
            sheet.write(row, 5, str(line.get('end_date')), date_txt)
            sheet.write(row, 6, line.get('state'), txt)
            sheet.write(row, 7, line.get('vehicle_type'), txt)
            sheet.write(row, 8, line.get('service_type'), txt)
            sheet.write(row, 9, line.get('total_amount'), txt)
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
