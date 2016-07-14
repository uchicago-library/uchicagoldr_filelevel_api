from flask import Flask, jsonify, send_file
from flask_restful import Resource, Api, reqparse
from uuid import uuid1
from werkzeug.utils import secure_filename
from os import scandir
from os.path import join
from urllib.parse import quote, unquote

from uchicagoldrtoolsuite.bit_level.lib.structures.stage import Stage
from uchicagoldrtoolsuite.bit_level.lib.readers.filesystemstagereader import FileSystemStageReader
from uchicagoldrtoolsuite.bit_level.lib.writers.filesystemstagewriter import FileSystemStageWriter

from config import Config
from apiresponse import APIResponse


# Globals
_SECRET_KEY = Config.secret_key
_STAGING_ENV_PATH = Config.staging_env_path

def escape(s):
    return quote(s, safe='')


def unescape(s):
    return unquote(s)


def get_stages_list():
    return [x.name for x in scandir(_STAGING_ENV_PATH) if x.is_dir()]


def get_stage(id):
    p = join(_STAGING_ENV_PATH, id)
    r = FileSystemStageReader(p)
    s = r.read()
    return s


def write_stage(stage, id):
    pass


class Stages(Resource):
    def get(self):
        try:
            return jsonify(
                APIResponse("success", data={"stages":get_stages_list()}).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self):
        # Create a new stage
        pass


class Stage(Resource):
    def get(self, stage_id):
        # Return a representation of this stage
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            r = {}
            r['stage_id'] = s.identifier
            r['segments'] = [x.identifier for x in s.segment_list]
            r['accession_records'] = [x.item_name for x in s.accessionrecord_list]
            r['admin_notes'] = [x.item_name for x in s.adminnote_list]
            r['legal_notes'] = [x.item_name for x in s.legalnote_list]
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self, stage_id):
        # Add a segment
        pass

    def delete(self, stage_id):
        # Delete this stage
        pass


class Segment(Resource):
    def get(self, stage_id, segment_id):
        # Return a representation of this segment
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            r = {}
            r['stage_id'] = s.identifier
            r['segment_id'] = segment.identifier
            r['material_suites'] = [escape(x.content.item_name) for x in segment.get_materialsuite_list()]
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self, stage_id, segment_id):
        # Add a materialsuite to this segment
        pass

    def delete(self, stage_id, segment_id):
        # Delete this segment
        pass


class MaterialSuite(Resource):
    def get(self, stage_id, segment_id, ms_id):
        # Get a representation of this materialsuite
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            r = {}
            r['stage_id'] = s.identifier
            r['segment_id'] = segment.identifier
            r['materialsuite_id'] = ms_id
            has_techmds = bool(ms.technicalmetadata_list)
            has_premis = bool(ms.premis)
            has_presforms = bool(ms.presform_list)
            r['has_techmds'] = has_techmds
            r['has_premis'] = has_premis
            r['has_presforms'] = has_presforms
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self, stage_id, segment_id, ms_id):
        # Add an element of this materialsuite
        pass

    def delete(self, stage_id, segment_id, ms_id):
        # Delete this materialsuite
        pass


class Presforms(Resource):
    def get(self, stage_id, segment_id, ms_id):
        # Return a representation of all available presforms
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            r = {}
            r['stage_id'] = s.identifier
            r['segment_id'] = segment.identifier
            r['materialsuite_id'] = ms_id
            r['presforms'] = [escape(x.content.item_name) for x in ms.presform_list]
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self, stage_id, segment_id, ms_id):
        # Add a presform
        pass

    def delete(self, stage_id, segment_id, ms_id):
        #Delete all presforms
        pass


class Presform(Resource):
    def get(self, stage_id, segment_id, ms_id, presform_id):
        # Return the presform file
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            presform = [x for x in ms.presform_list if x.content.item_name == presform_id]
            if len(presform) != 1:
                raise ValueError("Bad Presform Identifier")
            presform = presform[0]
            r = {}
            r['stage_id'] = s.identifier
            r['segment_id'] = segment.identifier
            r['materialsuite_id'] = ms_id
            r['presform_id'] = presform_id
            r['techmd'] = [x.item_name for x in presform.technicalmetadata_list]
            r['premis'] = None
            if presform.premis:
                r['premis'] = presform.premis.item_name
            r['presforms'] = []
            if presform.presform_list:
                r['presforms'] = [x.item_name for x in presform.presform_list]
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())


    def delete(self, stage_id, segment_id, ms_id, presform_id):
        # Delete this presform
        pass


