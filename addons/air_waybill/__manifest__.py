# -*- coding: utf-8 -*-
{
    'name': 'Air Waybill',
    'version': '1.0',
    'summary': 'Air Waybill Management with Financial Lines',
    'description': """
        Module to manage Air Waybills with financial lines and toggle columns in the list view.
    """,
    'author': 'Your Name',
    'category': 'Operations',
    'depends': ['base', 'mail', 'sale', 'web'],  # add any other dependencies
    'data': [
        'security/ir.model.access.csv',
        'views/air_waybill_views.xml',
        'views/menu_views.xml',  # <-- Add this line
    ],
    'assets': {
        'web.assets_backend': [
            'air_waybill/static/src/js/financial_column_toggle.js',
            'air_waybill/static/src/css/financial_column_toggle.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
