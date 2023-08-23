# -*- coding:utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    contratante_empleado_id = fields.Many2one('res.partner', string = "Contratante", related="employee_id.contratante_empleado_id", store=True)
    asalariado_de_empleado_id = fields.Many2one('res.partner', string = "Asalariado de (ok)", related="employee_id.asalariado_de_id", store=True)
    numero_semana_amazon = fields.Integer(string='Número de Semana Amazon', compute='_compute_numero_semana_amazon', store=True)

    @api.depends('check_in')
    def _compute_numero_semana_amazon(self):
        for record in self:
            fecha = record.check_in
            # Obtener el día de la semana (0 = lunes, 6 = domingo)
            dia_semana = fecha.weekday()
            # Ajustar el día de la semana para que 0 sea domingo en lugar de lunes
            dia_semana = (dia_semana + 1) % 7
            # Obtener la fecha del primer domingo del año
            primer_dia_anio = datetime(fecha.year, 1, 1)
            primer_domingo = primer_dia_anio + timedelta(days=(6 - primer_dia_anio.weekday()) % 7)
            # Si la fecha es anterior al primer domingo del año, se toma en cuenta el año anterior
            if fecha < primer_domingo:
                primer_dia_anio = datetime(fecha.year - 1, 1, 1)
                primer_domingo = primer_dia_anio + timedelta(days=(6 - primer_dia_anio.weekday()) % 7)
            # Calcular el número de semanas completas
            numero_semana = (fecha - primer_domingo).days // 7 + 1
            record.numero_semana_amazon = numero_semana
