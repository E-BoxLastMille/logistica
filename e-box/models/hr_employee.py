# -*- coding:utf-8 -*-

from odoo import fields, models, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contratante_empleado_id = fields.Many2one('res.partner', string = "Contratante", related="contract_id.contratante_id", store=True)
    asalariado_de_id = fields.Many2one('res.partner', string = "Asalariado de")

    def action_open_last_month_attendances(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Asistencias totales"),
            "res_model": "hr.attendance",
            "views": [
                [self.env.ref('hr_attendance.view_attendance_tree').id, "tree"],
                [self.env.ref('e-box.view_attendance_pivot_ebox').id, "pivot"],
                [self.env.ref('e-box.view_attendance_calendar_ebox').id, "calendar"],
            ],
            "context": {
                "create": 0
            },
            "domain": [('employee_id', '=', self.id)]
        }
    