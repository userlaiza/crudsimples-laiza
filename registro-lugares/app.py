from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Lugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_visita = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    lugares = Lugar.query.all()
    return render_template("index.html", lugares=lugares)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":

        nome = request.form["nome"]
        data_visita = request.form["data_visita"]
        descricao = request.form["descricao"]

        lugar = Lugar(
            nome=nome,
            data_visita=data_visita,
            descricao=descricao
        )

        db.session.add(lugar)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    lugar = Lugar.query.get_or_404(id)

    if request.method == "POST":

        lugar.nome = request.form["nome"]
        lugar.data_visita = request.form["data_visita"]
        lugar.descricao = request.form["descricao"]

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("editar.html", lugar=lugar)


@app.route("/excluir/<int:id>")
def excluir(id):

    lugar = Lugar.query.get_or_404(id)

    db.session.delete(lugar)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)