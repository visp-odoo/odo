# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Padhiyar Vishal',
#     'summary': '',
    'description': "Real Estate",
#     'website': 'https://www.odoo.com/page/estate',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate.menus.xml',
        'views/estate.property.views.xml',
        'wizards/make_offer_wizard_views.xml',
        'security/security.xml',
        'views/real_estate_template.xml',

    ],
}
