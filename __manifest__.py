# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'vehicle_repair_management',
    'version': '1.0',
    'category': 'Vehicle Repair Management',
    'summary': 'Vehicle Repair Management Module',
    'depends': ['base','fleet','mail','hr','hr_timesheet','stock'],
    'application': True,
    'installable': True,
    'sequence': -3,

    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_repair_views.xml',
        'views/vehicle_repair_tag_view.xml',
        'views/res_partner_view.xml',
        'views/vehicle_search_view.xml',
        'views/vehicle_repair_menu.xml',
    ],
    'demo': ['data/fleet_demo.xml'],

}
