from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    mensaje = "¡Hola desde Flask con plantilla!"
    return render_template("index.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
