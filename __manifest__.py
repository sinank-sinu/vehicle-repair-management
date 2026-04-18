# -*- coding: utf-8 -*-

{
    'name': 'vehicle_repair_management',
    'version': '1.0',
    'category': 'Vehicle Repair Management',
    'summary': 'Vehicle Repair Management Module',
    'depends': ['base','fleet','mail','hr','hr_timesheet','stock','product','uom','contacts','base_automation'],
    'application': True,
    'installable': True,
    'sequence': -3,

    'data': [
        'data/ir_cron.xml',
        'data/reference_sequence.xml',
        'data/repair_email.xml',
        'data/product_demo.xml',
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'wizard/repair_report.xml',
        'reports/report_action_template.xml',
        'views/vehicle_repair_views.xml',
        'views/vehicle_repair_tag_view.xml',
        'views/res_partner_view.xml',
        'views/vehicle_search_view.xml',
        'views/vehicle_repair_menu.xml',
    ],
    'demo': ['data/fleet_demo.xml'],

}
