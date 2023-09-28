# This module defines a Doc class and methods
# that end users can execute to create, rename,
# delete, and link to docs.

import os
import args_mod
import helper_mod
from jinja2 import Environment, FileSystemLoader
import re
import subprocess

class Doc:
    def __init__(self):
        # Set up the template environment and ensure that we
        # don't propagate any uncaught exceptions, as that isn't
        # fun for end user.
        try:
            env = Environment(loader=FileSystemLoader(args_mod.template_dir))
            self.module_tmpl = env.get_template('module_template.adoc')
            self.assembly_tmpl = env.get_template('assembly_template.adoc')
        except Exception as e:
            print("Error: Something is up with getting the templates: ")
            print(e)
            print("Make sure the path is set correctly in adoc.ini.")
            exit()

        # Get the required values from our helper methods.
        self.title=args_mod.iargs.module_title
        self.module_id=helper_mod.get_module_id(self.title)
        self.module_title=helper_mod.get_module_title(self.title)
        self.module_fname=helper_mod.get_full_fname(self.title)
        self.assembly_dir=args_mod.assembly_dir
        self.assembly_fname=helper_mod.get_assembly_fname()
        self.assembly_inc=helper_mod.get_assembly_include(self.title)
        self.content_type=helper_mod.get_content_type(args_mod.iargs.type.upper())

        '''
        #Print statements for debugging
        print("title="+self.title)
        print("module_id="+self.module_id)
        print("module_title="+self.module_title)
        print("module_fname="+self.module_fname)
        print("assembly_dir="+self.assembly_dir)
        print("assembly_fname="+self.assembly_fname)
        print("assembly_inc="+self.assembly_inc)
        '''

    # This function creates a module with CLI argument inputs and a template.
    # It also adds an include statement in the required assembly file.
    def create(self):

        if not os.path.exists(self.assembly_fname):
            print("\nThis assembly name does not exist. Should I create it?")
            create_assembly=input("Y/N\n").upper()
            if create_assembly == "N":
                print("\nCheck the assembly file name and try again.")
                exit()

        print("\nCreating a new module and include statement.\n")

        # Render the content with the module template.
        mod_txt = self.module_tmpl.render(asd=self.assembly_dir,
                                          af=args_mod.iargs.assembly_file,
                                          content_type=self.content_type,
                                          anchor=self.module_id,
                                          mod_title=self.module_title,
                                          lorem=args_mod.iargs.lorem)

        if os.path.exists(self.module_fname):
            print("This module already exists. \nDo you want to overwrite it?")
            overwrite=input("Y/N\n").upper()
            if overwrite == "Y":
                with open(self.module_fname, 'w') as mod_file:
                        mod_file.write(mod_txt)
                        print("Module overwritten. The include is already in the assembly. Skipping.")
                        exit()
            else:
                print("Preserving the existing module. Bye!")
                exit()
        else:
            try:
                with open(self.module_fname, 'w') as mod_file:
                    mod_file.write(mod_txt)
            except FileNotFoundError as e:
                print("Error: I couldn't find the destination path. There is likely an error "+\
                      "\nin the path specified in the configuration file or in an option you passed in. \n" +\
                      "Fix the error and try again.\n")
                exit()

        # Check to see if the assembly exists. If it does, append the assembly_include to
        # the existing assembly. If it doesn't exist, create the assembly from the 
        # template, prompting the user for the required values.
        if os.path.exists(self.assembly_fname):
            with open(self.assembly_fname, 'a') as afname:
                afname.write(self.assembly_inc + "\n\n")
        else:
            assembly_title=input("Enter the assembly title: \n")
            assembly_anchor=assembly_title.lower().replace(' ', '-')
            assembly_intro=input("Enter a brief abstract: ")

            assembly_txt=self.assembly_tmpl.render(anchor=assembly_anchor,
                                                   ast=assembly_title,
                                                   context=assembly_anchor,
                                                   intro=assembly_intro,
                                                   lorem=args_mod.iargs.lorem,
                                                   include_text=self.assembly_inc + "\n\n")
            #print(assembly_txt)

            try:
                with open(self.assembly_fname, 'w') as afname:
                    afname.write(assembly_txt)
            except FileNotFoundError as e:
                print("Error: I couldn't find the destination path. There is likely an error "+\
                      "\nin the path specified in the adoc.conf file or in an option you passed in. \n" +\
                      "Fix the error and try again. You can overwrite the module.\n")
                exit()
            print("include::" + self.assembly_dir + args_mod.iargs.assembly_file + "[leveloffset=+1]\n")

        print(helper_mod.get_xref(self.title, self.assembly_fname) + "\n")
        #print("Assembly path: " + self.assembly_fname)
        #print("Module path: " + self.module_fname + "\n")
        
        if args_mod.open_in_editor:
            subprocess.Popen([args_mod.editor_cli, self.assembly_fname])
            subprocess.Popen([args_mod.editor_cli, self.module_fname])

    # This function renames a module title, anchor tag, file name and include. It will 
    # strip off "Optional: " if -o isn't specified.
    def rename(self):
        print("\n Renaming a module and it's include statement.\n")

        # Make sure the assembly exists before trying to rename the module. Otherwise,
        # you might end up with a broken include statement in the asssembly.
        if not os.path.exists(self.assembly_fname):
            print("Sorry. I couldn't find an assembly file by that name.")
            exit()


        # set up the old title variables.
        old_title = args_mod.iargs.old_title
        old_file_name = helper_mod.get_full_fname(old_title)
        old_module_id=helper_mod.get_module_id(old_title)
        old_assembly_inc=helper_mod.get_assembly_include(old_title)

        if os.path.exists(old_file_name):
            with open(old_file_name, 'r') as f:
                module_data=f.read()
        else:
            print("Sorry. I couldn't find a module file by that name.")
            exit()        

        modified_data = module_data.replace(old_module_id, self.module_id)
        #Remove "Optional: " from the title. The new one will have it if -o is specified.
        module_data = modified_data.replace("Optional: ", "")
        modified_data = module_data.replace(old_title, self.module_title)

        with open(self.module_fname, 'w') as f:
            f.write(modified_data)        

        os.remove(old_file_name)

        with open(self.assembly_fname, 'r') as f:
            assembly_data=f.read()

        modified_assembly_data = assembly_data.replace(old_assembly_inc, self.assembly_inc)

        with open(self.assembly_fname, 'w') as f:
            f.write(modified_assembly_data)


        if args_mod.open_in_editor:
            subprocess.Popen([args_mod.editor_cli, self.assembly_fname])
            subprocess.Popen([args_mod.editor_cli, self.module_fname])


        #print("Assembly path: " + self.assembly_fname)
        #print("Module path: " + self.module_fname + "\n")


    # This function deletes a module and its include statement. 
    # It will prompt you again to ensure you don't delete the file inadvertantly.
    def delete(self):
        print("\nDeleting a module and include statement.\n")

        # Ensure the assembly file exists before deleting modules so that we don't end up with a broken
        # include statement.
        if not os.path.exists(self.assembly_fname):
            print("Sorry. I couldn't find an assembly file by that name.")
            print("I was looking for: " + self.assembly_fname)
            print("Check that the path and the filename are correct. \n")
            exit()


        #Ensure the module exists before deleting it.
        if os.path.exists(self.module_fname):
            print("\nDo you want to delete this file: \n" + self.module_fname + "?")
            overwrite=input("Y/N\n").upper()
            if overwrite == "Y":
                os.remove(self.module_fname)
            else:
                print("Ok. Keeping the file.")
                exit()
        else:
            print("Sorry. I couldn't find a module file by that name.")
            print("I was looking for: " + self.module_fname)
            print("If it's a different component type, use -t or --type with either 'proc', 'con', 'ref', or 'assembly' to override it.")
            exit()        

        #Since we might have multiple offset levels, we need a regex to match the levels.
        include_string=self.assembly_inc
        trimmed_include=include_string[:-16]
        include_pattern=trimmed_include + "\[leveloffset=\+[0-9]\]"

        with open(self.assembly_fname, 'r') as f:
            contents = f.readlines()

        with open(self.assembly_fname, 'w') as f:
            for line in contents:
                if not re.search(include_pattern, line):
                    f.write(line)


    def xref(self):
        print("\nCreating a cross-reference to a module.")

        print("\n" + helper_mod.get_xref(self.title, self.assembly_fname) + "\n")

        print("When incorporating an xref in a different directory from your assemblies,\nyou may need to adjust the relative path. (e.g., ../../)\n")

