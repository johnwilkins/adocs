# adocs

The `adocs` tool creates asciidoc modules and generates includes for assemblies using the [modular documentation](https://github.com/redhat-documentation/modular-docs) standards developed at [Red Hat](https://github.com/redhat-documentation). See the [Modular Documentation Reference Guide](https://redhat-documentation.github.io/modular-docs/) to learn more about modular documentation. 

Writing documentation in modules makes it much easier for large teams to work on documentation projects. However, it also requires some repetitive steps that writers might find tedious. This tool aims to streamline the process of creating modules and including them in assemblies. It supports four commands: 

* create
* rename
* delete
* xref

# The create command

The `create` command:

* Determines if the module name is already in use, so you don't overwrite existing modules inadvertantly.
* Generates the module file
* Adds a header comment in the module indicating which assembly includes the module
* Adds a `:content-type:` tag to the module
* Adds an anchor tag to the module
* Adds a heading with the specified module name
* Generates the module file name in the specified format
* Saves the module file
* Generates the assembly if it doesn't exist and prints an include statement for the assembly
* Adds/appends an include statement to the assembly file 
* Prints the paths to the assembly and module

The `create` command also has a few additional options: 

* `-o` or `--optional` prepends the module title with "Optional: ", which you can specify if the module is optional. 
* `-l` or `--level` allows you to set the level offset of the include statement. By default, it is `1`. Level offsets are the preferred method of nesting modules, rather than nesting assemblies. 
* `--lorem` will create the module with dummy "lorem ipsum" text.

# The rename command

The `rename` command:

* Renames the anchor tag.
* Renames the module title, removing "Optional: " if it's in the title and the `-o` or `--optional` flag isn't specified. 
* Renames the module file.
* Updates the include statement in the assembly. 

If the level offset is not `1`, you must specify the `-l` or `--level` option and specify the level.


# The delete command

The `delete` command:

* Prompts you if you want to delete the module
* Deletes the module
* Deletes the include statement from the assembly


# The xref command

The `xref` command creates a cross reference, specifying the assembly, the anchor tag of the module with the assembly context incorporated.

