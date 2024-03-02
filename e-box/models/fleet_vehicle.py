# -*- coding:utf-8 -*-

from odoo import models, fields, api

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    department_id = fields.Many2one('hr.department', string='Departamento')
    propietario_id = fields.Many2one('res.partner', string = "Propietario")
    attendance_ids = fields.One2many('hr.attendance', 'vehiculo_id')
    total_attendance = fields.Integer(compute='_compute_total_attendance', compute_sudo=True)

    @api.depends('attendance_ids')
    def _compute_total_attendance(self):
        for vehicle in self:
            vehicle.total_attendance = len(vehicle.attendance_ids)

    def action_open_attendances(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Asistencias totales Vehículo",
            "res_model": "hr.attendance",
            "views": [[self.env.ref('hr_attendance.view_attendance_tree').id, "tree"]],
            "context": {
                "create": 0
            },
            "domain": [('vehiculo_id', '=', self.id)]
        }
