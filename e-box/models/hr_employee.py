# -*- coding:utf-8 -*-

from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contratante_id = fields.Many2one('res.partner', string = "Contratante", related="contract_id.contratante_id", store=True)
    