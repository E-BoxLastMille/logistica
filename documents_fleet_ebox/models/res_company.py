# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company.id)]

    documents_fleet_settings = fields.Boolean()
    documents_fleet_folder = fields.Many2one('documents.folder', string="Fleet Workspace", domain=_domain_company,
                                          default=lambda self: self.env.ref('documents_fleet.documents_fleet_folder',
                                                                            raise_if_not_found=False))
