from flask.ext import restful
from keyhub.wsgi import app
from keyhub.rest import models


api = restful.Api(app)
print hash(app)


class SSHKey(restful.Resource):
    def get(self, username, key_id):
        key = models.SSHKey.get_by_username(username, key_id)


api.add_resource(SSHKey, '/users/<string:username>/keys/<string:key_id>')
