# -*- coding:utf-8 -*-

from odoo import api, models, fields

class ServiceDetailsReport(models.Model):
    _name = 'e_box.service_details_report'

    fecha = fields.Date(string='Fecha')
    empleado_id = fields.Many2one('hr.employee', string='Empleado')
    departamento_id = fields.Many2one('hr.department', string = 'Departamento (Estación)', related='empleado_id.department_id', store=True)
    amazon_duracion_planificada_id = fields.Many2one('e_box.amazon_duracion_planificada', string='Duración planificada')
    inicio_sesion = fields.Datetime(string='Inicio de sesión')
    cierre_sesion = fields.Datetime(string='Fin de sesión')
    amazon_identificacion = fields.Char(string = "Amazon Identificación", related='empleado_id.amazon_identificacion', store=True)
    contratante_empleado_amazon_id = fields.Many2one('res.partner', string = "Contratante", related="empleado_id.contratante_empleado_id", store=True)
    amazon_ruta_id = fields.Many2one('e_box.amazon_rutas', string='Ruta')
    amazon_tipo_servicio_id = fields.Many2one('e_box.amazon_tipo_servicio', string='Tipo servicio')
    puesto_id = fields.Many2one('hr.job', string = 'Puesto', related='empleado_id.job_id', store=True)
    amazon_delivery_id = fields.Many2one('e_box.amazon_delivery', string='Delivery')
    asalariado_de_id = fields.Many2one('res.partner', string = 'Asalariado de', related='empleado_id.asalariado_de_id', store=True)
    distancia_total_planificada = fields.Integer(string='Distancia total planificada')
    distancia_total_permitida = fields.Integer(string='Distancia total permitida')
    amazon_unidad_distancia_id = fields.Many2one('e_box.amazon_unidad_distancia', string='Unidad distancia')
    paquetes_total = fields.Integer(string='Paq. Total')
    paquetes_entregado = fields.Integer(string='Paq. Entregados')
    paquetes_devuelto = fields.Integer(string='Paq. Devueltos')
    amazon_nombre_mensajero = fields.Char(string = "Nombre mensajero", related='empleado_id.amazon_nombre_mensajero', store=True)
    old_id = fields.Integer(string='Old id.')
    numero_semana_amazon = fields.Integer(string='Número de Semana Amazon', compute='_compute_numero_semana_amazon', store=True)

    @api.depends('fecha')
    def _compute_numero_semana_amazon(self):
        for record in self:
            if record.fecha:
                # Usando strftime() con %U para considerar el domingo como el primer día
                week_number = int(record.fecha.strftime('%U'))
                # Si es domingo y el número de semana es 0, entonces es la semana 1
                if record.fecha.weekday() == 6 and week_number == 0:
                    record.numero_semana_amazon = 1
                else:
                    record.numero_semana_amazon = week_number + 1

class AmazonDuracionPlanificada(models.Model):
    _name = 'e_box.amazon_duracion_planificada'

    name = fields.Char(string='Nombre')
    precio = fields.Float(string='Precio')

class AmazonReasonCodes(models.Model):
    _name = 'e_box.amazon_reason_codes'

    name = fields.Char(string='Reason code')
    amazon_estado = fields.Selection([
        ('not_attrited', 'Not attrited'),
        ('non_regretted', 'Non regretted'),
        ('regretted', 'Regretted')
    ], string = "Amazon estado", required=True, default='not_attrited')
    nota = fields.Text(string='Nota')

class AmazonRutas(models.Model):
    _name = 'e_box.amazon_rutas'

    name = fields.Char(string='Ruta')
    departamento_id = fields.Many2one('hr.department', string = 'Departamento (Estación)')

class AmazonTipoServicio(models.Model):
    _name = 'e_box.amazon_tipo_servicio'

    name = fields.Char(string='Tipo servicio')

class AmazonDelivery(models.Model):
    _name = 'e_box.amazon_delivery'

    name = fields.Char(string='Delivery')

class AmazonUnidadDistancia(models.Model):
    _name = 'e_box.amazon_unidad_distancia'

    name = fields.Char(string='Unidad distancia')

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
    