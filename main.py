from app import flask_app
import flask
import flask_wtf
import passlib

if __name__ == '__main__':
    flask_app.debug = True
    flask_app.run(host='0.0.0.0', port=5000)
