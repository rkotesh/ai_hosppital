from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)
app = Flask(__name__, static_folder='static')

# --- Configure Gemini ---
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-2.0-pro")
chat = model.start_chat()

# --- Connect to MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_ai"]
feedbacks = db["feedback"]
appointments = db["appointments"]

# --- Routes ---
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot_page():
    return render_template("chatbot.html")

@app.route('/appointments')
def appointment_page():
    return render_template("appointments.html")

@app.route('/feedback')
def feedback_page():
    return render_template("feedback.html")

@app.route('/search')
def search_page():
    return render_template("search.html")

# --- Gemini Chat API ---
@app.route('/ask', methods=['POST'])
def ask_bot():
    user_input = request.json.get("message", "")
    response = chat.send_message(user_input)
    return jsonify({"reply": response.text})

# --- Appointment Booking API ---
@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.json
    data["date"] = datetime.now()
    appointments.insert_one(data)
    return jsonify({"status": "success", "message": "Appointment booked successfully."})

# --- Feedback API ---
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    data["timestamp"] = datetime.now()
    feedbacks.insert_one(data)
    return jsonify({"status": "success", "message": "Thanks for your feedback!"})

# --- Search Hospital by Specialty ---
@app.route('/search_hospital', methods=['POST'])
def search_hospital():
    specialty = request.json.get("specialty", "").lower()
    # Dummy data or connect real DB
    hospitals = [
        {"name": "City Care Hospital", "specialty": "cardiology", "location": "Guntur"},
        {"name": "Green Life Hospital", "specialty": "neurology"},
        {"name": "Sunrise Clinic", "specialty": "orthopedics"},
    ]
    results = [h for h in hospitals if h["specialty"] == specialty]
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up the API key and configure Gemini model
API_KEY = 'AIzaSyD1R-JbEJ-f_zsaE43mTFO2KXIFuCoLOJs'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the chat page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Send the user input to Gemini for a response
        chat = model.start_chat()
        response = chat.send_message(user_input)
        return jsonify({'response': response.text})
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        # Here, you would handle form data and save to the database (e.g., date, time, doctor).
        patient_name = request.form['name']
        appointment_date = request.form['appointment_date']
        doctor = request.form['doctor']
        # Example: Save data to a database (e.g., SQLite, MongoDB)
        return render_template('appointments.html', message="Appointment successfully booked!")
    return render_template('appointments.html')
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        # Save the feedback to a database (or print it for now)
        print("User Feedback:", feedback_text)
        return render_template('feedback.html', message="Thank you for your feedback!")
    return render_template('feedback.html')




from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import google.generativeai as genai

app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/hospitalDB?retryWrites=true&w=majority")
db = client.hospitalDB
appointments_collection = db.appointments
feedback_collection = db.feedback

# Gemini Setup
API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat = model.start_chat()
        response = chat.send_message(user_input)
        return jsonify({'response': response.text})
    return render_template('chatbot.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'appointment_date': request.form['appointment_date'],
            'doctor': request.form['doctor']
        }
        appointments_collection.insert_one(data)
        return render_template('appointments.html', message="Appointment booked successfully!")
    return render_template('appointments.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_collection.insert_one({'feedback': feedback_text})
        return render_template('feedback.html', message="Thanks for your feedback!")
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat = model.start_chat()
        response = chat.send_message(user_input)
        return jsonify({'response': response.text})
    return render_template('chatbot.html')
@app.route('/admin')
def admin():
    appointments = list(appointments_collection.find())
    feedbacks = list(feedback_collection.find())
    return render_template('admin.html', appointments=appointments, feedbacks=feedbacks)

