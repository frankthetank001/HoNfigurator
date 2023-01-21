import subprocess
output = subprocess.Popen(['git','pull'],stdout=subprocess.PIPE)
result = output.stdout.read()
result = result.decode()

if "local changes" in output.stdout:
    print("resetting repository...")
    subprocess.Popen(['git','reset','--hard'])
    subprocess.Popen(['git','pull'])