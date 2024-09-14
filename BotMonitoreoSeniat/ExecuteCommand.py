import paramiko as piko
import logging
logger = logging.getLogger(__name__)


class ExecuteCommand(object):
	def __init__(self, host, port, user, password):
		self.host = host
		self.port = port
		self.user = user
		self.password = password

	def execute(self, command):
		client = piko.SSHClient()
		client.set_missing_host_key_policy(piko.AutoAddPolicy())

		try:
			client.connect(self.host, self.port, self.user, self.password)

			current_command = command
			stdin, stdout, stderr = client.exec_command(current_command)

			output = stdout.read().decode('utf-8')
			lines = output.rstrip().splitlines()
			lines_ = [line for line in lines if line.strip()]
			print(lines, '\n', lines_)
			result = '\n'.join(lines_)
			client.close()
			print(result)
			return result

		except piko.AuthenticationException as e:
			logger.error(f"Error de autenticación al conectarse al servidor: {e}")
			return False

		except piko.SSHException as e:
			logger.error(f"Error SSH al conectarse al servidor: {e}")
			return False

		except piko.socket.error as e:
			logger.error(f"Error de conexión al servidor: {e}")
			return False

		except Exception as e:
			logger.error(f"Error desconocido al ejecutar el comando: {e}")
			return False


if __name__ == '__main__':

	ssh = ExecuteCommand('172.16.17.14', 22, 'k8s', 'seniat')
	# result = ssh.execute("zabbix_get -k opmn_ping -s 172.16.16.160")
	# result = ssh.execute('curl -d \'{"usuario": "11942322","clave": "rrecmwgc5"}\' -H "Content-Type: application/json" -X POST http://dgpatrimonios.seniat.gob.ve/AutenticadorOracle/auth/interno/login | jq .mensaje | sed -e \'s/"//\' -e \'s/"$//\'')
	result = ssh.execute(f"""output=$(sshpass -p {ssh.password} ssh {ssh.user}@{ssh.host} 'kubectl get nodes')
													problem_nodes=$(echo "$output" | grep -v "Ready" | grep -v "NAME" | wc -l)
													if [ "$problem_nodes" -eq 0 ]; then
														echo "       ✅ Cluster K8S Producción OK"
													else
														echo "       ❌ Problemas en el cluster. Los siguientes nodos no están listos:"
														echo "$output" | grep -v "Ready" | grep -v "NAME"
													fi
												""")

	print(result)