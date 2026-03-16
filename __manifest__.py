{
    'name': 'vehicle_repair_management',
    'version': '1.0',
    'category': 'Vehicle Repair Management',
    'summary': 'Vehicle Repair Management Module',
    'depends': ['base','fleet','mail'],
    'application': True,
    'installable': True,
    'sequence': -3,

    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_repair_views.xml',
        'views/vehicle_repair_tag_view.xml',
        'views/vehicle_repair_menu.xml',
    ],
    'demo': ['data/fleet_demo.xml'],

}
