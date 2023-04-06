### An example Makefile and testing scripts / files for HW3

___

## Source

The source file I used was written in C  
Per assignment directions you can use C or C++  
*Ensure the program compiles and works on Zeus*  
___

## Test files

Input files should be as described in the assignment directions  
Each input file will be ran according to parameters in expected output files  
Files should be named in the same manner as the example test files provided  

### Test file naming convention:

Input files begin with a prefix, e.g., input, input0, test2  
- input  
Expected output files begin with the same prefix and contain the parameters  
- input\_numentries\_associativity  
  
**Example**  
*Given*:  
- input\_filename = "example5"  
*For each name that starts with "example5"*:  
- test case 1: "example5\_4\_1"  <- num\_entries=4, associativity=1  
- test case 2: "example5\_8\_2"  <- num\_entries=8, associativity=2  
  
*For both of these test cases*:  
- The input file would be used for input  
- Each expected output is within the file whose name includes the parameters  
- Each program output is compared with the expected output  

