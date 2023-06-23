from multiprocessing import Process, Queue
from time import sleep

# Example task to be executed
def process_task(task):
    # Simulate some processing time
    sleep(1)
    # Perform some processing on the task
    result = task**2
    return result


# Function to add tasks to the queue
def add_tasks(queue, start_task):
    counter = start_task
    while True:
        print("Adding task:", counter)
        queue.put(counter)
        counter += 1
        sleep(1)


# Function to process tasks from the queue and put results in another queue
def process_queue(input_queue, output_queue):
    while True:
        task = input_queue.get()  # Get a task from the input queue
        result = process_task(task)  # Process the task
        output_queue.put((task, result))  # Put the result in the output queue


if __name__ == "__main__":
    # Create a queue for tasks
    task_queue = Queue()

    # Create a queue for results
    result_queue = Queue()

    # Create three processes to add tasks to the queue
    add_process1 = Process(target=add_tasks, args=(task_queue, 1))
    add_process2 = Process(target=add_tasks, args=(task_queue, 10))
    add_process3 = Process(target=add_tasks, args=(task_queue, 20))

    # Create a process to process tasks from the queue and put results in the result queue
    process_process = Process(
        target=process_queue, args=(task_queue, result_queue)
    )

    # Start the processes
    add_process1.start()
    add_process2.start()
    add_process3.start()
    process_process.start()

    try:
        # Process the results from the result queue and print them
        while True:
            task, result = result_queue.get()
            print("Result for task", task, ":", result)
    except KeyboardInterrupt:
        # Terminate the processes if Ctrl+C is pressed
        add_process1.terminate()
        add_process2.terminate()
        add_process3.terminate()
        process_process.terminate()
        add_process1.join()
        add_process2.join()
        add_process3.join()
        process_process.join()
