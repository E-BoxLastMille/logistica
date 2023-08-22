# -*- coding:utf-8 -*-
import base64
import csv
from io import StringIO
from datetime import datetime

from odoo import models, fields
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

def parse_date(date_str):
    """Intenta analizar una fecha con múltiples formatos"""
    formats = ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"La cadena {date_str} no coincide con ningún formato conocido.")

class AmazonImportEBLM(models.Model):
    _name = 'e_box.amazon_import_eblm'

    csv_file = fields.Binary(string='File (csv)', required=True)
    filename = fields.Char(string='Filename')

    def button_import(self):
        self.ensure_one()
        csv_file = base64.b64decode(self.csv_file)
        file_input = StringIO(csv_file.decode('utf-8-sig'))
        file_input.seek(0)
        reader = csv.DictReader(file_input, delimiter=',')
        missing_mensajeros = set()
        for row in reader:
            empleado_id = self.env['hr.employee'].with_context(active_test=False).search([
                '|',
                ('name','ilike', row['Mensajero']),
                ('amazon_nombre_mensajero','ilike', row['Mensajero'])
            ], limit=1, order='id desc')
            if row['Inicio de sesión'] == '' or row['Cierre de sesión'] == '':
                continue
            if not empleado_id:
                if row['Mensajero']:
                    missing_mensajeros.add(row['Mensajero'])
                continue
            amazon_delivery_id = self.env['e_box.amazon_delivery'].search([('name','=', row['Estación'])])
            if not amazon_delivery_id:
                amazon_delivery_id = self.env['e_box.amazon_delivery'].create({
                    'name' : row['Estación']
                })
            amazon_duracion_planificada_id = self.env['e_box.amazon_duracion_planificada'].search([('name','=', row['Duración planificada'])])
            if not amazon_duracion_planificada_id:
                amazon_duracion_planificada_id = self.env['e_box.amazon_duracion_planificada'].create({
                    'name' : row['Duración planificada']
                })
            amazon_ruta_id = self.env['e_box.amazon_rutas'].search([('name','=', row['Ruta'])])
            if not amazon_ruta_id:
                amazon_ruta_id = self.env['e_box.amazon_rutas'].create({
                    'name' : row['Ruta']
                })
            amazon_tipo_servicio_id = self.env['e_box.amazon_tipo_servicio'].search([('name','=', row['Tipo de servicio'])])
            if not amazon_tipo_servicio_id:
                amazon_tipo_servicio_id = self.env['e_box.amazon_tipo_servicio'].create({
                    'name' : row['Tipo de servicio']
                })
            amazon_unidad_distancia_id = self.env['e_box.amazon_unidad_distancia'].search([('name','=', row['Unidad de distancia'])])
            if not amazon_unidad_distancia_id:
                amazon_unidad_distancia_id = self.env['e_box.amazon_unidad_distancia'].create({
                    'name' : row['Unidad de distancia']
                })
            inicio_sesion = parse_date(row['Inicio de sesión'])
            cierre_sesion = parse_date(row['Cierre de sesión'])
            #Evitamos duplicados
            service_details_report_id = self.env['e_box.service_details_report'].search([
                ('fecha', '=', row['Fecha']),
                ('empleado_id', '=', empleado_id.id),
                ('amazon_delivery_id', '=', amazon_delivery_id.id),
                ('amazon_duracion_planificada_id', '=', amazon_duracion_planificada_id.id),
                ('inicio_sesion', '=', inicio_sesion),
                ('cierre_sesion', '=', cierre_sesion),
                ('amazon_ruta_id', '=', amazon_ruta_id.id),
                ('amazon_tipo_servicio_id', '=', amazon_tipo_servicio_id.id)
            ])
            if not service_details_report_id:
                self.env['e_box.service_details_report'].create({
                    'fecha': row['Fecha'],
                    'empleado_id': empleado_id.id,
                    'amazon_delivery_id' : amazon_delivery_id.id,
                    'amazon_duracion_planificada_id': amazon_duracion_planificada_id.id,
                    'inicio_sesion': inicio_sesion,
                    'cierre_sesion': cierre_sesion,
                    'amazon_ruta_id': amazon_ruta_id.id,
                    'amazon_tipo_servicio_id': amazon_tipo_servicio_id.id,
                    'distancia_total_planificada': row['Distancia total planificada'],
                    'distancia_total_permitida': row['Distancia total permitida'],
                    'amazon_unidad_distancia_id': amazon_unidad_distancia_id.id,
                    'paquetes_total': int(row['Envíos entregados']) + int(row['Envíos devueltos']),
                    'paquetes_entregado': row['Envíos entregados'],
                    'paquetes_devuelto': row['Envíos devueltos'],    
                })
        if missing_mensajeros:
            raise UserError('Los registros de los siguientes mensajeros no han podido ser importados porque no existen en Odoo:\n\n%s' % '\n'.join(missing_mensajeros))
        return {'type': 'ir.actions.client', 'tag': 'reload'}