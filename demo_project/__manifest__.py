# -*- coding: utf-8 -*-
{
    'name': 'Demo Project',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Demo Project management module',
    'description': """
Module for managing demo project
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/demo_project_security.xml',
        'views/demo_project_views.xml',
        'views/demo_project_menu.xml',
    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': false,
    'license': 'LGPL-3',
}