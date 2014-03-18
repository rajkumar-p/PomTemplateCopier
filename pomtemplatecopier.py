import argparse
import Queue
import os.path
import re

# Helper functions
def writeToFile(file_handle, string_to_be_written):
    """
    Helper to write to file
    input: file_handle, string_to_be_written
    """
    file_handle.write(string_to_be_written)

def writeLineToFile(file_handle, string_to_be_written):
    """
    Helper to write line to file
    input: file_handle, string_to_be_written
    """
    writeToFile(file_handle, string_to_be_written)
    writeToFile(file_handle, "\n")

def printDirBanner(file_handle, current_dir):
    """
    Helper to print the banner around the directory name
    input: file_handle, current_dir
    """
    writeLineToFile(file_handle, len(current_dir) * "-")
    writeLineToFile(file_handle, current_dir)
    writeLineToFile(file_handle, len(current_dir) * "-")

def fileExists(filename):
    """
    Helper to check if a file exists
    input: filename
    """
    try:
        with open(filename):
            return True
    except IOError:
        return False

# Parser for the command line arguments
arguments_parser = argparse.ArgumentParser()

# Add the arguments to the checked
arguments_parser.add_argument("-v", "--version",
                              type=str,
                              help="Version that needs to go in place of ${temp.version}")

arguments_parser.add_argument("-f", "--file",
                              action="store_true",
                              help="Change only for the directories given in the file")

arguments_parser.add_argument("-start", "--start_dir",
                              type=str,
                              help="The start directory from where to start the check")

arguments_parser.add_argument("-stop", "--stop_dir",
                              type=str,
                              help="The directory from where to stop processing it and its children")

# Parse the arguments passed
commandline_arguments = arguments_parser.parse()

# Error messages used
error_msg_both_not_present = "Pom and pom template not present."
error_msg_pom_not_present = "Pom not present."
error_msg_pom_template_not_present = "Pom template not present."

stopping_at_dir = "STOPPING AT DIR - {0}."

version = ""
starting_dir = ""
stop_dir = ""

# Directories Q
directories = Queue.Queue()

# Flag to control the recursive behavior of the program
recurse = True

if commandline_arguments.version:
    version = commandline_arguments.version
else:
    print "Version cannot be empty. Type -h for script usage"
    exit(0)

# If a file is passed, change only in the directories in the file
if commandline_arguments.file:
    recurse = False
    try:
        dir_fh = open(commandline_arguments.file, "r")
        lines = dir_fh.readlines()

        for line in lines:
            directories.put(line.strip())

        dir_fh.close()

    except IOError:
        print "Error. Cannot open file passed."
        exit(0)

if recurse:
    if commandline_arguments.start_dir:
        starting_dir = commandline_arguments
    else:
        starting_dir = "."

    if commandline_arguments.stop_dir:
        stop_dir = commandline_arguments.stop_dir
    else:
        stop_dir = "XXXXXXXXXX"

    directories.put(os.path.abspath(starting_dir))

# Logger to be used in the program
logger = open("ptc_session.log", "w")

# Process every directory in the Q
while not directories.empty():
    current_dir = directories.get()

    # Process other directories recursively only of the flag is set
    if recurse:
        if current_dir == stop_dir:
            writeLineToFile(logger, stopping_at_dir.format(current_dir))
            continue

        # Push the child directories into the directories Q
        for d in [os.path.join(current_dir, directory)
                        for directory in os.listdir(current_dir)
                            if os.path.isdir(current_dir + os.path.sep + directory)]:
            directories.put(d)

    # Pom and pom.template files
    pom_file = current_dir + os.path.sep + "pom.xml"
    pom_template_file = current_dir + os.path.sep + "pom.template.xml"

    printDirBanner(logger, current_dir)

    if not fileExists(pom_template_file):
        writeLineToFile(logger, error_msg_pom_template_not_present)
        writeLineToFile("")
        continue

    pom_fh = open(pom_file, "w")
    pom_template_fh = open(pom_template_file, "r")

    pom_template_contents = pom_fh.read()

    # Change the ${temp.version} in pom_template
    p = re.compile(r"\$\{temp\.version\}")
    pom_template_subs_contents = p.sub(commandline_arguments.version, pom_template_contents)

    pom_fh.write(pom_template_subs_contents)

    # Close the file handles
    pom_fh.close()
    pom_template_fh.close()

logger.close()
