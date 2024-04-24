from flask import Blueprint
from .core import core_bp

pages_bp = Blueprint("pages", __name__, url_prefix="/")

pages_bp.register_blueprint(core_bp)
