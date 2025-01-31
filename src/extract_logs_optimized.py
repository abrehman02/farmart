import sys
import os
import threading


def binary_search_first_occurrence(file_path, date):
    """Binary search to find the first occurrence of the date in the log file."""
    with open(file_path, "r", encoding="utf-8") as f:
        left, right = 0, os.path.getsize(file_path)

        while left < right:
            mid = (left + right) // 2

            f.seek(mid)
            f.readline()  # Move to the next full line

            pos = f.tell()
            line = f.readline()

            if not line:
                right = mid  # Reached EOF
                continue

            log_date = line[:10]  # Extract YYYY-MM-DD

            if log_date < date:
                left = pos  # Move right
            else:
                right = mid  # Move left

        return left  # Position of first occurrence


def extract_logs_worker(file_path, start_pos, end_pos, date, output_file):
    """Worker function to extract logs from a given file range."""
    with open(file_path, "r", encoding="utf-8") as f, open(output_file, "a", encoding="utf-8") as out_f:
        f.seek(start_pos)

        while f.tell() < end_pos:
            line = f.readline()
            if line.startswith(date):
                out_f.write(line)
            elif line[:10] > date:
                break  # Stop once we move past the date


def extract_logs(date, file_path="logs_2024.log", num_threads=4):
    """Extract logs for the given date using multi-threaded binary search."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    output_file = f"{output_dir}/output_{date}.txt"

    # Clear the file before writing
    open(output_file, "w").close()

    # Find the first occurrence of the date
    start_pos = binary_search_first_occurrence(file_path, date)

    # Get file size
    file_size = os.path.getsize(file_path)

    # Divide the file into chunks for multi-threading
    chunk_size = (file_size - start_pos) // num_threads
    threads = []

    for i in range(num_threads):
        chunk_start = start_pos + i * chunk_size
        chunk_end = min(start_pos + (i + 1) * chunk_size, file_size)

        thread = threading.Thread(target=extract_logs_worker,
                                  args=(file_path, chunk_start, chunk_end, date, output_file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Logs for {date} saved in {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs_optimized.py <YYYY-MM-DD>")
        sys.exit(1)

    date = sys.argv[1]

    extract_logs(date)
