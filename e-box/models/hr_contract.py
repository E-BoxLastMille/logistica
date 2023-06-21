# -*- coding:utf-8 -*-

from odoo import fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contratante_id = fields.Many2one('res.partner', string = "Contratante")