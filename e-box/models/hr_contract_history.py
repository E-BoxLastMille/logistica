# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools

class ContractHistory(models.Model):
    _inherit = 'hr.contract.history'

    contratante_id = fields.Many2one('res.partner', string='Contratante')

