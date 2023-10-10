import configparser
import argparse
import re
import os
import pkg_resources

# Users may work with many repositories, or with many assembly 
# directories in the same repo. This means that it will
# likely be a nicer user experience if they can change 
# configuration files easily. The adoc.ini file tells the
# program which configuration file to use. It also specifies
# the template folder.

iniParser = configparser.RawConfigParser()


# Expand the user's home directory
ini_file_path = os.path.expanduser('~/adocs/adoc.ini')

try:
    with open(ini_file_path, 'r') as ini_file:
        iniParser.read_file(ini_file)
        found = True
except FileNotFoundError:
    found = False
    print("\nError: I did not find the adoc.ini file.")
    exit()

adoc_conf_file = os.path.expanduser(iniParser.get('adoc', 'adoc_conf_file'))
template_directory = os.path.expanduser(iniParser.get('adoc', 'template_dir'))
editor_cli=iniParser.get('adoc', 'editor_cli')

try:
    open_in_editor=iniParser.getboolean('adoc', 'open_in_editor')
except ValueError:
    print("The value for key \"open_in_editor\" in the adoc.ini file is not a boolean. Use True or False.")
    exit()

# Some arguments have default values that are parsed from the 
# configuration file.
# Create a config file parser.
configParser = configparser.RawConfigParser()
try:
    configParser.read_file(open(adoc_conf_file))
except FileNotFoundError:
    print("\nError: I did not find the configuration file referenced in the adoc.ini file.\n")
    exit()
configParser.read(adoc_conf_file)

try:
    component_type = configParser.get('adocs-conf', 'component_type')
    repo_dir = configParser.get('adocs-conf', 'repo_dir')
    assembly_dir = configParser.get('adocs-conf', 'assembly_dir')
    module_dir = configParser.get('adocs-conf', 'module_dir')
    template_dir = template_directory
    filename_format = configParser.get('file-format', 'filename_format')
except Exception as e:
    print("\nError: There is an error parsing the arguments.")
    print(e)
    print("\n")
    exit()

if not re.match(r'^\/.*\/$', repo_dir):
    print("Error: The value of 'repo_dir' must be an absolute path beginning and ending with '/'.")
    exit()

if not re.match(r'^(?!\/).*\/$', assembly_dir):
    print("Error: The assembly directory must end with a forward slash and not start with one.")
    exit()

if not re.match(r'^(?!\/).*\/$', module_dir):
    print("Error: The module directory must end with a forward slash and not start with one.")
    exit()


parser = argparse.ArgumentParser(
    prog="\n\nadocs",
    description="Creates, renames, deletes or xrefs modules. \
    If there is no assembly for the module, it can create one. \
    Specify the module title in quotes. Specify the assembly file name ending in .adoc.\
    Retrieves default values from the configuration file.",
    epilog="© John Wilkins 2023. jowilkin@redhat.com",
)



subparsers = parser.add_subparsers()

# Define a subparser for the "create" command
create_parser = subparsers.add_parser('create', help="Create a module. For usage: adocs create -h")
create_parser.add_argument('module_title', metavar='\"title\"', type=str, help='The title of the new module in quotes.')
create_parser.add_argument('assembly_file', metavar='assembly_fname.adoc', type=str, help='The name of the assembly file.')
create_parser.add_argument("-o", "--optional",
                    help="Prepends \"Optional: \"\n in the module title.",
                    action='store_true'
                    )
create_parser.add_argument("-l", "--level",
                           help="The level offset for the assembly's include directive. Default is 1.",
                           default="1", choices=['1','2','3'])
create_parser.add_argument("--lorem",
                        help="Adds lorem ipsum placeholder text.",
                        action='store_true')
create_parser.add_argument("-t", "--type", 
                    help="The module type. The options are 'proc', 'con' 'ref', and 'assembly'. The default value is 'proc'.", 
                    choices=['proc','con','ref','assembly'],
                    default="proc", 
                    action="store"
                    )
create_parser.set_defaults(command='create')


# Define a subparser for the "delete" command
delete_parser = subparsers.add_parser('delete', help="Delete a module. For usage: adocs delete -h")
delete_parser.add_argument('module_title', metavar='\"title\"', type=str, help='The title of the module to delete in quotes.')
delete_parser.add_argument('assembly_file', metavar='assembly_fname.adoc', type=str, help='The name of the assembly file.')
delete_parser.add_argument("-t", "--type", 
                    help="The module type. The options are 'proc', 'con' 'ref', and 'assembly'. The default value is 'proc'.", 
                    choices=['proc','con','ref','assembly'],
                    default="proc", 
                    action="store"
                    )
delete_parser.add_argument("-l", "--level",
                           help="The level offset for the assembly's include directive. You don't need to specify it.",
                           default="1", choices=['1','2','3'])
delete_parser.set_defaults(command='delete')

# Define a subparser for the "rename" command
rename_parser = subparsers.add_parser('rename', help="Rename a module. For usage: adocs rename -h")
rename_parser.add_argument('old_title', metavar='\"old title\"', type=str, help='The old title of the module to rename in quotes.')
rename_parser.add_argument('module_title', metavar='\"new title\"', type=str, help='The new title of the module to rename in quotes.')
rename_parser.add_argument('assembly_file', metavar='assembly_fname.adoc', type=str, help='The name of the assembly file.')
rename_parser.add_argument("-o", "--optional",
                    help="Prepends \"Optional: \" in the module title if it doesn't exist. If not specified, it will strip \"Optional: \" from the title if it exists.",
                    action='store_true')
rename_parser.add_argument("-l", "--level",
                           help="The level offset for assembly includes. Default is 1.",
                           default="1", choices=['1','2','3'])
rename_parser.add_argument("-t", "--type", 
                    help="The module type. The options are 'proc', 'con' 'ref', and 'assembly'. The default value is 'proc'.", 
                    choices=['proc','con','ref','assembly'],
                    default="proc", 
                    action="store"
                    )
rename_parser.set_defaults(command='rename')


# Define a subparser for the "xref" command
xref_parser = subparsers.add_parser('xref', help="Cross-reference a module. For usage: adocs xref -h")
xref_parser.add_argument('module_title', metavar='\"title\"', type=str, help='The title of the module to xref in quotes.')
xref_parser.add_argument('assembly_file', metavar='assembly_fname.adoc', type=str, help='The name of the assembly file.')
xref_parser.add_argument("-t", "--type", 
                    help="The module type. The options are 'proc', 'con' 'ref', and 'assembly'. The default value is 'proc'.", 
                    choices=['proc','con','ref','assembly'],
                    default="proc", 
                    action="store"
                    )
xref_parser.add_argument("-l", "--level",
                           help="Irrelevant for this command.",
                           default="1", choices=['1','2','3'])
xref_parser.set_defaults(command='xref')


iargs = parser.parse_args()


if getattr(iargs, 'assembly', None) and not re.match(r'.+\.adoc$', iargs.assembly):
    print("Error: The assembly file must end in '.adoc'.")
    exit()

print(iargs)