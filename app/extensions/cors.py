from flask_cors import CORS

CORS_ORIGINS = "*"

cors = CORS(resources={r"/*": {"origins": CORS_ORIGINS}})
