import subprocess
import pprint

result = subprocess.run(['echo', '자식 프로세스가 보내는 인사!'],
                        capture_output=True,
                        encoding='utf-8'
                        )

result.check_returncode()
print(result.stdout)

proc = subprocess.Popen(['sleep', '3'])
while proc.poll() is None:
    print("작업 중..")

print('종료 상태', proc.poll())

import time

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()
end = time.time()
delta = end - start
print(f"{delta:.3}초만에 끝남")

import os


def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zfShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

procs = []
