import subprocess
import os

def run_script(script_name):
    script_path = os.path.join(r'C:\Users\mapinedad\Documents\work_scripts\PYTHON\CONTROL_CAMBIO_SIADM_PROD', script_name)
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}:\n{e.stderr}")
        raise

def main():
    scripts_to_run = [
        'copyToAdmin.py',
        'connectToSIADM.py'
    ]
    
    for script in scripts_to_run:
        print(f"Running {script}...")
        run_script(script)
        print(f"Finished running {script}\n")
        
if __name__ == "__main__":
    main()