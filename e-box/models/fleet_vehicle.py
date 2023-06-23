# -*- coding:utf-8 -*-

from odoo import models, fields

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    department_id = fields.Many2one('hr.department', string='Departamento')