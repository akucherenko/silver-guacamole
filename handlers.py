from datetime import date

from flask import abort, jsonify, request, redirect
from marshmallow import ValidationError

from app import app, APP_HOST
from services import Shortener, Resolver, LinkStatistics
from shemas import NewLinkRequestSchema


@app.route("/")
def start():
    return jsonify({"message": "It works!"})


@app.route("/<string:short_code>", methods=["GET"])
def redirect_link(short_code):
    resolver = Resolver()
    stats = LinkStatistics()

    link = resolver.retrieve_link(short_code)

    if not link:
        abort(404)

    stats.increment(link, date.today())

    return redirect(link.original_url)


@app.route("/api/short/", methods=["POST"])
def short_link():
    payload = request.json

    if request.content_type != "application/json":
        abort(406)
    if not payload:
        abort(400)

    schema = NewLinkRequestSchema(context={
        "app_host": APP_HOST
    })

    try:
        link_req = schema.load(payload)
    except ValidationError as err:
        return jsonify({
            "errors": err.messages
        }), 400

    gen = Shortener()

    try:
        code = gen.save_url(link_req["url"])
    except RuntimeError:
        abort(500)

    return jsonify({"result": {
        "short_code": code,
        "full_link": "http://{}/{}".format(APP_HOST, code)
    }}), 201
