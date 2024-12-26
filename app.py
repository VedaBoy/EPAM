from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL connection
db = mysql.connector.connect(
    host="vedardhagudapati.ddns.net",
    user="devout",
    password="123456789",
    database="registration"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll = request.form['roll']
    email = request.form['email']
    address = request.form['address']
    phone = request.form['phone']

    roll_pattern = re.compile(r'^2210030[0-5][0-9]{2}$')
    phone_pattern = re.compile(r'^[0-9]{10}$')
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    if not roll_pattern.match(roll):
        flash('Roll number must be between 2210030001 and 2210030600.')
        return redirect('/')
    if len(phone) != 10 or not phone_pattern.match(phone):
        flash('Phone number must be a 10-digit number.')
        return redirect('/')
    if not email_pattern.match(email):
        flash('Please enter a valid email address.')
        return redirect('/')

    cursor = db.cursor()
    cursor.execute("INSERT INTO registrations (name, roll, email, address, phone) VALUES (%s, %s, %s, %s, %s)",
                   (name, roll, email, address, phone))
    db.commit()
    cursor.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
