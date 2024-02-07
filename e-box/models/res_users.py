# -*- coding:utf-8 -*-

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    department_ids = fields.Many2many('hr.department', string = "Departamentos")

    