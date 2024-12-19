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
            "bursts": structured_bursts
        })

    # Print inputs for debugging (can be removed later)
    print("\n# Inputs Captured:\n")
    print(f"Number of Processes: {num_processes}")
    print(f"Time Allotment for Q1: {time_allotment_q1} ms")
    print(f"Time Allotment for Q2: {time_allotment_q2} ms")
    print(f"Context Switch Time: {context_switch_time} ms")
    print("Processes:")
    for process in processes:
        print(process)

if __name__ == "__main__":
    main()



# Multi-level Feedback Queue Scheduler Input Handling
'''
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

        # Pair CPU and I/O bursts sequentially
        for i in range(len(bursts)):
            if i % 2 == 0:
                structured_bursts.append({"CPU": int(bursts[i])})
            else:
                structured_bursts[-1]["IO"] = int(bursts[i])

        processes.append({
            "name": process_data[0],
            "arrival_time": int(process_data[1]),
            "bursts": structured_bursts
        })

    # Print inputs for debugging (can be removed later)
    print("\n# Inputs Captured:\n")
    print(f"Number of Processes: {num_processes}")
    print(f"Time Allotment for Q1: {time_allotment_q1} ms")
    print(f"Time Allotment for Q2: {time_allotment_q2} ms")
    print(f"Context Switch Time: {context_switch_time} ms")
    print("Processes:")
    for process in processes:
        print(process)

if __name__ == "__main__":
    main()
#
'''