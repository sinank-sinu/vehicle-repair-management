# -*- coding: utf-8 -*-
import json
from odoo import models, fields
import io
import xlsxwriter
from odoo.tools import json_default


class RepairReportWizard(models.TransientModel):
    _name = 'repair.report.wizard'
    _description = 'Vehicle Repair Report Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    partner_ids = fields.Many2many('res.partner', string='Customers')
    salesperson_ids = fields.Many2many('res.users', string='Service Advisors')

    def action_print_report(self):
       data = {'form': self.read()[0]}
       return self.env.ref('vehicle_repair_management.action_report_repair_wizard' ).report_action(self, data=data)

    def action_print_xlsx(self):
        """This function is to fetch data and return"""
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
        """This function is used to customize the xlsx report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Repairs')

        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '18px','bg_color': 'EEEEEE'})
        table_head = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#EEEEEE','align': 'center'})
        txt = workbook.add_format({'font_size': '10px', 'border': 1,'align': 'center'})
        sheet.merge_range('B2:K3', 'VEHICLE REPAIR REPORT', head)

        if data.get('single_customer'):
            sheet.write('A4', 'CUSTOMER:', txt)
            sheet.write('B4', data['single_customer'], txt)

        if data.get('single_advisor'):
            sheet.write('A5', 'ADVISOR:', txt)
            sheet.write('B5', data['single_advisor'], txt)

        headers = [('Model:', 'model'), ('Vehicle No:', 'vehicle_number')]

        if not data.get('single_customer'):
            headers.append(('Customer:', 'customer'))

        if not data.get('single_advisor'):
            headers.append(('Advisor:', 'advisor'))

        headers.extend([('Start Date:', 'start_date'),('End Date:', 'end_date'),('State:', 'state'),('Vehicle Type:', 'vehicle_type'),
                        ('Service Type:', 'service_type'),('Total:', 'total_amount')
        ])

        for col, (header_label, field_name) in enumerate(headers):
            sheet.write(6, col, header_label, table_head)
            sheet.set_column(col, col, 15)

        row = 7
        for line in data.get('docs', []):
            for col, (header_label, field_name) in enumerate(headers):
                val = line.get(field_name)
                sheet.write(row, col, val if val else '0')
            row += 1

        workbook.close()

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
