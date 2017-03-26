import sys,os
from sandy import sandy_func
from comparator import compare

base_dir = os.path.dirname(os.path.abspath(__file__))
user_dir=base_dir+"/user"
error_dir=base_dir +"/error"
description_dir=base_dir + "/standard/description"
cosin_dir = base_dir + "/input"
stdin_dir = base_dir + "/standard/input"
#output_dir = base_dir + "/standard/output"

def run(exec_file,uid,qid):
	#print "in run function"
	if(sys.argv[2]=='1'):
		#print "in custom"+sys.argv[2]
		in_file=cosin_dir+"/"+str(uid)+"/"+sys.argv[1].split(".")[0]+".in"	#standard input for running
	else:
		#print "in std"+sys.argv[2]
		in_file=stdin_dir+"/"+str(qid)+"/s.in"				#testcase file to be changed
	in_file_fd=open(in_file,"r")
	user_out=user_dir+"/"+str(uid)+"/"+str(qid)+"/"+sys.argv[1].split(".")[0]+".uout"
	
	user_out_fd=os.open(user_out, os.O_RDWR|os.O_CREAT)	#user output after running
	des_file=description_dir+"/"+str(qid)+"/"+str(0)+".txt"	#description file
	
	des_fd=open(des_file,"r")
	lines=des_fd.readlines()
	time=lines[0].strip()
	mem=lines[1].strip()
	des_fd.close()
	
	res=sandy_func(exec_file,in_file_fd,user_out_fd,time,mem)
	
	in_file_fd.close()
	os.close(user_out_fd)
	out_fd=open(user_out,"r")
	print out_fd.read()
	os.remove(user_out)			#removing user output
	if(sys.argv[2]=='1'):
		os.remove(in_file)		#removing user input file in case of custom
	
	return res
	
def compile(src_userfile, exec_file,error_file,ext):	
		a=1
		if (ext=='c'):
			a=os.system("gcc "+src_userfile+" -o "+exec_file+" 2>"+error_file)
		elif (ext=="cpp"):
			a= os.system("g++ "+ src_userfile+" -o "+exec_file+" 2>"+error_file)
		return a
		
def main():
	filename=sys.argv[1]
	ext=sys.argv[1].split(".")[-1]		#Assuming filename with format uid_qid.ext is passed on command line
	#print ext
	uid= sys.argv[1].split("_")[0]
	qid=sys.argv[1].split("_")[1]
	qid=qid.split(".")[0]
	
	#print uid,qid,sid

	src_userfile=user_dir+"/"+uid+"/"+qid+"/"+filename
	exec_file=user_dir+"/"+uid+"/"+qid+"/"+filename.split(".")[0]
	
	error_file=error_dir+"/"+uid+"/"+filename.split(".")[0]		#need to check existence before using
	res= []
	if(os.path.isfile(error_file)==False):
		error_fd=os.open(error_file, os.O_RDONLY|os.O_CREAT)
		os.close(error_fd)
	a=compile(src_userfile,exec_file,error_file,ext)	#exec_file created after compilation
		
	if(a==0):
			os.remove(error_file)			#removes files only not directory removedirs to remove dir
			#for i in range(0,5):
			res=run(exec_file,uid,qid)
				
			os.remove (exec_file)
			#print "successful compilation"
	else:
			res=-9999
			#print "error in compilation"
	
	if res == 5 :
	    print "Time Limit Exceeded"
	elif res == 7:
	    print "Abnormal Termination"
	elif res == -9999:
	    print "Compile Time Error"    
main()

# result of judge
# 1= write answer
#-99 = wrong answer
# 5  = TLE
# 7  = Abnormal termiation
#-9999 = compile time error

#1 = custom
#0 = standard input
