import subprocess


l = subprocess.Popen(['npm', 'run', 'dev'], stdout=subprocess.DEVNULL ,cwd='/app/metacad')