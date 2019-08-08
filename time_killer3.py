import multiprocessing
import time

# bar
def bar(return_dict):
    for i in range(100):
        print("Tick")
        time.sleep(1)
        return_dict[i] = "bee"


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    # Start bar as a process
    p = multiprocessing.Process(target=bar, args=(return_dict, ))   # note the use of ,
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(4)

    # If thread is still active
    if p.is_alive():
        print("running... let's kill it...")

        # Terminate
        p.terminate()
        p.join()
    # print(return_dict.values())