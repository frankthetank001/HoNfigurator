import subprocess
output = subprocess.Popen(['git','pull'])

if "local changes" in output:
    subprocess.Popen(['git','reset','--hard'])
    subprocess.Popen(['git','pull'])