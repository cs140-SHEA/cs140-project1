# Multi-level Feedback Queue Scheduler Input Handling

def main():
    # Prompt for number of processes
    print("# Enter Scheduler Details #")
    num_processes = int(input())  # Line 0: Number of processes (N)

    # Prompt for time allotment for Q1
    time_allotment_q1 = int(input())  # Line 1: Time Allotment for Q1

    # Prompt for time allotment for Q2
    time_allotment_q2 = int(input())  # Line 2: Time Allotment for Q2

    # Prompt for context switch time
    context_switch_time = int(input())  # Line 3: Time for Context Switch

    # Prompt for process details
    print(f"# Enter {num_processes} Process Details #")
    processes = []
    for _ in range(num_processes):
        process_input = input()  # Line 4 onwards: Process details
        process_data = process_input.split(";")
        bursts = process_data[2:]
        structured_bursts = []

        # Label CPU and I/O bursts separately
        for i, burst in enumerate(bursts):
            if i % 2 == 0:
                structured_bursts.append({"type": "CPU", "duration": int(burst)})
            else:
                structured_bursts.append({"type": "IO", "duration": int(burst)})

        processes.append({
            "name": process_data[0],
            "arrival_time": int(process_data[1]),
            "bursts": structured_bursts,
            "queue_level": None,  # Track which queue the process is in
            "quantum_counter": 0, # Track remaining quantum time for Q1 RR
            "allotment_counter": 0, # Track remaining allotment time for Q1
            "start_time": None,   # Track the start time of the process
            "finish_time": None,  # Track the finish time of the process
            "waiting_time": 0     # Track the total waiting time for the process
        })

    # Initialize queues
    Q1 = []  # Top Priority Queue (Round Robin)
    Q2 = []  # Medium Priority Queue (First-Come, First-Served)
    Q3 = []  # Least Priority Queue (Shortest Job First)

    # Simulation parameters
    current_time = 0
    cpu_state = None  # Currently running process in CPU
    io_state = []  # List of processes performing I/O
    finished_process = [] # List of recently finished processes
    done_process = [] # List of already done processes
    demoted_process = [] # List of demoted processes
    prev_cpu_process = None  # Track the previous process that was running on CPU to avoid context switch if the same

    # Begin time-based simulation
    print("# Scheduling Results #")
    while processes or Q1 or Q2 or Q3 or cpu_state or io_state or finished_process:
        print(f"At Time = {current_time}")

        # Check for newly arriving processes
        arriving_processes = []
        for process in processes[:]:
            if process["arrival_time"] == current_time:
                process["queue_level"] = "Q1"
                process["quantum_counter"] = 4 # Initialize quantum counter for Q1
                process["allotment_counter"] = time_allotment_q1
                Q1.append(process)
                arriving_processes.append(process["name"])
                processes.remove(process)
        if arriving_processes:
            print(f"Arriving: [{', '.join(arriving_processes)}]")

        # Check for finished processes
        for _ in finished_process[:]:
            process = finished_process.pop(0)
            print(process, " DONE")

        for _ in demoted_process[:]:
            process = demoted_process.pop(0)
            print(process, " DEMOTED")

        # Handle CPU execution
        if not cpu_state and Q1:
            cpu_state = Q1.pop(0)  # Take process from Q1
            if prev_cpu_process != cpu_state:
                prev_cpu_process = cpu_state
            if cpu_state["start_time"] is None:
                cpu_state["start_time"] = current_time  # Mark start time
            
        elif not cpu_state and Q2:
            cpu_state = Q2.pop(0)  # Take process from Q2
            if prev_cpu_process != cpu_state:
                prev_cpu_process = cpu_state

        elif not cpu_state and Q3:
            cpu_state = min(Q3, key=lambda p: p["bursts"][0]["duration"])  # Shortest Job First
            Q3.remove(cpu_state)
            if prev_cpu_process != cpu_state:
                prev_cpu_process = cpu_state

        # print(cpu_state) # for debugging 
        # Simulate CPU execution
        if cpu_state:
            current_burst = cpu_state["bursts"][0]
            if current_burst["type"] == "CPU":
                current_burst["duration"] -= 1 
                cpu_state["allotment_counter"] -= 1  # Decrement the process's allotment counter
                if cpu_state["queue_level"] == "Q1":
                    cpu_state["quantum_counter"] -= 1 # Decrement the process's Q1 RR quantum counter

                # Check if CPU burst is complete
                if current_burst["duration"] == 0:
                    cpu_state["bursts"].pop(0)  # Remove completed burst
                    if not cpu_state["bursts"]:  # Process is done
                        cpu_state["finish_time"] = current_time + 1  # Mark finish time
                        finished_process.append(cpu_state['name'])
                        done_process.append(cpu_state)
                        cpu_state = None
                    else:
                        io_state.append(cpu_state)
                        cpu_state = None

                # Check if quantum expires
                elif cpu_state["queue_level"] == "Q1":
                    if cpu_state["allotment_counter"] == 0:
                        demoted_process.append(cpu_state['name'])
                        cpu_state["queue_level"] = "Q2"
                        cpu_state["allotment_counter"] = time_allotment_q2 # Initialize quantum counter for Q2
                        Q2.append(cpu_state)
                        cpu_state = None
                    elif cpu_state["quantum_counter"] == 0:
                        # reset quantum_counter
                        cpu_state["quantum_counter"] = 4
                        # go to next ready process
                        Q1.append(cpu_state)
                        cpu_state = None


                elif cpu_state["queue_level"] == "Q2" and cpu_state["allotment_counter"] == 0:
                    demoted_process.append(cpu_state['name'])
                    cpu_state["queue_level"] == "Q3"
                    Q3.append(cpu_state)
                    cpu_state = None

        # Simulate I/O
        for io_process in io_state[:]:
            current_burst = io_process["bursts"][0]
            if current_burst["type"] == "IO":
                current_burst["duration"] -= 1
                if current_burst["duration"] == 0:
                    io_process["bursts"].pop(0)
                    if not io_process["bursts"]:  # Process is done
                        print(f"At Time = {current_time}")
                        finished_process.append(io_process['name'])
                        done_process.append(io_process)
                    else:
                        if io_process["queue_level"] == "Q1":
                            io_process["allotment_counter"] = time_allotment_q1  # Reset quantum counter for Q1
                            Q1.append(io_process)
                        elif io_process["queue_level"] == "Q2":
                            io_process["allotment_counter"] = time_allotment_q2  # Reset quantum counter for Q2
                            Q2.append(io_process)
                        else:
                            Q3.append(io_process)
                    io_state.remove(io_process)

        # Print state
        print(f"Queues: [{', '.join(p['name'] for p in Q1)}]; [{', '.join(p['name'] for p in Q2)}]; [{', '.join(p['name'] for p in Q3)}]")
        if cpu_state:
            print(f"CPU: {cpu_state['name']}") 
            print(f"{cpu_state['queue_level']}") # for debugging
        else:
            print("CPU: []")
        print(f"I/O: [{', '.join(p['name'] for p in io_state)}]")
        print()

        # Increment time
        current_time += 1

    # Print simulation end
    print("# SIMULATION DONE #")
    # print(done_process) # for debugging

    # total_turnaround_time = 0
    # total_waiting_time = 0
    # for process in processes + Q1 + Q2 + Q3:
    #     turn_around_time = process["finish_time"] - process["arrival_time"]
    #     waiting_time = turn_around_time - sum(burst["duration"] for burst in process["bursts"])

    #     print(f"Turn-around time for {process['name']} : {process['finish_time']} - {process['arrival_time']} = {turn_around_time} ms")
    #     print(f"Waiting time for {process['name']} : {waiting_time} ms")
    #     total_turnaround_time += turn_around_time
    #     total_waiting_time += waiting_time

    # avg_turnaround_time = total_turnaround_time / num_processes
    # avg_waiting_time = total_waiting_time / num_processes
    # print(f"Average Turn-around time = {avg_turnaround_time:.2f} ms")
    # print(f"Average Waiting time = {avg_waiting_time:.2f} ms")

    # Print simulation end
    print("\n# Simulation Complete #")

if __name__ == "__main__":
    main()
