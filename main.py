import sys

CHUNK_SIZE = 1
BYTES_PER_LINE = 10
NUMBER_PADDING = 25

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

lines_to_print = -1

if len(sys.argv) != 3:
    print("Usage: must include exactly two files to compare")
file_a_path = sys.argv[1]
file_b_path = sys.argv[2]

if len(sys.argv) > 3:
    lines_to_print = int(sys.argv[3])

with open(file_a_path, "rb") as file_a, open(file_b_path, "rb") as file_b:
    file_a_bytes = file_a.read(CHUNK_SIZE)
    file_b_bytes = file_b.read(CHUNK_SIZE)

    bytes_read = 0

    file_a_line_buffer = []
    file_b_line_buffer = []
    while file_a_bytes or file_b_bytes:
        bytes_read += 1

        file_a_bytes = file_a.read(CHUNK_SIZE)
        file_b_bytes = file_b.read(CHUNK_SIZE)

        if file_a_bytes == file_b_bytes:
            file_a_line_buffer.append(file_a_bytes.hex())
            file_b_line_buffer.append(file_b_bytes.hex())
        else:
            if not file_a_bytes:
                file_a_line_buffer.append(FAIL + "--" + ENDC)
            else:
                file_a_line_buffer.append(FAIL + file_a_bytes.hex() + ENDC)

            if not file_b_bytes:
                file_b_line_buffer.append(FAIL + "--" + ENDC)
            else:
                file_b_line_buffer.append(FAIL + file_b_bytes.hex() + ENDC)

        if bytes_read % BYTES_PER_LINE == 0:
            file_output = "{}{}{:{}}".format(OKBLUE, str(bytes_read - BYTES_PER_LINE), ENDC,
                                             NUMBER_PADDING - len(str(bytes_read - BYTES_PER_LINE)))
            file_output += " ".join(file_a_line_buffer) + "\t\t" + " ".join(file_b_line_buffer)
            file_a_line_buffer = []
            file_b_line_buffer = []
            print(file_output)

            lines_to_print -= 1
            if lines_to_print == 0:
                break
