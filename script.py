import os,subprocess,sys, glob, pandas, numpy as np

# compile all java files
def compileFiles():
	# compile my key code
	files = glob.glob('./*java')
	for file in files:
		if file.endswith('.java'):
			subprocess.call(["javac", "-cp", "./junit-4.11.jar:.", file])

	# compile students' code
	for root, dirs, files in os.walk("."):
		if root is not ".":
			os.chdir(root)
			
			print "Compiling " + root
			for root, dirs, files in os.walk("."):
				for file in files:
					if file.endswith('.java'):
						subprocess.call(["javac", "-cp", "./../junit-4.11.jar:.", file])

			os.chdir("..")

# remove all class files and generated output files
def removeClassFiles():
	files = glob.glob('./*class')
	for file in files:
		subprocess.call(["rm", file])

	for root, dirs, files in os.walk("."):
		if root is not ".":
			os.chdir(root)
			
			for root, dirs, files in os.walk("."):
				for file in files:
					if file.endswith(('.class','.txt')):
						subprocess.call(["rm", file])
			os.chdir("..")

def runTests(testClassFile):
	# compile my key code
	files = glob.glob('./*java')
	for file in files:
		if file.endswith('.java'):
			subprocess.call(["javac", "-cp", "./junit-4.11.jar:.", file])

	# preprocess matrix
	studentList = []
	studentTestList = []
	numberOfStudents = 0
	for root, dirs, files in os.walk('.'): # traverse each student
		if root is not ".":
			studentList.append(root[2:])
			studentTestList.append(root[2:]+"'s test")
			numberOfStudents = numberOfStudents + 1
	
	# detect students' test errors
	errorMatrix = detectStudentTestErrors(numberOfStudents, testClassFile)

	testMatrix = []
	# runTests
	for root, dirs, files in os.walk('.'): # traverse each student
		if root is not ".":
			os.chdir(root)
			
			for root2, dirs2, files2 in os.walk("."): # find all none test file and add to main directory
				for file in files2:
					if file.endswith(".class") and testClassFile not in file:
						# copy code files to main
						subprocess.call(["cp", file, "./../"])
			os.chdir("..")

			row = []
			# traverse every student directory, copy the test file to main, run test file, save results, remove test file
			for root2, dirs2, files2 in os.walk("."):
				if root2 is not ".":
					os.chdir(root2)
					# copy the test file to main
					subprocess.call(["cp",testClassFile,"./../"]) 
					os.chdir("..")

					# run test and save results
					text_file = open(root+'/'+root[2:]+'Results.txt', 'a')
					testingNow = "\n" +root[2:] + " testing with " + root2[2:] + "'s test file\n"
					print testingNow
					with open(root+'/'+root[2:]+'Results.txt', "a") as myfile:
						myfile.write(testingNow)

					proc = subprocess.Popen(["java", "-cp", "./hamcrest-core-1.3.jar:./junit-4.11.jar:.", testClassFile[:-6]], stdout=subprocess.PIPE)
					output = proc.stdout.read()

					# write the result to file
					with open(root+'/'+root[2:]+'Results.txt', "a") as myfile:
						myfile.write(output)

					# parse output, append number of errors to row
					outputList = output.split()
					numberOfErrors = int(outputList[2])
					row.append(numberOfErrors)

					# remove test file
					subprocess.call(["rm",testClassFile])
			testMatrix.append(row)

			# remove student's code files in main
			for root2, dirs2, files2 in os.walk("."):
				for file in files2:
					if file.endswith(".class"):
						subprocess.call(["rm","-f", file])
	# flip matrix
	resultArray = np.array(testMatrix).transpose() - np.array(errorMatrix)

	# print matrix
	print "\nError Matrix\n"
	printMatrix(resultArray,studentList,studentTestList)

# return a matrix of number of errors each student's test have
def detectStudentTestErrors(numberOfStudents, testClassFile):
	errorMatrix = []
	for root, dirs, files in os.walk('.'): # traverse each student
		if root is not ".":
			os.chdir(root)

			for root2, dirs2, files2 in os.walk("."): # find test file and add to main directory
				for file in files2:
					if file.endswith(".class") and testClassFile in file:

						# copy test file to main
						subprocess.call(["cp", file, "./../"])
			os.chdir("..")

			row = []
			proc = subprocess.Popen(["java", "-cp", "./hamcrest-core-1.3.jar:./junit-4.11.jar:.", testClassFile[:-6]], stdout=subprocess.PIPE)
			output = proc.stdout.read()

			# parse output see how many errors there are
			outputList = output.split()
			numberOfErrors = int(outputList[2])
			
			# append to the list
			for x in range(0, numberOfStudents):
			 	row.append(numberOfErrors)
   			errorMatrix.append(row)

   	return errorMatrix

def printMatrix(matrix,students,studentTests):
	print pandas.DataFrame(matrix, studentTests, students)

args = sys.argv
if len(args) <= 1:
	print "Not enough arguments"
elif args[1] == "compile":
	compileFiles()
elif args[1] == "run":
	if len(args) <= 2:
		print "Not enough arguments"
	else:
		runTests(args[2])
elif args[1] == "remove":
	removeClassFiles()
else:
	print "invalid command" + args[1]