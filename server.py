from flask import Flask, request, abort
import redis


application = Flask(__name__)
application.config['PREFIX'] = 'terraform'
application.config['REDIS_HOST'] = 'localhost'
application.config['REDIS_PORT'] = 6379
application.config.from_envvar('BACKEND_SETTINGS', silent=True)


r = redis.Redis(
    host=application.config['REDIS_HOST'],
    port=application.config['REDIS_PORT'],
    db=0
)


@application.route("/")
def hello():
    return "Hello World!"


@application.route('/<path:path>', methods=['GET'])
def get(path):
    key = "%s/state/%s" % (application.config['PREFIX'], path)
    return r.get(key) or ""


@application.route('/<path:path>', methods=['POST'])
def post(path):
    key = "%s/state/%s" % (application.config['PREFIX'], path)
    r.set(key, request.get_data())
    return ""


@application.route('/<path:path>', methods=['DELETE'])
def delete(path):
    key = "%s/state/%s" % (application.config['PREFIX'], path)
    r.delete(key)
    return ""


@application.route('/<path:path>', methods=['LOCK'])
def lock(path):
    key = "%s/lock/%s" % (application.config['PREFIX'], path)
    if r.setnx(key, request.get_data()):
        return ""
    else:
        abort(409)


@application.route('/<path:path>', methods=['UNLOCK'])
def unlock(path):
    key = "%s/lock/%s" % (application.config['PREFIX'], path)
    r.delete(key)
    return ""


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080)
