# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_fleet_settings = fields.Boolean(
        related='company_id.documents_fleet_settings', readonly=False, string="Fleet Resources")
    documents_fleet_folder = fields.Many2one(
        'documents.folder', related='company_id.documents_fleet_folder', readonly=False, string="fleet default workspace")

    @api.onchange('documents_fleet_folder')
    def _onchange_documents_fleet_folder(self):
        # Implemented in other documents-hr bridge modules
        pass
