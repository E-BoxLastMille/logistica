# -*- coding:utf-8 -*-

from odoo import api, fields, models

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    contratante_empleado_id = fields.Many2one('res.partner', string = "Contratante", related="employee_id.contratante_empleado_id", store=True)

    numero_semana_amazon = fields.Integer(string='Número de Semana Amazon', compute='_compute_numero_semana_amazon', store=True)

    @api.depends('check_in')
    def _compute_numero_semana_amazon(self):
        for record in self:
            if record.check_in:
                # Convertir el campo datetime a date
                check_in_date = record.check_in.date()
                # Usando strftime() con %U para considerar el domingo como el primer día
                record.numero_semana_amazon = int(check_in_date.strftime('%U')) + 1