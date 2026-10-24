from flask import Blueprint, jsonify, request

from lemmy_client import fetch_communities
from lemmy_posts import fetch_posts
from transform import build_response
from transform_posts import build_post_response

bp = Blueprint("main", __name__)


@bp.route("/subreddits/popular", methods=["GET"])
@bp.route("/subreddits/popular.json", methods=["GET"])
def popular_subreddits():
    limit = request.args.get("limit", default=25, type=int)
    if limit is None or limit < 1:
        limit = 25
    if limit > 100:
        limit = 100
    try:
        communities = fetch_communities(limit)
        payload = build_response(limit, communities)
        return jsonify(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


def _frontpage():
    limit = request.args.get("limit", default=25, type=int)
    if limit is None or limit < 1:
        limit = 25
    if limit > 100:
        limit = 100
    try:
        posts = fetch_posts(limit)
        payload = build_post_response(limit, posts)
        return jsonify(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@bp.route("/", methods=["GET"])
@bp.route("/.json", methods=["GET"])
@bp.route("/hot", methods=["GET"])
@bp.route("/hot.json", methods=["GET"])
@bp.route("/r/all", methods=["GET"])
@bp.route("/r/all.json", methods=["GET"])
@bp.route("/r/popular", methods=["GET"])
@bp.route("/r/popular.json", methods=["GET"])
def frontpage():
    return _frontpage()
