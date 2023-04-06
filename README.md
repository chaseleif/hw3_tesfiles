### An example Makefile and testing scripts / files for HW3

___
## Makefile

The Makefile given will work on Linux systems  

### Variables which likely need to be modified:

- CC:=gcc <- This sets the compiler to gcc and may need to be g++
- CFLAGS:=-Wall <- This turns some warnings on, may need -std=c99, etc.  
*Can be space-separated. Ensure any flags required are available on Zeus!*  
- SOURCE:=cache\_sim.c <- This is my (single) source file name  
*If you have a multi-source solution you could use a space-separated list here*

### Usage:

Example usage:  
`$ make      # compiles using $CC $CFLAGS $DEBUGFLAGS -o $BIN $SOURCE`  
`$ make test # creates a new $BIN and runs the testOutput.py script`  
  
The .PHONY: line contains actions that always act like targets need updating  
Even if the `$SOURCE` doesn't change, `$BIN` will recompile while in .PHONY  
  
The bottom of the Makefile shows the actions of `$ make test`  
- The `$BIN` is created by compiling the `$SOURCE` using `$CC` with `$CFLAGS`
- The test script files are put into the `test/` directory
- The test script is ran with arguments for test paths and the `$BIN` name

___

## Source

The source file I used was written in C  
Per assignment directions you can use C or C++  
*Ensure your program compiles and works on Zeus*  
___

## Test files

Input files' contents should be as described in the assignment directions  
Each input file will be ran using parameters from expected output filenames  
New files should be named in the same manner as example test files provided  

### Test file naming convention:

> Due to the naming convention of input/output files specified below,  
> input and associated expected output files can be in the same directory.  
> Input files, to be ran and tested, require an associated expected output.  
> The parameters, num\_entries and associativity, are in the output filename.  
  
Input files begin with a prefix, e.g., input, input0, test2  
Expected output files begin with the same prefix and contain the parameters  
- test2
- test2\_numentries\_associativity

### Example:

*Given*:  
- input\_filename = "example5"
  
*Say we found these names that start with "example5"*  
- test case 1: "example5\_4\_1"  <- num\_entries=4, associativity=1
- test case 2: "example5\_8\_2"  <- num\_entries=8, associativity=2
  
*For both of these test cases*:  
- The input file will be used for input
- The parameters are obtained through the expected output's filename
- The expected output is the contents of the expected output file
- Actual program output is compared with the expected output

