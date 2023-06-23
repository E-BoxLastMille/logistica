# -*- coding: utf-8 -*-
{
    'name': "E-Box",

    'summary': """
        Personalizaciones E-Box""",

    'description': """
        Personalizaciones E-Box
    """,

    'author': "Voodoo Enterprise Software S.L.",
    'website': "https://www.voodoo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'hr',
        'hr_contract',
        'fleet',
    ],

    # always loaded
    'data': [
        'views/hr_contract.xml',
        'views/hr_contract_history.xml',
        'views/hr_employee.xml',
        'views/fleet_vehicle.xml',
    ],
}
