from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    html = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Bem-vindo ao Despesas</h1>
	<footer>
		<p>Copyright 2015 - Régis da Silva</p>
		<p>Feito com <a href="http://flask.pocoo.org/">Flask</a></p>
	</footer>
</body>
</html>\
"""

    return html

if __name__ == "__main__":
    app.run()
