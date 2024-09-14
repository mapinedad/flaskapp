from flask import Flask, jsonify
import subprocess
import json
from datetime import datetime, date

app = Flask(__name__)

# Mapping of databases to their server IPs
DB_SERVER_MAP = {
    'seniat': '172.16.34.73',
    'psuv': '172.16.56.46'
}

def run_pgbackrest_command(db, command_suffix):
    server_ip = DB_SERVER_MAP.get(db)
    if not server_ip:
        return None, f'Unknown database: {db}'
    command = f'pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza={db} {command_suffix}'
    ssh_command = f'ssh pgbackrest@{server_ip} "{command}"'
    try:
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return str(e), None

def run_check_pgbackrest_command(db, command_suffix):
    server_ip = DB_SERVER_MAP.get(db)
    if not server_ip:
        return None, f'Unknown database: {db}'
    command = f'check_pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza={db} {command_suffix}'
    ssh_command = f'ssh pgbackrest@{server_ip} "{command}"'
    try:
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return str(e), None

@app.route('/api/<db>/backups', methods=['GET'])
def get_backups(db):
    command_suffix = '--output=json info | jq'
    stdout, stderr = run_pgbackrest_command(db, command_suffix)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500
    return jsonify({'status': 'success', 'data': stdout})

@app.route('/api/<db>/backups/last', methods=['GET'])
def get_last_backup(db):
    command_suffix = '--output=json info | jq \'.[0] | .backup[-1]\''
    stdout, stderr = run_pgbackrest_command(db, command_suffix)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    try:
        last_backup = json.loads(stdout)
    except json.JSONDecodeError as e:
        return jsonify({'status': 'error', 'message': f'Error parsing JSON: {str(e)}'}), 500

    return jsonify({'status': 'success', 'data': last_backup})

@app.route('/api/<db>/status', methods=['GET'])
def get_status(db):
    command_suffix = 'check'
    stdout, stderr = run_pgbackrest_command(db, command_suffix)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500
    return jsonify({'status': 'success', 'data': stdout})

@app.route('/api/<db>/check_archives', methods=['GET'])
def check_archives(db):
    command_suffix = '--service=archives --output=json'
    stdout, stderr = run_check_pgbackrest_command(db, command_suffix)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    return jsonify({'status': 'success', 'data': json.loads(stdout)})

@app.route('/api/<db>/check_retention', methods=['GET'])
def check_retention(db):
    command_suffix = '--service=retention --output=json --retention-full=2 --retention-incr=8 --retention-age=1d | jq'
    stdout, stderr = run_check_pgbackrest_command(db, command_suffix)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    return jsonify({'status': 'success', 'data': json.loads(stdout)})

if __name__ == '__main__':
    app.run(host='10.156.80.115', port=6500)
