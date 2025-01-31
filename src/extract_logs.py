import sys
import os


def extract_logs(date, log_file="test_logs.log.txt"):
    output_dir = "output"
    output_file = os.path.join(output_dir, f"output_{date}.txt")

    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(log_file, "r", encoding="utf-8") as file, open(output_file, "w", encoding="utf-8") as out_file:
            for line in file:
                if line.startswith(date):  # Efficient date filtering
                    out_file.write(line)

        print(f"Logs for {date} saved in {output_file}")
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)

    date_input = sys.argv[1]
    extract_logs(date_input)
