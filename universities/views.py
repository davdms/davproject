from db import Country
from db import db
from db import University
from flask import Blueprint, jsonify, request
from flask.views import MethodView

bp = Blueprint('university', __name__)


class UniversitiesBaseView(MethodView):
    def data_validation(self, data):
        errors = {}
        field = {
            'country_id': int,
            'name': str,
            'rank': int,
            'score': float
        }

        for name, _type in field.items():
            if name in data.keys():
                try:
                    _type(data[name])
                except (ValueError, TypeError, KeyError):
                    errors[name] = 'invalid'

        return data, errors

    def is_column_is_unique(self, col, val):
        return University.query.filter_by(**{col: val}).first()

    def get_country_by_id(self, country_id):
        return Country.query.get(country_id)

    def get_university_by_id(self, university_id):
        return University.query.filter_by(id=university_id).first()


class UniversitiesListCreateView(UniversitiesBaseView):

    def get(self):
        limit = 20
        rows = University.query

        country = request.args.get('country')
        if country:
            rows = rows.filter_by(country=country)

        rows = rows.limit(limit)

        page = request.args.get('page', '1')
        if page and page.isnumeric():
            page = int(page)
            offset = (page - 1) * limit
            rows = rows.offset(offset)

        response = [{
            'id': row.id,
            'rank': row.rank,
            'name': row.name,
            'country_id': row.country_id,
            'score': row.score
        } for row in rows]

        return jsonify(response)

    def post(self):
        data = request.json
        data, errors = self.data_validation(data)

        if len(errors):
            return jsonify(errors), 401

        if not self.get_country_by_id(data['country_id']):
            errors['country'] = 'invalid'

        if self.is_column_is_unique('name', data['name']):
            errors['name'] = 'invalid'

        if self.is_column_is_unique('rank', data['rank']):
            errors['rank'] = 'invalid'

        if len(errors):
            return jsonify(errors), 401

        u = University(**data)
        db.session.add(u)
        db.session.commit()
        db.session.refresh(u)
        return jsonify({'id': u.id}), 201


class UniversitiesDetailsUptadeDeleteView(UniversitiesBaseView):
    def get(self, u_id):
        # if there is no university return jsonify({}), 404
        uni = self.get_university_by_id(u_id)
        if uni:
            response = [{
                'id': uni.id,
                'rank': uni.rank,
                'name': uni.name,
                'country_id': uni.country_id,
                'score': uni.score
            }]
            return jsonify(response)
        else:
            return jsonify({}), 404

    def put(self, u_id):
        # if there is no university return jsonify({}), 404
        uni = self.get_university_by_id(u_id)
        if uni:
            data = request.json
            data, errors = self.data_validation(data)

            if len(errors):
                return jsonify(errors), 401

            if 'country_id' in data.keys() and not self.get_country_by_id(data['country_id']):
                errors['country'] = 'invalid'

            if 'name' in data.keys() and self.is_column_is_unique('name', data['name']):
                errors['name'] = 'invalid'

            if 'rank' in data.keys() and self.is_column_is_unique('rank', data['rank']):
                errors['rank'] = 'invalid'

            if len(errors):
                return jsonify(errors), 401

            if 'country_id' in data.keys():
                uni.country_id = data['country_id']

            if 'name' in data.keys():
                uni.name = data['name']

            if 'rank' in data.keys():
                uni.rank = data['rank']

            if 'score' in data.keys():
                uni.score = data['score']

            db.session.commit()
            return self.get(u_id)

        else:
            return jsonify({}), 404


    def delete(self, u_id):
        # if there is no university return jsonify({}), 404
        uni = self.get_university_by_id(u_id)
        if uni:
            db.session.delete(uni)
            db.session.commit()
            return jsonify({}), 201
        else:
            return jsonify({}), 404


bp.add_url_rule('/universities/', view_func=UniversitiesListCreateView.as_view('universities'))
bp.add_url_rule('/universities/<u_id>/', view_func=UniversitiesDetailsUptadeDeleteView.as_view('university'))
