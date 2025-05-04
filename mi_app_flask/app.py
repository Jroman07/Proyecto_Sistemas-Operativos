from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secreto"

# Cada cliente tendrá: nombre, y una lista de pedidos [{hamburguesa, bebida}, ...]
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

    # Buscar si ya está en la fila
    for c in fila:
        if c["cliente"] == cliente:
            c["pedidos"].append({"hamburguesa": hamburguesa, "bebida": bebida})
            flash(f"Añadido nuevo pedido para '{cliente}': hamburguesa '{hamburguesa}', bebida '{bebida}'.")
            return redirect(url_for("index"))

    # Si la fila está llena, atender al primero
    if len(fila) >= MAX_CLIENTES:
        atendido = fila.pop(0)
        flash(f"La fila estaba llena. Se atendió automáticamente a '{atendido['cliente']}'.")

    # Nuevo cliente
    fila.append({
        "cliente": cliente,
        "pedidos": [{"hamburguesa": hamburguesa, "bebida": bebida}]
    })
    flash(f"'{cliente}' fue agregado con su primer pedido: hamburguesa '{hamburguesa}', bebida '{bebida}'.")
    return redirect(url_for("index"))

@app.route("/servir")
def servir():
    if fila:
        atendido = fila.pop(0)
        flash(f"Se atendió a '{atendido['cliente']}' con {len(atendido['pedidos'])} pedido(s).")
    else:
        flash("No hay clientes para atender.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
