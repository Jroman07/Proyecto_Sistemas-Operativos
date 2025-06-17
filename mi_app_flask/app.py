from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secreto"

fila = []
historial_reemplazos = []
fallos = 0
MAX_CLIENTES = 4  # valor por defecto

@app.route("/")
def index():
    return render_template(
        "index.html",
        fila=fila,
        historial=historial_reemplazos,
        fallos=fallos,
        max_clientes=MAX_CLIENTES
    )

@app.route("/configurar_max", methods=["POST"])
def configurar_max():
    global MAX_CLIENTES
    try:
        nuevo_max = int(request.form["max_clientes"])
        if 4 <= nuevo_max <= 10:
            MAX_CLIENTES = nuevo_max
            flash(f"🔧 Máximo de clientes actualizado a {MAX_CLIENTES}.")
    except ValueError:
        flash("❌ Valor inválido para el número máximo de clientes.")
    return redirect(url_for("index"))

@app.route("/agregar", methods=["POST"])
def agregar():
    global fallos

    cliente = request.form["cliente"].strip()
    hamburguesa = request.form["hamburguesa"].strip()
    bebida = request.form["bebida"].strip()

    if not cliente or not hamburguesa or not bebida:
        flash("Debes completar todos los campos del formulario.")
        return redirect(url_for("index"))

    # Buscar si el cliente ya está en la fila (no genera fallo de página)
    for c in fila:
        if c["cliente"] == cliente:
            c["pedidos"].append({"hamburguesa": hamburguesa, "bebida": bebida})
            flash(f"✅ Pedido añadido para '{cliente}': 🍔 '{hamburguesa}', 🥤 '{bebida}'.")
            return redirect(url_for("index"))

    # Fallo de página: cliente no estaba en la fila
    fallos += 1

    if len(fila) >= MAX_CLIENTES:
        reemplazado = fila.pop(0)
        historial_reemplazos.append(reemplazado)
        flash(f"🔁 FIFO: Se reemplazó a '{reemplazado['cliente']}' para ingresar a '{cliente}'.")

    # Agregar nuevo cliente
    fila.append({
        "cliente": cliente,
        "pedidos": [{"hamburguesa": hamburguesa, "bebida": bebida}]
    })

    flash(f"⚠️ Fallo de página: se cargó '{cliente}' con 🍔 '{hamburguesa}' y 🥤 '{bebida}'.")
    return redirect(url_for("index"))

@app.route("/servir")
def servir():
    if fila:
        atendido = fila.pop(0)
        flash(f"✅ Se atendió a '{atendido['cliente']}' con {len(atendido['pedidos'])} pedido(s).")
    else:
        flash("ℹ️ No hay clientes para atender.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
