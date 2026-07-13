import json
import math

from odoo import http
from odoo.http import request


def invalid_response(error, status):
    return request.make_json_response({'error': error}, status=status)


def valid_response(data, pagintion_info=None, status=200):
    response_body = {'message': 'success', 'data': data}
    if pagintion_info:
        response_body['pagintion_info'] = pagintion_info
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    @http.route('/v1/property', methods=['POST'], type='http', auth='none', csrf=False)
    def post_property(self):
        try:
            vals = json.loads(request.httprequest.data.decode() or '{}')
        except json.JSONDecodeError:
            return invalid_response('Invalid JSON payload', 400)

        if not vals.get('name'):
            return invalid_response('Name is required', 400)

        try:
            property_record = request.env['property'].sudo().create(vals)
            return request.make_json_response({
                'message': 'Property has been created successfully',
                'id': property_record.id,
                'name': property_record.name,
            }, status=201)
        except Exception as error:
            return invalid_response(str(error), 400)

    @http.route('/v1/property/<int:property_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return invalid_response('ID not found', 400)

            vals = json.loads(request.httprequest.data.decode() or '{}')
            property_record.write(vals)
            return request.make_json_response({
                'message': 'Property has been updated successfully',
                'id': property_record.id,
                'name': property_record.name,
            }, status=200)
        except Exception as error:
            return invalid_response(str(error), 400)

    @http.route('/v1/property/<int:property_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return invalid_response('ID not found', 400)
            return request.make_json_response({
                'id': property_record.id,
                'name': property_record.name,
                'ref': property_record.ref,
                'bedrooms': property_record.bedrooms,
            }, status=200)
        except Exception as error:
            return invalid_response(str(error), 400)

    @http.route('/v1/property/<int:property_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return invalid_response('ID not found', 400)
            property_record.unlink()
            return request.make_json_response({'message': 'Property has been deleted successfully'}, status=200)
        except Exception as error:
            return invalid_response(str(error), 400)

    @http.route('/v1/properties', methods=['GET'], type='http', auth='none', csrf=False)
    def get_property_list(self):
        try:
            params = request.params or {}
            property_domain = []
            limit = int(params.get('limit', 5) or 5)
            page = int(params.get('page', 1) or 1)
            offset = (page - 1) * limit if page > 0 else 0

            if params.get('state'):
                property_domain.append(('state', '=', params.get('state')))

            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)
            if not property_ids:
                return invalid_response('No properties found', 400)

            return valid_response([{
                'id': property_id.id,
                'name': property_id.name,
                'ref': property_id.ref,
                'bedrooms': property_id.bedrooms,
            } for property_id in property_ids], pagintion_info={
                'page': page,
                'limit': limit,
                'count': property_count,
                'pages': math.ceil(property_count / limit) if limit else 1,
            }, status=200)
        except Exception as error:
            return invalid_response(str(error), 400)
