import paramiko
import logging
from hosts import *
from ping3 import ping
from ExecuteCommand import *


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def status_oas():
    """Revisar el status OAS y sus servicios"""
    try:
        for categoria, tuplas in OAS.items():
            print(f"🔷 OAS {categoria}")

            for ip, clave in tuplas:
                if ping(ip, timeout=3):
                    try:
                        # Establecer la conexión SSH
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ip, port=22, username='oas', password=clave, timeout=5)

                        # Obtener el hostname
                        stdin, stdout, stderr = ssh.exec_command("hostname | awk -F'.' '{{print $1}}'")
                        hostname = stdout.read().decode('utf_8').strip()

                        # Verificar el status de opmn_ping
                        stdin, stdout, stderr = ssh.exec_command("cat /etc/zabbix/zabbix_agentd.d/zabbix/opmn_ping.out")
                        opmn_status = "✅ OPMN OK" if stdout.read().decode().strip() == '1' else "❌ ping failed"

                        # Verificar el status de status_islas
                        stdin, stdout, stderr = ssh.exec_command("cat /etc/zabbix/zabbix_agentd.d/zabbix/status_islas.out")
                        output = stdout.read().decode('utf_8').strip()

                        if output == "Alive":
                            oc4j_status = "✅ Alive"

                        else:
                            oc4j_status = f"❌ {output}"

                        # Imprimir el resultado
                        print(f"       {hostname} {opmn_status} \n       {hostname} {oc4j_status}")

                    except paramiko.SSHException as e:
                        print(f"       ❌ No pudo conectarse a {ip}: {e}")
                        continue  # Continuar con el siguiente servidor
                else:
                    print(f"       ❌ {ip} no responde a ping")

    except Exception as e:
        print(f"Error general: {e}")
        return False

    finally:
        ssh.close()


