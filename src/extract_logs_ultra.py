import sys
import os
import mmap
import threading


def binary_search_first_occurrence(file_path, date):
    """Binary search to find the first occurrence of the date in the log file using mmap."""
    with open(file_path, "r", encoding="utf-8") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        left, right = 0, len(mm)

        while left < right:
            mid = (left + right) // 2

            # Move to a new line
            while mid > 0 and mm[mid] != ord("\n"):
                mid -= 1
            if mid > 0:
                mid += 1  # Move to the start of the next line

            pos = mid
            line = mm[pos:mm.find(b"\n", pos)].decode(errors="ignore")

            if not line:
                right = mid
                continue

            log_date = line[:10]  # Extract YYYY-MM-DD

            if log_date < date:
                left = pos
            else:
                right = mid

        return left  # Position of first occurrence


def extract_logs_worker(file_path, date, start_pos, end_pos, output_file):
    """Worker function to extract logs from a memory-mapped file in chunks."""
    with open(file_path, "r", encoding="utf-8") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        with open(output_file, "a", encoding="utf-8") as out_f:
            pos = start_pos
            while pos < end_pos:
                newline_pos = mm.find(b"\n", pos)
                if newline_pos == -1 or newline_pos >= end_pos:
                    break  # Stop at the chunk boundary

                line = mm[pos:newline_pos].decode(errors="ignore")
                if line.startswith(date):
                    out_f.write(line + "\n")
                elif line[:10] > date:
                    break  # Stop once we move past the date

                pos = newline_pos + 1  # Move to next line


def extract_logs(date, file_path="logs_2024.log", num_threads=4):
    """Extract logs for the given date using mmap and multi-threading."""
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
                                  args=(file_path, date, chunk_start, chunk_end, output_file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Logs for {date} saved in {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs_ultra.py <YYYY-MM-DD>")
        sys.exit(1)

    date = sys.argv[1]

    extract_logs(date)
