import subprocess as sp
from threading import Timer


def kill_proc(proc):
    proc.kill()
    print('Process running overtime! Killed.')


def run_proc_timeout(proc, timeout_sec):
    # kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        proc.communicate()
    finally:
        timer.cancel()


def main():
    CMD = 'echo YOUR COMMAND'
    timeout_sec = 10.
    try:
        proc = sp.Popen(CMD)
        run_proc_timeout(proc, timeout_sec)
    except Exception as e:
        print(e)