def status_dgp():
    """Revisar el status de DGP y sus servicios"""

    try:
        for categoria, ips in DGP.items():
            print(f"🔷 {categoria} Servicios de Declaración")

            if categoria == "CLUSTER K8S":
                for ip in ips:
                    # print(f"""{ip}""")
                    if ip == '172.16.17.14':
                        if ping(ip, timeout=3):
                            try:
                                # Establecer la conexión SSH
                                ssh = paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh.connect(ip, port=22, username='k8s', timeout=5)

                                # Verificar el status del cluster de producción
                                stdin, stdout, stderr = ssh.exec_command(f"""output=$(kubectl get nodes); problem_nodes=$(echo "$output" | grep -v "Ready" | grep -v "NAME" | wc -l); if [ "$problem_nodes" -eq 0 ]; then echo "       Cluster K8S Desarrollo ✅ OK"; else echo "       Problemas en el cluster. ❌ Los siguientes nodos no están listos:"; echo "$output" | grep -v "Ready" | grep -v "NAME"; fi""")
                                # stdin, stdout, stderr = ssh.exec_command("cat /home/k8s/scripts/status_cluster.out")
                                k8s_status = stdout.read().decode('utf_8').strip()

                                print(f"""       {k8s_status}""")
                        
                            except paramiko.SSHException as e:
                                print(f"       ❌ No pudo conectarse a {ip}: {e}")
                                continue
                        else:
                            print(f"       ❌ {ip} no responde a ping")

                    elif ip == '172.16.17.25':
                        if ping(ip, timeout=3):
                            try:
                                # Establecer la conexión SSH
                                ssh = paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh.connect(ip, port=22, username='k8s', timeout=5)

                                # Verificar el status del cluster de producción
                                stdin, stdout, stderr = ssh.exec_command(f"""output=$(kubectl get nodes); problem_nodes=$(echo "$output" | grep -v "Ready" | grep -v "NAME" | wc -l); if [ "$problem_nodes" -eq 0 ]; then echo "       Cluster K8S Calidad ✅ OK"; else echo "       Problemas en el cluster. ❌ Los siguientes nodos no están listos:"; echo "$output" | grep -v "Ready" | grep -v "NAME"; fi""")
                                # stdin, stdout, stderr = ssh.exec_command("cat /home/k8s/scripts/status_cluster.out")
                                k8s_status = stdout.read().decode('utf_8').strip()

                                print(f"""       {k8s_status}""")
                        
                            except paramiko.SSHException as e:
                                print(f"       ❌ No pudo conectarse a {ip}: {e}")
                                continue
                        else:
                            print(f"       ❌ {ip} no responde a ping")

                    elif ip == '172.16.17.7':
                        if ping(ip, timeout=3):
                            try:
                                # Establecer la conexión SSH
                                ssh = paramiko.SSHClient()
                                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh.connect(ip, port=22, username='k8s', timeout=5)

                                # Verificar el status del cluster de producción
                                stdin, stdout, stderr = ssh.exec_command(f"""output=$(kubectl get nodes); problem_nodes=$(echo "$output" | grep -v "Ready" | grep -v "NAME" | wc -l); if [ "$problem_nodes" -eq 0 ]; then echo "       Cluster K8S Producción ✅ OK"; else echo "       Problemas en el cluster. ❌ Los siguientes nodos no están listos:"; echo "$output" | grep -v "Ready" | grep -v "NAME"; fi""")
                                # stdin, stdout, stderr = ssh.exec_command("cat /home/k8s/scripts/status_cluster.out")
                                k8s_status = stdout.read().decode('utf_8').strip()


                                # Verificar el servicio de AutenticadorOracle
                                comando = 'output=$(curl -sd \'{"usuario": "11942322","clave": "rrecmwgc5"}\' -H "Content-Type: application/json" -X POST http://dgpatrimonios.seniat.gob.ve/AutenticadorOracle/auth/interno/login | jq .mensaje | sed -e \'s/"//\' -e \'s/"$//\'); if [ "$output" = \'USUARIO VALIDADO EXITOSAMENTE\' ]; then echo "       Servicio AUTENTICADORORACLE ✅ Activo"; elif [ "$output" = \'Usuario o Clave Inválida\' ];  then echo "       AUTENTICADORORACLE 🛑 Usuario o Clave Inválida"; else [ "$output" = \'\' ];  echo "       Servicio AutenticadorOracle ❌ down"; fi'

                                stdin, stdout, stderr = ssh.exec_command(comando)
                                status_autenticador = stdout.read().decode().strip()

                                comando_2 = 'output=$(curl -d \'{"usuario": "11942322","clave": "rrecmwgc5"}\' -H "Content-Type: application/json" -X POST http://dgpatrimonios.seniat.gob.ve/declaraciongp/GenUsuarioInternet/login | jq .[].resultado.message | sed -e \'s/"//\' -e \'s/"$//\'); if [ "$output" = "Usuario Valido" ]; then echo "       Servicio DECLARACIONGP ✅ Activo"; elif [ "$output" = "Usuario o Clave Inválida" ]; then echo "       DECLARACIONGP 🛑 Usuario o Clave Inválida"; else [ "$output" = "" ]; echo "       Servicio DECLARACIONGP ❌ down"; fi'

                                stdin, stdout, stderr = ssh.exec_command(comando_2)
                                status_declaraciongp = stdout.read().decode().strip()

                                print(f"""       {k8s_status}\n       {status_autenticador}\n       {status_declaraciongp}""")
                        
                            except paramiko.SSHException as e:
                                print(f"       ❌ No pudo conectarse a {ip}: {e}")
                                continue
                        else:
                            print(f"       ❌ {ip} no responde a ping")

            elif categoria == "BD POSTGRES":
                for ip in ips:
                    if ping(ip, timeout=3):
                        try:
                            # Establecer la conexión SSH
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(ip, port=22, username='postgres', timeout=5)

                            # Verificar el status de los nodos de base de datos del cluster
                            stdin, stdout, stderr = ssh.exec_command(f"""output=$(systemctl is-active postgresql); if [ "$output" = 'active' ]; then echo "$(hostname) ✅ $(systemctl is-active postgresql | tr [:lower:] [:upper:])"; else echo "$(hostname) ❗️$(systemctl is-active postgresql | tr [:lower:] [:upper:])"; fi""")

                            postgresql_status = stdout.read().decode('utf_8').strip()

                            stdin, stdout, stderr = ssh.exec_command(f"""output=$(repmgr -f /etc/postgresql/15/main/repmgr.conf node check | grep -E 'Server role|Replication lag|WAL archiving|Upstream connection|Missing physical replication slots' | awk '/OK/ {{count++}} END {{if (count == 5) print "OK"; else print "Problemas"}}'); if [ "$output" = 'OK' ]; then echo "$(hostname) Replicación ✅ $output"; else echo "$(hostname) ❗️$output"; fi""")

                            replication_status = stdout.read().decode('utf_8').strip()

                            # print(f"""       {postgresql_status}""")
                            print(f"""       {postgresql_status}\n       {replication_status}""")

                        except paramiko.SSHException as e:
                            print(f"       ❌ No pudo conectarse a {ip}: {e}")
                            continue  # Continuar con el siguiente servidor

                    else:
                        print(f"       ❌ {ip} no responde a ping")
            
            elif categoria == "PGBACKREST":
                for ip in ips:
                    if ping(ip, timeout=3):
                        try:
                            # Establecer la conexión SSH
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(ip, port=22, username='pgbackrest', timeout=5)

                            # Verificar el status del pgbackrest y su stanza (seniat)
                            stdin, stdout, stderr = ssh.exec_command(f"""output=$(pgbackrest --config=/etc/pgbackrest/backrest_standby.conf --stanza=seniat check | grep "completed successfully" | awk '{{print $9}}' | tr [:lower:] [:upper:]); if ["$output" = 'SUCCESSFULLY']; then echo "$(hostname) Stanza ✅ $output"; else echo "$(hostname) ❗️$output"; fi""")

                            stanza_status = stdout.read().decode('utf_8').strip()

                            print(f"       {stanza_status}")

                        except paramiko.SSHException as e:
                            print(f"       ❌ No pudo conectarse a {ip}: {e}")
                            continue  # Continuar con el siguiente servidor

                    else:
                        print(f"       ❌ {ip} no responde a ping")
    except:
        return False


def test_func():
    try:
        ssh = ExecuteCommand(HOST, PORT, USER, PASSWORD)

        for categoria, tuplas in OAS.items():
            print(f"🔷 {categoria}")
            for ip, clave in tuplas:
                print(f"  IP: {ip}, Clave: {clave}")
                # Aquí puedes realizar las acciones que necesites con cada IP y clave.
                # Por ejemplo, podrías usarlos para conectarte a través de SSH.
                # También puedes almacenarlos en variables si los necesitas para acciones posteriores.
                # Realiza tus operaciones aquí.
                print("\n")
    except:
        return False



if __name__=='__main__':

    status_oas()
    status_dgp()
    # test_func()