{
    'name': 'Air Waybill Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage Air Waybills (LTA)',
    'description': """
        This module allows you to manage Air Waybills (LTA) with the following features:
        - Create and store air waybills
        - Track shipment details
        - Manage handling information
        - Record financial details
    """,
    'depends': ['sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/air_waybill_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}