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
            "queue_level": "Q1",  # Track which queue the process is in
            "quantum_counter": time_allotment_q1, # Initial quantum time for Q1
            "start_time": None,   # Track the start time of the process
            "finish_time": None,  # Track the finish time of the process
            "waiting_time": 0,    # Track the total waiting time for the process
            "turnaround_time": 0
        })

    # Initialize queues
    Q1 = []  # Top Priority Queue (Round Robin)
    Q2 = []  # Medium Priority Queue (First-Come, First-Served)
    Q3 = []  # Least Priority Queue (Shortest Job First)

    # Simulation parameters
    current_time = 0
    cpu_state = None  # Currently running process in CPU
    io_state = []  # List of processes performing I/O
    prev_cpu_process = None  # Track the previous process that was running on CPU to avoid context switch if the same
   
    event_log = [] # Event Log

    # Begin Simulation
    print("# Scheduling Results #")
    while processes or Q1 or Q2 or Q3 or cpu_state or io_state:
        # Log and display the current time
        log_entry = f"Time {current_time}:"
        print(f"At Time = {current_time}")

        # Handle New Arrivals
        arriving_processes = []
        for process in processes[:]:
            if process["arrival_time"] == current_time:
                process["queue_level"] = "Q1"
                process["quantum_counter"] = time_allotment_q1
                Q1.append(process)
                arriving_processes.append(process["name"])
                processes.remove(process)

        if arriving_processes:
            log_entry += f" Arrivals: [{', '.join(arriving_processes)}]"

        # CPU Execution
        if not cpu_state:
            if Q1:
                cpu_state = Q1.pop(0)
                cpu_state["quantum_counter"] = min(cpu_state["quantum_counter"], time_allotment_q1)
            elif Q2:
                cpu_state = Q2.pop(0)
            elif Q3:
                cpu_state = min(Q3, key=lambda p: p["bursts"][0]["duration"])
                Q3.remove(cpu_state)

            if cpu_state and prev_cpu_process != cpu_state:
                current_time += context_switch_time
                log_entry += f" Context Switch to {cpu_state['name']}"
                prev_cpu_process = cpu_state

        # Process CPU Burst
        if cpu_state:
            current_burst = cpu_state["bursts"][0]
            current_burst["duration"] -= 1
            cpu_state["quantum_counter"] -= 1

            # Handle CPU Burst Completion
            if current_burst["duration"] == 0:
                cpu_state["bursts"].pop(0)
                if not cpu_state["bursts"]:  # Process completes
                    cpu_state["finish_time"] = current_time + 1
                    cpu_state["turnaround_time"] = cpu_state["finish_time"] - cpu_state["arrival_time"]
                    log_entry += f" {cpu_state['name']} Finished"
                    cpu_state = None
                else:  # Move to I/O
                    io_state.append(cpu_state)
                    log_entry += f" {cpu_state['name']} Moved to I/O"
                    cpu_state = None

            # Handle Quantum Expiry
            elif cpu_state["queue_level"] == "Q1" and cpu_state["quantum_counter"] == 0:
                log_entry += f" {cpu_state['name']} Demoted to Q2"
                cpu_state["queue_level"] = "Q2"
                cpu_state["quantum_counter"] = time_allotment_q2
                Q2.append(cpu_state)
                cpu_state = None
            elif cpu_state["queue_level"] == "Q2" and cpu_state["quantum_counter"] == 0:
                log_entry += f" {cpu_state['name']} Demoted to Q3"
                cpu_state["queue_level"] = "Q3"
                Q3.append(cpu_state)
                cpu_state = None

        # Process I/O Burst
        for process in io_state[:]:
            current_burst = process["bursts"][0]
            current_burst["duration"] -= 1
            if current_burst["duration"] == 0:
                process["bursts"].pop(0)
                if not process["bursts"]:
                    log_entry += f" {process['name']} Finished"
                else:
                    if process["queue_level"] == "Q1":
                        process["quantum_counter"] = time_allotment_q1
                        Q1.append(process)
                    elif process["queue_level"] == "Q2":
                        process["quantum_counter"] = time_allotment_q2
                        Q2.append(process)
                    else:
                        Q3.append(process)
                io_state.remove(process)

        # Update Waiting Times for All Queues
        for process in Q1 + Q2 + Q3:
            process["waiting_time"] += 1

        # Print Scheduler State
        print(f"Queues: Q1[{', '.join(p['name'] for p in Q1)}], Q2[{', '.join(p['name'] for p in Q2)}], Q3[{', '.join(p['name'] for p in Q3)}]")
        if cpu_state:
            print(f"CPU: {cpu_state['name']} ({cpu_state['queue_level']})")
        else:
            print("CPU: []")
        print(f"I/O: [{', '.join(p['name'] for p in io_state)}]")
        print()

        # Add log entry and increment time
        event_log.append(log_entry)
        current_time += 1

    # Final Output
    print("# SIMULATION COMPLETE #")
    print("\n# Process Statistics #")
    total_turnaround_time = 0
    total_waiting_time = 0

    for process in sorted(Q1 + Q2 + Q3 + io_state + ([cpu_state] if cpu_state else []), key=lambda p: p["name"]):
        turnaround_time = process["turnaround_time"]
        waiting_time = process["waiting_time"]
        print(f"{process['name']} - Turnaround Time: {turnaround_time}, Waiting Time: {waiting_time}")
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time

    # Averages
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes
    print(f"\nAverage Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")

if __name__ == "__main__":
    main()