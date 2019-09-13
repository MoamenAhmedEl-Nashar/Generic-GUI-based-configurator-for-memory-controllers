[![Codacy Badge](https://api.codacy.com/project/badge/Grade/476507473cc840d2a9913ba67ef21223)](https://www.codacy.com/manual/moamen.ahmed.n1/Generic-GUI-based-configurator-for-memory-controllers?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers&amp;utm_campaign=Badge_Grade)

# Generic-GUI-based-configurator-for-memory-controllers
## GIF 
![gif](https://github.com/MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers/blob/master/new_demo_gif.gif)
## Introduction
The goal of this GUI program is to make the process of change parameters
in test benches easily, it parses the verilog input file, then extracts
parameters for each module instance. Also, it parses \``include` and \``define`
to allow the user to control \``ifdef` that controls module instances or
controls code within them.

## How it works
If you choose design file option, then click upload:
  -	Click upload
  -	Choose file with any extension
  -	The tool searches input code to get \``ifdefs`
  - The tool saves all identifiers that comes after \``ifdefs` and puts them in defines dictionary.
  -	The tool searches for \``defines` and modifies the defines dictionary with 1 for all defined identifiers.
  -	The tool shows all \``ifdef` identifiers with check buttons on the window as follows:
![defines example](https://github.com/MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers/blob/master/defines.png)
  
  -	If there are nothing to show, the tool says “no defines found” as follows:![no defines found](https://github.com/MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers/blob/master/no_defines.png)
  - If you click save:
    -	The tool saves the defines values from the user and updates the defines dictionary
    -	The tool opens the input file and modifies defines only. 
  - If you click arrow to show parameters:
  -	The tool modifies parsers to ignore undefined sections (\``ifdef` “not defined identifier”)
  -	The tool parses the input file to get any parameter declaration
  - The tool shows all parameters on the window as follows:
  ![parameters example](https://github.com/MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers/blob/master/parameters.png)
  -	If there are nothing to show, the tool says “There are no parameters” as follows:
  ![no parameters found](https://github.com/MoamenAhmedEl-Nashar/Generic-GUI-based-configurator-for-memory-controllers/blob/master/no_parameters.png)
  - If you click save:
  - The tool saves the defines values from the user and updates the defines dictionary.
  -	The tool saves the parameters values from the user and updates the parameters dictionary.
  -	The tool opens the input file and modifies it. 



If you choose test file option, then click upload:
  -	Click upload
  -	Choose file with any extension
  -	The tool searches input code to get \``ifdefs`
  -	The tool saves all identifiers that comes after \``ifdefs` and puts them in defines dictionary.
  -	The tool searches for \``defines` and modify the defines dictionary with 1 for all defined identifiers.
  -	The tool shows all \``ifdef` identifiers with check buttons on the window
  -	If there are nothing to show, the tool says “no defines found”
  - If you click save:
    - The tool saves the defines values from the user and updates the defines dictionary
    - The tool opens the input file and modifies defines only. 
  - If you click arrow to show parameters:
    -	The tool modifies parsers to ignore undefined sections (\``ifdef` “not defined identifier”)
    -	The tool parses the input file to get any parameter declaration
    -	The tool parses the input file to get one module instance
    -	The tool saves the module name and module parameter names
    -	The tool shows “module: “module name
    -	The tool parser the included file (with extension “.v”)
    -	The tool shows module parameters names (from the input file and the included file) on the window
    -	If there are nothing to show, the tool says “There are no parameters”
  - If you click save:
    -	The tool saves the defines values from the user and updates the defines dictionary.
    -	The tool saves the parameters values from the user and updates the parameters dictionary.
    -	The tool opens the input file and modifies it. 
    
## How to use
   - open the executable file.
   - choose type of the file (design or test).
   - change `defines`.
   - click on the arrow.
   - change `parameters`.
   - click save to apply changes on the same file.
   - click settings to adjust settings of run simulation.
   - click compile design file, and choose the design file for the test file.
   - click run.
   
## Notes
   - add Questa executables to system path.
   - you don't have to compile design files for each run if you compiled it before in the same directory that 
   `work` folder exists.

## Features
   - The tool detects the module name of the uploaded test file, and compile it autmatically to apply changes.
   
