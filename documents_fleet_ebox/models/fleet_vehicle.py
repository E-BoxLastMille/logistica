# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _inherit = ['fleet.vehicle', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')
    documents_share_id = fields.Many2one('documents.share', groups="fleet.fleet_group_manager")
    
    def _get_document_folder(self):
        return self.company_id.documents_fleet_folder if self.company_id.documents_fleet_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_fleet_settings and super()._check_create_documents()

    def _get_fleet_document_domain(self):
        self.ensure_one()
        return [
            ('res_id', '=', self.id),
            ('res_model', '=', self._name)
        ]

    def _compute_document_count(self):
        for r in self:
            r.document_count = self.env['documents.document'].search_count(r._get_fleet_document_domain())

    def action_open_documents(self):
        self.ensure_one()
        fleet_folder = self._get_document_folder()
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            'default_res_id': self.id,
            'default_res_model': self._name,
            'searchpanel_default_folder_id': fleet_folder and fleet_folder.id,
        }
        action['domain'] = self._get_fleet_document_domain()
        return action
