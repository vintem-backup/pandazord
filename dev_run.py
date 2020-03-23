import os
import sys

def export_env_var(path_to_env_file):

    export_status = 'fail'

    try:
        
        with open(path_to_env_file) as entry_file:

            environments_vars = entry_file.readlines()

            for i in range(len(environments_vars)):

                if (('=' in environments_vars[i]) and 
                ('#' not in environments_vars[i])):
                    
                    key=environments_vars[i].split('=')[0]
                    value=environments_vars[i].split('=')[1].split()[0]
                    os.environ[key] = value

                    export_status = 'done'
    
    except: pass #TODO: tratar exceção aqui
    
    return export_status

export_env_var('.env')

command = 'docker-compose -f dev-compose.yml up > docker-compose-devlog 2>&1 &'
os.system(command)

try:
    mode = str(sys.argv[1])
    if (mode == 'server'): shell_to_run = 'dev_run.sh'
    elif (mode == 'jupyter'): shell_to_run = 'jupyter.sh'

    command = 'chmod +x ' + shell_to_run
    os.system(command)

    command = 'sh ' + shell_to_run
    os.system(command)

except:
    print('Undefined mode')