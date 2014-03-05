import argparse

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

arguments_parser.add_argument("-ntc", "--node_to_change",
                              type=str,
                              help="The XML node to be changed. If not given, the pom template is just copied as is")

arguments_parser.add_argument("-nv", "--new_value",
                              type=str,
                              help="The new value to be substituted. If no value is given, empty string is used")

arguments_parser.add_argument("-ct", "--change_type",
                              type=str,
                              help="0 denotes a tag change and 1 denotes a text change. 1 is the default value")

arguments_parser.add_argument("-ns", "--namespace",
                              type=str,
                              help="The namespace of the node to be changed. If not given, the root node's namespace is taken")
