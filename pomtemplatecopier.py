import argparse
import Queue
import os
import stat
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

def getChildrenDirectories(current_dir):
    return [os.path.join(current_dir, directory)
                    for directory in os.listdir(current_dir)
                        if os.path.isdir(current_dir + os.path.sep + directory)]

def getDirName(current_dir):
    return os.path.basename(current_dir.strip("/\\"))

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
commandline_arguments = arguments_parser.parse_args()

# Error messages used
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

    # Check if the file exists
    if fileExists(commandline_arguments.file):
        dir_fh = open(commandline_arguments.file, "r")
        lines = dir_fh.readline()

        for line in lines:
            directories.put(line.strip())

        dir_fh.close()

if recurse:
    if commandline_arguments.start_dir:
        starting_dir = commandline_arguments.start_dir
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

    # Get the children directories
    children = getChildrenDirectories(current_dir)

    # If stop directory, do not put it into the Q
    for d in children:
        if getDirName(d) != stop_dir:
            directories.put(d)

    # Pom and pom.template files
    pom_file = current_dir + os.path.sep + "pom.temp.xml"
    pom_template_file = current_dir + os.path.sep + "pom.template.xml"

    printDirBanner(logger, current_dir)

    if not fileExists(pom_template_file):
        writeLineToFile(logger, error_msg_pom_template_not_present)
        continue

    # Check if the pom file is read only
    pom_file_read_only = False

    if fileExists(pom_file):
        fileAtt = os.stat(pom_file).st_mode
        pom_file_read_only = not (fileAtt & stat.S_IWRITE)

    # If read only, change the attribute before writing
    if pom_file_read_only:
        os.chmod(pom_file, stat.S_IWRITE)

    pom_fh = open(pom_file, "w")
    pom_template_fh = open(pom_template_file, "r")

    pom_template_contents = pom_template_fh.read()

    # Change the ${temp.version} in pom_template
    p = re.compile(r"\$\{temp\.version\}")
    pom_template_subs_contents = p.sub(commandline_arguments.version, pom_template_contents)

    pom_fh.write(pom_template_subs_contents)

    # Close the file handles
    pom_fh.close()
    pom_template_fh.close()

    # Log success
    writeLineToFile(logger, "Pom.xml replacement done")

logger.close()
