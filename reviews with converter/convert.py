import csv
import xlwt
import os
import sys
import subprocess
	
def convert(filename):	
	# Look for input file in same location as script file:
	inputfilename = os.path.join(os.path.dirname(sys.argv[0]), filename)
	# Strip off the path
	basefilename = os.path.basename(inputfilename)
	# Strip off the extension
	basefilename_noext = os.path.splitext(basefilename)[0]
	# Get the path of the input file as the target output path
	targetoutputpath = os.path.dirname(inputfilename)
	# Generate the output filename
	outputfilename =  os.path.join(targetoutputpath, basefilename_noext+'.xls')
 
	# Create a workbook object
	workbook = xlwt.Workbook()
	# Add a sheet object
	worksheet = workbook.add_sheet(basefilename_noext, cell_overwrite_ok=True)

	# Get a CSV reader object set up for reading the input file with tab delimiters
	datareader = csv.reader(open(inputfilename, 'r'),
                        delimiter='\t', quotechar='-')

	# Process the file and output to Excel sheet
	for rowno, row in enumerate(datareader):
	    for colno, colitem in enumerate(row):
	        worksheet.write(rowno, colno, colitem)

	# Write the output file.
	workbook.save(outputfilename)

	# Open it via the operating system (will only work on Windows)
	# On Linux/Unix you would use subprocess.Popen(['xdg-open', filename])
	#os.startfile(outputfilename)
	subprocess.Popen(['xdg-open', outputfilename])

my_files = os.listdir()
for file in my_files:
	if file.endswith("txt"):
		convert(file)