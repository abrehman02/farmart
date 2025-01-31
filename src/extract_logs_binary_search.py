import sys
import os


def find_first_occurrence(log_file, target_date):
    """Binary search to find the first occurrence of logs for a given date."""
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        file_size = os.path.getsize(log_file)
        left, right = 0, file_size
        first_position = -1

        while left <= right:
            mid = (left + right) // 2
            f.seek(mid)

            # Move to the start of a line
            if mid > 0:
                f.readline()

            line = f.readline()
            if not line:
                break  # End of file reached

            if line[:10] >= target_date:
                first_position = mid  # Potential first occurrence
                right = mid - 1  # Search left
            else:
                left = mid + 1  # Search right

        return first_position


def extract_logs(log_file, target_date):
    """Extract all log entries for the given date."""
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found.")
        return

    start_pos = find_first_occurrence(log_file, target_date)
    if start_pos == -1:
        print(f"No logs found for {target_date}.")
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{target_date}.txt")

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f, \
            open(output_file, 'w', encoding='utf-8') as out:

        f.seek(start_pos)  # Start reading from the found position
        found_logs = False

        for line in f:
            if line.startswith(target_date):
                out.write(line)
                found_logs = True
            elif found_logs:
                break  # Stop when logs for the date end

    if found_logs:
        print(f"Logs for {target_date} saved in {output_file}")
    else:
        print(f"No logs found for {target_date}.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
    else:
        extract_logs("test_logs.log.txt", sys.argv[1])
