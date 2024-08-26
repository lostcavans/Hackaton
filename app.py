from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ejecuta el script de Python (por ejemplo, main.py)
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
        # Devuelve la salida del script
        return jsonify({'stdout': result.stdout, 'stderr': result.stderr})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
