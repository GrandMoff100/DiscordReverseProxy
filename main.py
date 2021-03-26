import flask
import requests

app = flask.Flask(__name__)

site = "https://discord.com/"
methods = ['GET', 'POST', 'PUT', 'DELETE']
excludes = [
    "content-encoding", "content-length", "transfer-encoding", "connection"
]


@app.route("/")
def index():
	return flask.render_template("index.html")


@app.route("/<path:path>", methods=methods)
def reverse_proxy(path: str):
	global site, methods

	if flask.request.method == methods[0]:
		head = []
		c = dict(flask.request.cookies)
		r = requests.post(f"{site}{path}",
		                  json=flask.request.get_json(),
		                  cookies=c)

		for name, value in r.raw.headers.items():
			if name.lower() not in excludes:
				head.append((name, value))
			else:
				continue

		res = flask.Response(r.content, r.status_code, head)

		return res
	elif flask.request.method == methods[1]:
		head = []
		c = dict(flask.request.cookies)
		r = requests.post(f"{site}{path}",
		                  json=flask.request.get_json(),
		                  cookies=c)

		for name, value in r.raw.headers.items():
			if name.lower() not in excludes:
				head.append((name, value))
			else:
				continue

		res = flask.Response(r.content, r.status_code, head)

		return res
	elif flask.request.method == methods[2]:
		head = []
		c = dict(flask.request.cookies)
		r = requests.put(f"{site}{path}",
		                 json=flask.request.get_json(),
		                 cookies=c)

		for name, value in r.raw.headers.items():
			if name.lower() not in excludes:
				head.append((name, value))
			else:
				continue

		res = flask.Response(r.content, r.status_code, head)

		return res
	elif flask.request.method == methods[3]:
		head = []
		c = flask.request.cookies

		r = requests.delete(f"{site}{path}",
		                    json=flask.request.get_json(),
		                    cookies=c).content

		res = flask.Response(r.content, r.status_code, head)

		return res
	else:
		return f"Unable to handle given method: '{flask.request.method}'"


app.run(
    host="0.0.0.0",
    port=8080,
    debug=False,
    threaded=True,
    ssl_context=("ssl/cert.pem", "ssl/key.pem")
)

# Serves a reverse proxy to unblock Discord!
# Note: SSL Context are unsupported by repl.it
