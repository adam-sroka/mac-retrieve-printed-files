# TODO check and handle python version in the os
# TODO handle different files than just PDFs
# TODO retrieve more control file fields

import os
from distutils.dir_util import copy_tree, remove_tree
from datetime import datetime

PRINTED_FILES_DIRECTORY = "/var/spool/cups"
CONTROL_FILE_FIELD_TYPES = {
    "job-id": "int",
    "job-originating-user-name": "str",
    "time-at-creation": "int",
    "job-name": "str",
}


def find_string_end(start, control_file_bytes):
    for i, single_byte in enumerate(control_file_bytes[start:]):
        if single_byte == 0:
            return start + i - 1
    return len(control_file_bytes) - 1


def decode_string(position, control_file_bytes):
    position += 2
    end = find_string_end(position, control_file_bytes)
    return control_file_bytes[position:end].decode()


def decode_int(position, control_file_bytes):
    position += 2
    return int.from_bytes(control_file_bytes[position : position + 4], byteorder="big")


def does_field_name_match(field_name, current_index, control_file_bytes):
    field_name_bytes = field_name.encode()
    does_other_field_name_continue = (
        current_index >= 3 and control_file_bytes[current_index - 2] != 0
    )
    field_name_runs_over_end = current_index + len(field_name_bytes) > len(
        control_file_bytes
    )
    if does_other_field_name_continue or field_name_runs_over_end:
        return False
    return (
        field_name_bytes
        == control_file_bytes[current_index : current_index + len(field_name_bytes)]
    )


def decode_control_file(control_file, control_file_field_types, convert_timestamp=True):
    decoded_control_file_fields = dict()
    decoded_control_file = control_file.read()
    for index in range(len(decoded_control_file)):
        for field_name, field_type in control_file_field_types.items():
            if does_field_name_match(field_name, index, decoded_control_file):
                if field_type == "str":
                    decoded_control_file_fields[field_name] = decode_string(
                        index + len(field_name), decoded_control_file
                    )
                elif field_type == "int":
                    decoded_control_file_fields[field_name] = decode_int(
                        index + len(field_name), decoded_control_file
                    )
    # TODO handle more timestamp fields than time-at-creation
    if convert_timestamp:
        decoded_control_file_fields["time-at-creation"] = datetime.fromtimestamp(
            decoded_control_file_fields["time-at-creation"]
        ).strftime("%Y-%m-%d_%H:%M:%S")
    return decoded_control_file_fields


def proceed_only_if_running_as_root():
    is_running_as_root = os.geteuid() == 0
    if not is_running_as_root:
        print(
            'ERROR: please run this file as "sudo python retrieve_printed_files.py", type your password, and press enter.'
        )
        exit()


def stringify_decoded_fields(decoded_fields, control_file_field_types):
    output = ""
    for field_name in control_file_field_types.keys():
        output += str(decoded_fields[field_name])
        output += ","
    return output


if __name__ == "__main__":
    proceed_only_if_running_as_root()
    working_directory = os.getcwd()
    retrieved_files_directory = working_directory + "/retrieved-printed-files"
    copy_tree(PRINTED_FILES_DIRECTORY, retrieved_files_directory)

    other_directories = ["cache", "tmp"]
    for other_directory in other_directories:
        path_to_directory = retrieved_files_directory + "/" + other_directory
        if os.path.exists(path_to_directory):
            remove_tree(path_to_directory)

    retrieved_files_names = os.listdir(retrieved_files_directory)
    retrieved_files_names.sort()  # to have the log file in ascending id order
    retrieved_control_file_names = [
        file_name for file_name in retrieved_files_names if file_name[0] == "c"
    ]
    retrieved_data_file_names = [
        file_name for file_name in retrieved_files_names if file_name[0] == "d"
    ]

    print(
        f"Found {len(retrieved_data_file_names)} previously printed files out of {len(retrieved_control_file_names)} files ever printed."
    )
    print("Retrieving files...")

    log_file_path = retrieved_files_directory + "/all_retrieved_files_data.csv"
    with open(log_file_path, "w") as log_file:
        log_file.write(
            "job-id,job-originating-user-name,time-at-creation,job-name,file-available\n"
        )  # TODO generalise
        for file_name in retrieved_control_file_names:
            control_file_path = retrieved_files_directory + "/" + file_name
            with open(control_file_path, "rb") as control_file:
                decoded_fields = decode_control_file(
                    control_file, CONTROL_FILE_FIELD_TYPES, convert_timestamp=True
                )
            log_file_line = stringify_decoded_fields(
                decoded_fields, CONTROL_FILE_FIELD_TYPES
            )
            corresponding_data_file_name = "d" + file_name[1:] + "-001"
            is_data_file_available = (
                corresponding_data_file_name in retrieved_data_file_names
            )
            if is_data_file_available:
                log_file_line += "yes\n"
                data_file_path = (
                    retrieved_files_directory + "/" + corresponding_data_file_name
                )
                data_file_corrected_path = (
                    retrieved_files_directory
                    + "/"
                    + str(decoded_fields["job-id"])
                    + "_"
                    + decoded_fields["job-name"]
                )
                # TODO generalise for other file types
                if data_file_corrected_path[-4:] != ".pdf":
                    data_file_corrected_path += ".pdf"
            else:
                log_file_line += "no\n"
            log_file.write(log_file_line)
            os.remove(control_file_path)

    print('Done! See the files in the folder "retrieved-printed-files".')
