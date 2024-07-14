from flask import Flask, jsonify
from woocommerce import API
import os

app = Flask(__name__)

# Configuración de WooCommerce API
wcapi = API(
    url="https://cindyl23.sg-host.com",
    consumer_key="ck_7f3df1337b0b8a969fd0c68d841fece817b15862",
    consumer_secret="cs_f6982c08085d6f2dd6047b77531858530f758864",
    version="wc/v3"
)

@app.route('/')
def home():
    return "API de verificación de compras de WooCommerce"

@app.route('/verificar-compra/<int:user_id>/<int:product_id>')
def verificar_compra(user_id, product_id):
    try:
        # Obtener todas las órdenes del usuario
        ordenes = wcapi.get(f"orders?customer={user_id}").json()

        # Verificar si el producto está en alguna de las órdenes
        comprado = any(
            any(item['product_id'] == product_id for item in orden['line_items'])
            for orden in ordenes
        )

        return jsonify({"comprado": comprado})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error al verificar la compra"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)