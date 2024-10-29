from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="Prem@123", # Replace with your MySQL password
        database="equipment_rentals"
    )
    return conn

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index2.html')

# Route to get all equipment records
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM equipment')
    equipment_records = cursor.fetchall()
    conn.close()
    return jsonify(equipment_records)

# Route to add a new equipment record
@app.route('/api/equipment', methods=['POST'])
def add_equipment():
    new_equipment = request.json
    name = new_equipment['name']
    type = new_equipment['type']
    quantity = new_equipment['quantity']
    price_per_day = new_equipment['price_per_day']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO equipment (name, type, quantity, price_per_day) VALUES (%s, %s, %s, %s)',
                   (name, type, quantity, price_per_day))
    conn.commit()
    conn.close()
    return jsonify(new_equipment), 201

# Route to delete an equipment record
@app.route('/api/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipment WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
