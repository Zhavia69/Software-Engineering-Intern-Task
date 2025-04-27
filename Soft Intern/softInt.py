from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DATA_FILE = 'health_system.json'

# Predefined illnesses with descriptions
PREDEFINED_ILLNESSES = [
    {"name": "Malaria", "description": "A mosquito-borne infectious disease causing fever, fatigue, vomiting, and headaches."},
    {"name": "HIV/AIDS", "description": "A chronic, potentially life-threatening condition caused by the human immunodeficiency virus."},
    {"name": "Tuberculosis (TB)", "description": "A serious infectious disease that mainly affects the lungs."},
    {"name": "Pneumonia", "description": "Infection that inflames air sacs in one or both lungs, which may fill with fluid."},
    {"name": "Diarrheal diseases", "description": "Conditions characterized by loose, watery stools and frequent bowel movements."},
    {"name": "Malnutrition", "description": "Condition resulting from eating a diet lacking in nutrients or not absorbing nutrients properly."},
    {"name": "Typhoid fever", "description": "Bacterial infection causing high fever, abdominal pain, and headache."},
    {"name": "Hypertension (High blood pressure)", "description": "A condition in which the force of the blood against artery walls is too high."},
    {"name": "Diabetes", "description": "A metabolic disease causing high blood sugar levels over a prolonged period."},
    {"name": "Respiratory infections", "description": "Infections that interfere with normal breathing, affecting upper or lower respiratory tract."},
    {"name": "Intestinal worms", "description": "Parasitic worms that live in the human intestine and feed off the host."},
    {"name": "Schistosomiasis (Bilharzia)", "description": "A disease caused by parasitic worms that live in certain types of freshwater snails."},
    {"name": "Dengue fever", "description": "A mosquito-borne tropical disease causing severe flu-like symptoms."},
    {"name": "Hepatitis B", "description": "A serious liver infection caused by the hepatitis B virus."}
]

# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
            # Add predefined illnesses if they don't exist
            for illness in PREDEFINED_ILLNESSES:
                if not any(p['name'] == illness['name'] for p in data['programs']):
                    data['programs'].append(illness)
            return data
    # Initialize with predefined illnesses if file doesn't exist
    return {'clients': [], 'programs': PREDEFINED_ILLNESSES.copy(), 'enrollments': []}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Health Program Class
class HealthProgram:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_dict(self):
        return {'name': self.name, 'description': self.description}

# Client Class
class Client:
    def __init__(self, client_id, name, age, gender):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.gender = gender

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

# Web Interface Routes
@app.route('/')
def home():
    data = load_data()
    
    # Enhance clients data with their enrolled programs
    enhanced_clients = []
    for client in data['clients']:
        enrolled_programs = [
            e['program_name'] for e in data['enrollments']
            if e['client_id'] == client['client_id']
        ]
        enhanced_client = client.copy()
        enhanced_client['enrolled_programs'] = enrolled_programs
        enhanced_clients.append(enhanced_client)
    
    return render_template('index.html', 
                         clients=enhanced_clients, 
                         programs=data['programs'])

@app.route('/web/create_program', methods=['GET', 'POST'])
def web_create_program():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        use_predefined = request.form.get('use_predefined')
        
        data = load_data()
        
        if use_predefined:
            # Using predefined illness
            predefined_name = request.form.get('predefined_name')
            illness = next((ill for ill in PREDEFINED_ILLNESSES if ill['name'] == predefined_name), None)
            if illness:
                if not any(p['name'] == illness['name'] for p in data['programs']):
                    data['programs'].append(illness)
                    save_data(data)
                    return redirect(url_for('home'))
                else:
                    error = "This predefined program already exists in the system"
            else:
                error = "Invalid predefined program selected"
        else:
            # Creating custom program
            if not name or not description:
                error = "Program name and description are required!"
            elif any(p['name'] == name for p in data['programs']):
                error = "Program already exists!"
            else:
                new_program = HealthProgram(name, description)
                data['programs'].append(new_program.to_dict())
                save_data(data)
                return redirect(url_for('home'))
        
        return render_template('create_program.html', 
                            predefined_illnesses=PREDEFINED_ILLNESSES,
                            error=error)
    
    return render_template('create_program.html', 
                         predefined_illnesses=PREDEFINED_ILLNESSES)

@app.route('/web/register_client', methods=['GET', 'POST'])
def web_register_client():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        
        if not client_id or not name or not age or not gender:
            return render_template('register_client.html', error="All fields are required!")
        
        data = load_data()
        
        # Check if client already exists
        if any(c['client_id'] == client_id for c in data['clients']):
            return render_template('register_client.html', error="Client ID already exists!")
        
        new_client = Client(client_id, name, age, gender)
        data['clients'].append(new_client.to_dict())
        save_data(data)
        return redirect(url_for('home'))
    
    return render_template('register_client.html')

@app.route('/web/enroll_client', methods=['GET', 'POST'])
def web_enroll_client():
    data = load_data()
    
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        program_name = request.form.get('program_name')

        # Check if client and program exist
        client = next((c for c in data['clients'] if c['client_id'] == client_id), None)
        program = next((p for p in data['programs'] if p['name'] == program_name), None)

        if not client or not program:
            return render_template('enroll_client.html', 
                                clients=data['clients'], 
                                programs=data['programs'],
                                error="Client or program not found!")

        # Check if enrollment already exists
        enrollment_exists = any(
            e['client_id'] == client_id and e['program_name'] == program_name
            for e in data['enrollments']
        )
        
        if enrollment_exists:
            return render_template('enroll_client.html', 
                                clients=data['clients'], 
                                programs=data['programs'],
                                error="Client is already enrolled in this program!")
        
        # Add new enrollment
        data['enrollments'].append({
            'client_id': client_id,
            'program_name': program_name
        })
        save_data(data)
        return redirect(url_for('home'))
    
    return render_template('enroll_client.html', 
                         clients=data['clients'], 
                         programs=data['programs'])

@app.route('/web/view_profile/<client_id>')
def web_view_profile(client_id):
    data = load_data()
    client = next((c for c in data['clients'] if c['client_id'] == client_id), None)
    
    if client:
        enrolled_programs = [
            e['program_name'] for e in data['enrollments']
            if e['client_id'] == client_id
        ]
        
        # Get program details for enrolled programs
        program_details = []
        for program_name in enrolled_programs:
            program = next((p for p in data['programs'] if p['name'] == program_name), None)
            if program:
                program_details.append(program)
        
        return render_template('view_profile.html', 
                             client=client,
                             enrolled_programs=program_details)
    else:
        return render_template('error.html', message="Client not found!")

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data({'clients': [], 'programs': PREDEFINED_ILLNESSES.copy(), 'enrollments': []})
    app.run(debug=True)