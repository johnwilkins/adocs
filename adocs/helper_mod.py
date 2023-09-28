import os
import args_mod
import re

# The module ID is base for the anchor tag and the file name.
# Takes the title, so we can reuse with renaming.
def get_module_id(title):
    return title.lower().replace(' ', '-')

# The file name might change based upon the project. This
# function allows to extend the file name formats as needed.
def get_filename(title):
    module_id=get_module_id(title)
    if(args_mod.filename_format == "fcc"):
        o_file=args_mod.component_type + \
               "_" + args_mod.iargs.type + \
               "_" + module_id + ".adoc"
        
    elif(args_mod.filename_format == "ocp"):      
        o_file=args_mod.component_type + \
            "-" + module_id + ".adoc"
    
    return o_file

# Once we have the file name, add the absolute path.
def get_full_fname(title):
    mod_path = os.path.join(args_mod.repo_dir,
                            args_mod.module_dir,
                            get_filename(title))
    return mod_path

# A function to get the module title, since it might be optional.
def get_module_title(title):
    if getattr(args_mod.iargs, 'optional', None) and args_mod.iargs.optional == True:
        mod_title = "Optional: " + title
    else:
        mod_title = title
    return mod_title

# A function to get the full assembly filename path.
def get_assembly_fname():
    assembly_fname = os.path.join(args_mod.repo_dir + \
                                  args_mod.assembly_dir, \
                                  args_mod.iargs.assembly_file
                                  )
    return assembly_fname

# Gets the assembly include.
def get_assembly_include(title):
    assembly_include = "include::" + \
                        args_mod.module_dir + get_filename(title) + \
                        "[leveloffset=+" + args_mod.iargs.level + "]" 
    return assembly_include


# Gets an xref to a module.
def get_xref(title, assembly_fname):

    include_pattern=":context: [a-z-]+"
    if os.path.exists(assembly_fname):
        with open(assembly_fname) as f:
            contents = f.readlines()
            for line in contents:
                if re.search(include_pattern, line):
                    context=line.replace(":context: ", "")
    my_xref = "xref:" + \
                args_mod.assembly_dir + args_mod.iargs.assembly_file + \
                 "#" + get_module_id(title) + "_" + context + "[" + title + "]"
    return my_xref

# Gets the content type
def get_content_type(c_type):
    content_types = {
        'proc': 'PROCEDURE',
        'con': 'CONCEPT',
        'ref': 'REFERENCE',
        'assembly': 'ASSEMBLY'
    }

    # Check if the input argument exists as a key in the content_types dictionary
    # If it does, return its corresponding value fully spelled out in uppercase
    # If it doesn't, return None
    return content_types.get(c_type.lower(), None)