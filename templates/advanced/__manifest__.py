# -*- coding: utf-8 -*-
{
    'name': '{{MODULE_NAME}}',
    'version': '18.0.1.0.0',
    'category': '{{CATEGORY}}',
    'summary': '{{SUMMARY}}',
    'description': """
Advanced Module Template
=======================
This is a comprehensive template for Odoo 18 Community Edition modules with advanced features.

Key Features:
------------
* Complete module structure
* Includes report directory
* Includes wizard directory
* Demo data templates
* Multi-model support
* Best practices built-in
    """,
    'author': '{{AUTHOR}}',
    'website': '{{WEBSITE}}',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}