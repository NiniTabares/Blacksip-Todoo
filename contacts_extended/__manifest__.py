# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Contacts Extended',
    'version': '18.0.0.1',
    'summary': """Adición de campos avanzados en el maestro de contactos""",
    'description': 'Este módulo te ayuda a agregar más información en los registros de los contactos.',
    'category': 'Generic Modules/Contacts',
    'author': 'End to End Technology',
    'website': "https://www.endtoendt.com/",
    'sequence': 160,
    'summary': 'Centralize your address book',
    'description': """
This module gives you a quick view of your contacts directory, accessible from your home page.
You can track your vendors, customers and other contacts.
""",
    'depends': ['base', 'contacts', 'mail', 'account'],
    'data': [
        'views/contact_views.xml',
        'views/res_bank_view.xml',
        'views/res_partner_bank_view.xml',
        'views/res_partner_view.xml',


    ],
    'application': True,
    'license': 'LGPL-3',
}
