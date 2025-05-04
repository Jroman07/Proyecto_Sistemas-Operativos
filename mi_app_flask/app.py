from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secreto"  # Necesario para mostrar mensajes flash
fila = []  # Cola FIFO

MAX_CLIENTES = 4

@app.route("/")
def index():
    return render_template("index.html", fila=fila)

@app.route("/agregar", methods=["POST"])
def agregar():
    cliente = request.form["cliente"].strip()

    if cliente == "":
        flash("El nombre no puede estar vacío.")
        return redirect(url_for("index"))

    # Si el cliente ya está en la fila, no se agrega
    if cliente in fila:
        flash(f"'{cliente}' ya está en la fila.")
        return redirect(url_for("index"))

    # Si la fila está llena, se atiende (elimina) al primero
    if len(fila) >= MAX_CLIENTES:
        atendido = fila.pop(0)
        flash(f"La fila estaba llena. Se atendió automáticamente a '{atendido}'.")

    fila.append(cliente)
    flash(f"'{cliente}' fue agregado a la fila.")
    return redirect(url_for("index"))

@app.route("/servir")
def servir():
    if fila:
        atendido = fila.pop(0)
        flash(f"Se atendió a '{atendido}'.")
    else:
        flash("No hay clientes para atender.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
