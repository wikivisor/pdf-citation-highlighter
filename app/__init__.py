from flask import Flask

def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
    )

    app.app_context().push()

    from app.config.prod import ProdConfig

    app.config.from_object(ProdConfig)

    from app.extensions import cors
    
    cors.init_app(app)
    
    from app.routes import pages_bp

    app.register_blueprint(pages_bp)

    return app
