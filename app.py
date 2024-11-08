from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mutant_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DNARecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dna_sequence = db.Column(db.String, unique=True, nullable=False)
    is_mutant = db.Column(db.Boolean, nullable=False)


with app.app_context():
    db.create_all()

def is_mutant(dna):
    n = len(dna)
    count = 0

    def check_sequence(i, j, delta_i, delta_j):
        sequence = dna[i][j]
        for k in range(1, 4):
            i += delta_i
            j += delta_j
            if i >= n or j >= n or j < 0 or dna[i][j] != sequence:
                return False
        return True

  
    for i in range(n):
        for j in range(n):
            if j + 3 < n and check_sequence(i, j, 0, 1):
                count += 1
            if i + 3 < n and check_sequence(i, j, 1, 0):
                count += 1
            if i + 3 < n and j + 3 < n and check_sequence(i, j, 1, 1):
                count += 1
            if i + 3 < n and j - 3 >= 0 and check_sequence(i, j, 1, -1):
                count += 1

            if count > 1:
                return True

    return False
@app.route('/')
def home():
    return "Bienvenido a la API de Mutant Detector. Usa el endpoint /mutant para verificar ADN.", 200
    
@app.route('/mutant', methods=['POST'])
def mutant():
    data = request.get_json()
    dna = data.get('dna', [])
    if not dna:
        return "Bad Request: Missing 'dna' parameter", 400

    
    dna_sequence_str = ','.join(dna)

    record = DNARecord.query.filter_by(dna_sequence=dna_sequence_str).first()
    if record:
        is_mutant_result = record.is_mutant
    else:
   
        is_mutant_result = is_mutant(dna)
       
        new_record = DNARecord(dna_sequence=dna_sequence_str, is_mutant=is_mutant_result)
        db.session.add(new_record)
        db.session.commit()


    if is_mutant_result:
        return "Mutant detected", 200
    else:
        return "Forbidden", 403

@app.route('/stats', methods=['GET'])
def stats():
  
    count_mutant_dna = DNARecord.query.filter_by(is_mutant=True).count()
    count_human_dna = DNARecord.query.filter_by(is_mutant=False).count()


    if (count_human_dna + count_mutant_dna) > 0:
        ratio = count_mutant_dna / (count_human_dna + count_mutant_dna)
    else:
        ratio = 0

 
    return jsonify({
        "count_mutant_dna": count_mutant_dna,
        "count_human_dna": count_human_dna,
        "ratio": ratio
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
