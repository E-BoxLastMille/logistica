# -*- coding:utf-8 -*-

from odoo import fields, models

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    contratante_empleado_id = fields.Many2one('res.partner', string = "Contratante", related="employee_id.contratante_empleado_id", store=True)
    