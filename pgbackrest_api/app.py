from flask import Flask, jsonify
import subprocess
import json
from datetime import datetime, date

app = Flask(__name__)


def run_pgbackrest_command(command):
    ssh_command = f'ssh pgbackrest@172.16.34.73 "{command}"'
    try:
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return str(e), None


@app.route('/api/backups', methods=['GET'])
def get_backups():
    # command = 'pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza=seniat info'
    command = 'pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza=seniat --output=json info | jq'
    stdout, stderr = run_pgbackrest_command(command)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500
    return jsonify({'status': 'success', 'data': stdout})

@app.route('/api/backups/last', methods=['GET'])
def get_last_backup():
    command = 'pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --output=json --stanza=seniat info | jq \'.[0] | .backup[-1]\''
    stdout, stderr = run_pgbackrest_command(command)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    try:
        last_backup = json.loads(stdout)
    except json.JSONDecodeError as e:
        return jsonify({'status': 'error', 'message': f'Error parsing JSON: {str(e)}'}), 500

    return jsonify({'status': 'success', 'data': last_backup})

@app.route('/api/status', methods=['GET'])
def get_status():
    command = 'pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza=seniat check'
    stdout, stderr = run_pgbackrest_command(command)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500
    return jsonify({'status': 'success', 'data': stdout})

@app.route('/api/check_archives', methods=['GET'])
def check_archives():
    command = 'check_pgbackrest --stanza=seniat --service=archives --config=/etc/pgbackrest/backrest_standby.conf --output=json'
    stdout, stderr = run_pgbackrest_command(command)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    return jsonify({'status': 'success', 'data': json.loads(stdout)})

@app.route('/api/check_retention', methods=['GET'])
def check_retention():
    command = 'check_pgbackrest --stanza=seniat --service=retention --config=/etc/pgbackrest/backrest_standby.conf --output=json --retention-full=2 --retention-incr=8 --retention-age=1d | jq'
    stdout, stderr = run_pgbackrest_command(command)
    if stderr:
        return jsonify({'status': 'error', 'message': stderr}), 500

    return jsonify({'status': 'success', 'data': json.loads(stdout)})


if __name__ == '__main__':
    app.run(host='10.156.80.115', port=6500)