class PresformContent(Resource):
    def get(self, stage_id, segment_id, ms_id, presform_id):
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            presform = [x for x in ms.presform_list if x.content.item_name == presform_id]
            if len(presform) != 1:
                raise ValueError("Bad Presform Identifier")
            presform = presform[0]
            presform_content = presform.content
            return send_file(presform_content.open(), as_attachment=True, attachment_filename=presform_content.item_name)
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def delete(self, stage_id, segment_id, ms_id, presform_id):
        pass


class PresformPremis(Resource):
    def get(self, stage_id, segment_id, ms_id, presform_id):
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            presform = [x for x in ms.presform_list if x.content.item_name == presform_id]
            if len(presform) != 1:
                raise ValueError("Bad Presform Identifier")
            presform = presform[0]
            presform_premis = presform.premis
            return send_file(presform_premis.open(), as_attachment=True, attachment_filename=presform_premis.item_name)
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def delete(self, stage_id, segment_id, ms_id, presform_id):
        pass


class Techmds(Resource):
    def get(self, stage_id, segment_id, ms_id):
        # Return a list of available techmds
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            r = {}
            r['stage_id'] = s.identifier
            r['segment_id'] = segment.identifier
            r['materialsuite_id'] = ms_id
            r['tech_mds'] = [escape(x.item_name) for x in ms.technicalmetadata_list]
            return jsonify(
                APIResponse("success", data=r).dictify()
            )
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def post(self, stage_id, segment_id, ms_id):
        # Add a Techmd
        pass

    def delete(self, stage_id, segment_id, ms_id):
        # Delete all techmds
        pass


class Techmd(Resource):
    def get(self, stage_id, segment_id, ms_id, techmd_id):
        # Get a technical metadata record
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            techmd = [x for x in ms.technicalmetadata_list if escape(x.item_name) == escape(techmd_id)]
            if len(techmd) != 1:
                raise ValueError("Bad Technical Metadata Identifier")
            techmd = techmd[0]
            return send_file(techmd.open(), as_attachment=True, attachment_filename=techmd.item_name)
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def delete(self, stage_id, segment_id, ms_id, techmd_id):
        # Delete a technical metadata record
        pass


class Content(Resource):
    def get(self, stage_id, segment_id, ms_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('body', type=bool)
            args = parser.parse_args()
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            # Return this stuff as an attachment right now, because who knows
            # what were going to be returning - depending on how this works out
            # we might have to change it in the future s the LDR can serve
            # interfaces or something.
            # Maybe this should be two endpoints? Content and ContentSafe or
            # something?
            return send_file(ms.content.open(), as_attachment=True, attachment_filename=ms.content.item_name)
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())


        # Return the content file
        pass

    def delete(self, stage_id, segment_id, ms_id):
        # Delete the content file
        pass


class Premis(Resource):
    def get(self, stage_id, segment_id, ms_id):
        # get the PREMIS file
        try:
            try:
                s = get_stage(stage_id)
            except:
                raise ValueError("Bad Stage Identifier")
            segment = [x for x in s.segment_list if x.identifier == segment_id]
            if len(segment) != 1:
                raise ValueError("Bad Segment Identifier")
            segment = segment[0]
            print(ms_id)
            ms = [x for x in segment.get_materialsuite_list() if escape(x.content.item_name) == escape(ms_id)]
            if len(ms) != 1:
                raise ValueError("Bad MaterialSuite Identifier")
            ms = ms[0]
            return send_file(ms.premis.open(), as_attachment=True, attachment_filename=ms.premis.item_name)
        except Exception as e:
            return jsonify(APIResponse("fail", errors=[str(type(e)) + ": " + str(e)]).dictify())

    def delete(self, stage_id, segment_id, ms_id):
        # Delete the PREMIS file
        pass


app = Flask(__name__)

app.secret_key = _SECRET_KEY
app.config['BUNDLE_ERRORS'] = True

api = Api(app)

api.add_resource(Stages, '/stages')
api.add_resource(Stage, '/stages/<string:stage_id>')
api.add_resource(Segment, '/stages/<string:stage_id>/<string:segment_id>')
api.add_resource(MaterialSuite, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>')
api.add_resource(Presforms, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/presforms')
api.add_resource(Presform, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/presforms/<path:presform_id>')
api.add_resource(PresformContent, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/presforms/<path:presform_id>/content')
api.add_resource(PresformPremis, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/presforms/<path:presform_id>/premis')
api.add_resource(Techmds, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/techmds')
api.add_resource(Techmd, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/techmds/<path:techmd_id>')
api.add_resource(Content, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/content')
api.add_resource(Premis, '/stages/<string:stage_id>/<string:segment_id>/<path:ms_id>/premis')
