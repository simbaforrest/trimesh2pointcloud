import signal

# Register an handler for the timeout
def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")


# This function *may* run for an indetermined time...
def loop_forever():
    import time
    while 1:
        print("sec")
        time.sleep(1)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)
    try:
       loop_forever()
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    main()
