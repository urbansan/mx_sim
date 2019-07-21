from flask import Flask


app = Flask(__name__)

from .frontend import frontend_app

app.register_blueprint(frontend_app)
app.secret_key = b'\xa9]B<\x1f9\x1en3\xd9\x90&if\xdb\x14'


if __name__ == '__main__':
    app.run(debug=True)