# -*- coding: utf-8 -*-

from odoo import models, api

class VehicleReportTemplateAbstract(models.AbstractModel):
    _name = 'report.vehicle_repair_management.report_repair_details_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        """This function is to fetch data from database,And finding  """
        form = data.get('form')

        query = """
        SELECT
        vm.name AS model,
        vr.vehicle_number,
        rp.name AS customer,
        advisor_partner.name AS advisor,
        vr.start_date,
        vr.deliver_date AS end_date,
        vr.state,
        vt.name AS vehicle_type,
        vr.service_type,
        vr.estimated_amount,
        vr.total_parts_labor_cost AS total_amount
        FROM vehicle_repair vr
        JOIN fleet_vehicle_model vm ON vr.vehicle_model_id = vm.id
        JOIN fleet_vehicle_model_category vt ON vr.vehicle_type_id = vt.id
        JOIN res_partner rp ON vr.partner_id = rp.id
        JOIN res_users ru ON vr.salesperson_id = ru.id
        JOIN res_partner advisor_partner ON ru.partner_id = advisor_partner.id
        WHERE vr.start_date >= %s
        AND vr.start_date <= %s
        """
        params = [form['start_date'], form['end_date']]

        if form.get('partner_ids'):
            query += " AND vr.partner_id IN %s"
            params.append(tuple(form['partner_ids']))

        if form.get('salesperson_ids'):
            query += " AND vr.salesperson_id IN %s"
            params.append(tuple(form['salesperson_ids']))

        self.env.cr.execute(query, params)
        res = self.env.cr.dictfetchall()

        partner_ids = form.get('partner_ids', [])
        salesperson_ids = form.get('salesperson_ids', [])

        return {
        'docs': res,
        'single_customer': self.env['res.partner'].browse(partner_ids[0]).name
        if len(partner_ids) == 1 else False,
        'single_advisor': self.env['res.users'].browse(salesperson_ids[0]).name
        if len(salesperson_ids) == 1 else False,
        }