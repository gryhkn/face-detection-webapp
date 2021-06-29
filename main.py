from flask import Flask
from app import views

app = Flask(__name__)

# urls
app.add_url_rule('/', 'app', views.memorize, methods=['GET', 'POST'])
app.add_url_rule('/faceapp', 'predicted', views.recognize, methods=['GET', 'POST'])


if __name__ == "__main__":
    app.run(debug=True)
