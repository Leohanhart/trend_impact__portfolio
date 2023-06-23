import multiprocessing
import time


lock = multiprocessing.Lock()


def task_function(task_name):
    with lock:
        print(f"Task {task_name} is executing.")
        time.sleep(1)  # Simulate some task execution time
        print(f"Task {task_name} is done.")


if __name__ == "__main__":
    # Create a lock object

    # Define the task names
    tasks = ["A", "B", "C"]

    # Create a process for each task
    processes = []
    for task in tasks:
        process = multiprocessing.Process(target=task_function, args=(task))
        processes.append(process)

    # Start the processes
    for process in processes:
        process.start()

    # Wait for the processes to finish
    for process in processes:
        process.join()
