# -*- coding:utf-8 -*-

from odoo import models, fields

class ServiceDetailsReport(models.Model):
    _name = 'e_box.service_details_report'

    fecha = fields.Date(string='Fecha')
    empleado_id = fields.Many2one('hr.employee', string='Empleado')
    departamento_id = fields.Many2one('hr.department', string = 'Departamento', related='empleado_id.department_id', store=True)
    amazon_duracion_planificada_id = fields.Many2one('e_box.amazon_duracion_planificada', string='Duración planificada')
    inicio_sesion = fields.Datetime(string='Inicio de sesión')
    cierre_sesion = fields.Datetime(string='Fin de sesión')
    amazon_identificacion = fields.Char(string = "Amazon Identificación", related='empleado_id.amazon_identificacion', store=True)
    distancia_total_permitida = fields.Integer(string='Distancia total permitida')


class AmazonDuracionPlanificada(models.Model):
    _name = 'e_box.amazon_duracion_planificada'

    name = fields.Date(string='Nombre')
    precio = fields.Float(string='Precio')

class AmazonReasonCodes(models.Model):
    _name = 'e_box.amazon_reason_codes'

    name = fields.Char(string='Reason code')
    estado_amazon = fields.Selection([
        ('not_attrited', 'Not attrited'),
        ('non_regretted', 'Non regretted'),
        ('regretted', 'Regretted')
    ], required=True, default='not_attrited')
    nota = fields.Text(string='Nota')

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    amazon_identificacion = fields.Char(string='Identificación Amazon')
    amazon_nombre_mensajero = fields.Char(string='Nombre mensajero')
    amazon_estado = fields.Selection([
        ('activo', 'ACTIVO'),
        ('inactivo', 'INACTIVO'),
        ('offboarded', 'OFFBOARDED')
    ], default='activo')
    amazon_reason_codes_id = fields.Many2one('e_box.amazon_reason_codes', string='Reason code')