from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secreto"  # Necesario para mostrar mensajes flash

# Cada elemento de la fila será un diccionario con cliente, hamburguesa y bebida
fila = []

MAX_CLIENTES = 4

@app.route("/")
def index():
    return render_template("index.html", fila=fila)

@app.route("/agregar", methods=["POST"])
def agregar():
    cliente = request.form["cliente"].strip()
    hamburguesa = request.form["hamburguesa"].strip()
    bebida = request.form["bebida"].strip()

    if not cliente or not hamburguesa or not bebida:
        flash("Debes completar todos los campos del formulario.")
        return redirect(url_for("index"))

    # Verificar si el cliente ya está en la fila
    if any(c["cliente"] == cliente for c in fila):
        flash(f"'{cliente}' ya está en la fila.")
        return redirect(url_for("index"))

    # Si la fila está llena, se atiende al primero
    if len(fila) >= MAX_CLIENTES:
        atendido = fila.pop(0)
        flash(f"La fila estaba llena. Se atendió automáticamente a '{atendido['cliente']}' con su hamburguesa '{atendido['hamburguesa']}' y bebida '{atendido['bebida']}'.")

    fila.append({
        "cliente": cliente,
        "hamburguesa": hamburguesa,
        "bebida": bebida
    })

    flash(f"'{cliente}' fue agregado con hamburguesa '{hamburguesa}' y bebida '{bebida}'.")
    return redirect(url_for("index"))

@app.route("/servir")
def servir():
    if fila:
        atendido = fila.pop(0)
        flash(f"Se atendió a '{atendido['cliente']}' con hamburguesa '{atendido['hamburguesa']}' y bebida '{atendido['bebida']}'.")
    else:
        flash("No hay clientes para atender.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
