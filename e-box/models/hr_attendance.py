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
                week_number = int(check_in_date.strftime('%U'))
                # Si es domingo y el número de semana es 0, entonces es la semana 1
                if check_in_date.weekday() == 6 and week_number == 0:
                    record.numero_semana_amazon = 1
                else:
                    record.numero_semana_amazon = week_number + 1