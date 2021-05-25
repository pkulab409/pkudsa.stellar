from flask import Flask
import webbrowser

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='', static_folder='public')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    app.run(port=8080, debug=False)
