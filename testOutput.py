#! /usr/bin/env python3

'''
    TestOutput - a Python script to test a program
    Copyright (C) 2023  Chase Phelps

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

'''
    Example Makefile usage given a top-level directory and ./assgnX/ subfolders
    ( with the scripts in the top level-dir and Makefile in assgn dir )
    This example usage (and below import) includes the DiffWindow script

$ tail -n14 Makefile
test/cursemenu.py: ../cursemenu.py
	cp $< $@

test/diffwin.py: ../diffwin.py test/cursemenu.py
	cp $< $@

test/testOutput.py: ../testOutput.py
	cp $< $@

test: obj/$(BIN) test/diffwin.py test/testOutput.py
	python3 ./test/testOutput.py \
--testpath test/cases \
--exppath test/exp \
--program $<
'''

import argparse, difflib, re, os, sys
from signal import Signals
from subprocess import Popen, PIPE
sys.dont_write_bytecode = True
try:
  from diffwin import DiffWindow
except ModuleNotFoundError: DiffWindow = None
sys.dont_write_bytecode = False

'''
runproc(cmd, filepos, filename)
  input:
    cmd:     str, command specified to execute
  returns:
    a list: [output, returncode]
    output is a list: [stdout, stderr]
    stdout or stderr are strings and may be empty
    returncode is a numeric value indicating exit code
                = 0: normal exit
                = 1: uncaught exception
                < 0: exception with negative signal number
'''
def runproc(cmd):
  try:
    proc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE,
                  shell = True, universal_newlines = True)
    output = proc.communicate()
    return output, proc.returncode
  except Exception as e:
    print('ERROR (' + sys.argv[0] + ':runproc): ' + str(e))
    return ['',''], 1

'''
dotests(cases, program)
  input:
    cases:   dict, key = case file, value = exp file(s)
      The parameters (num_entries and associativity)
      are taken from the expected output's filename
    program: the program to test
  executes the test for each case in cases
  displays actual output (if possible)
    segmentation faults may suppress output
'''
def dotests(cases, program):
  # Remove any previously generated output file
  if os.path.isfile('cache_sim_output'):
    os.remove('cache_sim_output')
  # For each test input file . . .
  for inFile in cases:
    # inFile could be: "input0"
    # The test name is the filename without any extension
    test = inFile.split('.')[0].split('/')[-1]
    for expfile in cases[inFile]:
      # expfile could be: "input0_1024_8"
      num_entries = expfile.split('_')[-2]
      associativity = expfile.split('_')[-1]
      print('~~~~~\n~~ Test ' + test + ', (num_entries = ' + num_entries + \
            ', associativity = ' + associativity + '):')
      cmd = ' '.join([program, num_entries, associativity, inFile])
      output = runproc(cmd)
      # Handle bad return codes
      if output[1] != 0:
        print('~~ cmd:', cmd + '\n')
        if len(output[0][0]) > 0 and output[0][0].rstrip() != '':
          print('~~ stdout:')
          print(output[0][0].rstrip() + '\n')
        if len(output[0][1]) > 0 and output[0][1].rstrip() != '':
          print('~~ stderr:')
          print(output[0][1].rstrip() + '\n')
        if output[1] > 0:
          print('~~', program, 'terminated with exception')
        else:
          print('~~', program, 'terminated with signal', Signals(-output[1]))
        continue
      # Handle normal exit
      out = [line.rstrip() for line in output[0][0].split('\n') \
                              if line.strip() != '']
      # Assignment directions say to put output in this file
      if os.path.isfile('cache_sim_output'):
        with open('cache_sim_output','r') as infile:
          # If we wanted to keep the stdout gathered from output[0][0] . . .
          #out += [line.rstrip() for line in infile.readlines() \
          # Take the file output rather than the stdout/stderr
          out = [line.rstrip() for line in infile.readlines() \
                                            if line.strip() != '']
        # Remove the generated output file
        os.remove('cache_sim_output')
      # Get our expected output
      exp = []
      with open(expfile, 'r') as infile:
        exp = [line.rstrip() for line in infile.readlines() \
                                if line.strip() != '\n']
      # Check for an exact match
      matches = True if len(out) == len(exp) else False
      if matches:
        for i, line in enumerate(exp):
          # If they don't match
          if line != out[i]:
            matches = False
            break
      # If matches is True then our output matched
      if matches == True:
        print('Actual output matches expected output\n')
        continue
      # Ask whether to use curses or difflib
      if DiffWindow and input('Open ' + test + ' in curses? (y/n): ') == 'y':
        with DiffWindow() as win: win.showdiff(out, exp)
      else:
        for line in difflib.context_diff(a=out, fromfile='Actual',
                                          b=exp, tofile='Expected'):
          print(line)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(add_help=False,
                                    description=sys.argv[0] + \
                                      ' - The test script for HW3',
                                    argument_default=argparse.SUPPRESS,
                                    prog=sys.argv[0],
                                    epilog='Required: testpath, program')
  parser.add_argument('-h', '--help', action='store_true',
                      help='Show this help message.')
  parser.add_argument('--testpath', metavar='<path>',
                      help='Path containing test input files')
  parser.add_argument('--exppath', metavar='<path>',
                      help='Path containing expected output files')
  parser.add_argument('--program', metavar='<program>',
                      help='Path to program to test')

  args = vars(parser.parse_args())
  if 'help' in args or 'testpath' not in args or 'program' not in args:
    parser.print_help()
    sys.exit(0)

  # Collect the input files in a dictionary
  # key = inFile, value = (expFile or None)
  cases = {}
  if args['testpath'][-1] != '/': args['testpath'] += '/'
  if 'exppath' not in args: args['exppath'] = args['testpath']
  elif args['exppath'][-1] != '/': args['exppath'] += '/'
  for inFile in os.listdir(args['testpath']):
    # These are the expected output files (with parameters)
    print(os.listdir(args['exppath']))
    expFiles = [args['exppath'] + '/' + name \
                  for name in os.listdir(args['exppath']) \
                  if re.search(inFile + r'_[0-9]+_[0-9]+$', name)]
    if len(expFiles) == 0: continue
    # Link the test file to the expected output files
    cases[args['testpath'] + inFile] = expFiles

  # Do the tests
  try:
    dotests(cases, args['program'])
  # Allow ctrl-c to exit
  except KeyboardInterrupt: pass
  # Allow ctrl-d to exit
  except EOFError: print('< EOF')

# vim: tabstop=2 shiftwidth=2 expandtab
