from tempfile import mkstemp
from shutil import move, rmtree, copytree
import os, argparse, io, shutil, sys

def replace(filePath, pattern, replacement):
	# writing in temp file needed, since single files can be very big > 1GB
	tempFileDescr, tempFilePath = mkstemp()
	
	with open(filePath, mode='r') as currentFileHandle, io.open(tempFilePath, mode='w', newline='\n') as tempFileHandle: #unix line endings needed
		for line in currentFileHandle:
			tempFileHandle.write(unicode(line.replace(pattern, replacement)))

	os.close(tempFileDescr) #need to close this since it's blocking the move
	shutil.move(tempFilePath, filePath)

# Currently no copy supported
# rmtree('C:\\HANA_EXPORT\\TEST2')
# copytree("C:\\HANA_EXPORT\\TEST1", "C:\\HANA_EXPORT\\TEST2")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--pattern", help="The pattern to replace", required=True)
	parser.add_argument("-r", "--replacement", help="The text which is placed instead of the removed pattern", required=True)
	parser.add_argument("-d", "--directory", help="The directory to work with", required=True)
	parser.add_argument("-i", "--includeFilter", default="", help="comma seperated list of file extension to include (whitelist)")
	parser.add_argument("-e", "--excludeFilter", default="", help="comma seperated list of file extension to exclude (blacklist)")
	args = parser.parse_args()

	if args.includeFilter and args.excludeFilter:
		print "Not supported! Either includeFilter or excludeFilter must be omitted"
		sys.exit(1)
	
	args.includeFilter = args.includeFilter.split(',')
	args.excludeFilter = args.excludeFilter.split(',')

	allFiles = [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(args.directory) for f in filenames]

	for currentFile in allFiles:
		fileExtension = os.path.splitext(currentFile)[1][1:]
		if args.excludeFilter and fileExtension in args.excludeFilter: continue
		if args.includeFilter and fileExtension not in args.includeFilter: continue
		print "Using file ", currentFile
		replace(currentFile, args.pattern, args.replacement)

if __name__ == '__main__':
	main()
