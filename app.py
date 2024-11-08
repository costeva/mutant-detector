from flask import Flask, request, jsonify

app = Flask(__name__)

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

    # Buscar secuencias horizontales, verticales y diagonales
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
    if is_mutant(dna):
        return "Mutant detected", 200
    else:
        return "Forbidden", 403

if __name__ == '__main__':
    app.run(debug=True, port=5000)