from flask import Flask
from app.classViews import flaskApp

# from app import views

app = Flask(__name__)

main_page = flaskApp()

# urls
app.add_url_rule('/', 'app', main_page.memorize, methods=['GET', 'POST'])
app.add_url_rule('/faceapp', 'predicted', main_page.recognize, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5000, host="0.0.0.0")
