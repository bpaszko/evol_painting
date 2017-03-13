import os
from time import sleep


i = 1
while True:
	if os.path.exists("/proc/12729"):
		os.system("rm bak1/*")
		os.system("cp pictures/* bak1/")
		os.system("rm pictures/*")	
	if os.path.exists("/proc/12739"):
		os.system("rm bak2/*")
		os.system("cp pictures2/* bak2/")
		os.system("rm pictures2/*")	
	if os.path.exists("/proc/12755"):
		os.system("rm bak3/*")
		os.system("cp pictures3/* bak3/")
		os.system("rm pictures3/*")	

	print("Cleaned: ", i)
	i += 1
	sleep(1800)