# PomTemplateCopier

## Overview
This is a simple utility to replace a pom.xml file with the contents of the pom.template.xml file with specified changes

## Language & Compiler
Python 2.7+

## Usage
<code>python pomtemplatecopier.py -v 205</code>  

The above command runs the program and copies over the pom.template.xml into your pom.xml replacing the ${temp.version} to the given version.

Various paramters can be given to control the run of the program.

-v (--version) - This specifies the version that needs to replace ${temp.version} in the pom.template.xml file when copying over. This param is mandatory
-f (--file) - This options let you input a list of only the directories that the program should act upon. The file needs to be a line seperated list of directories
-start (--start_dir) - The directory where the program is to be run. Default is the present directory
-stop (--stop_dir) - This specifies where the program needs to stop. By default, it will run till the starting directory tree is depleted

<code>python pomtemplatecopier.py -4 -start . -stop src</code>  
<code>python pomtemplatecopier.py -f dir_list.in</code>

## License
Free as in free speech.

## Contributions & Questions
Send me a mail on <raj@diskodev.com> or tweet me at <https://twitter.com/#!/rajkumar_p>