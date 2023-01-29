import subprocess
output = subprocess.Popen(['git','pull'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
result = output.stdout.read()
result = result.decode()

if "local changes" in output.stderr:
    print("resetting repository...")
    subprocess.Popen(['git','reset','--hard'])
    subprocess.Popen(['git','pull'])
subprocess.Popen('honfigurator.exe')