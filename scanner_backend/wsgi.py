from werkzeug.middleware.proxy_fix import ProxyFix

from scanner_backend.app import create_app
from scanner_backend.settings import Config


app = create_app(config=Config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


if __name__ == "__main__":
    app.run()
