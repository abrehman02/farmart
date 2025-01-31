import sys
import os


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


def extract_logs(date, file_path="logs_2024.log"):
    """Extract logs for the given date using an efficient search."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    output_file = f"{output_dir}/output_{date}.txt"

    with open(file_path, "r", encoding="utf-8") as f, open(output_file, "w", encoding="utf-8") as out_f:
        # Find the first occurrence using binary search
        start_pos = binary_search_first_occurrence(file_path, date)
        f.seek(start_pos)

        # Extract logs for the target date
        for line in f:
            if line.startswith(date):
                out_f.write(line)
            else:
                break  # Stop when the date changes

    print(f"Logs for {date} saved in {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs_binary_search.py <YYYY-MM-DD>")
        sys.exit(1)

    date = sys.argv[1]

    extract_logs(date)
