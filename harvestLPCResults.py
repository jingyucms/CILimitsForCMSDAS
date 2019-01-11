import argparse
import os
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
parser.add_argument("-t","--tag",dest="tag", default='', help='tag')
parser.add_argument("-u","--user",dest="user", default='', help='name of the user running the script')
args = parser.parse_args()

tag = ""
if not args.tag == "":
	tag = "_"  + args.tag

global outDir 
outDir = "results_%s_%s"%(args.config,args.tag)
user = args.user
import subprocess
print '/store/user/%s/limits/%s'%(user,outDir)
#os.system('eosls /store/user/%s/limits/%s/'%(user,outDir))
my_env = os.environ.copy()
#process = subprocess.Popen(['eosls', '/store/user/%s/limits/%s/'%(user,outDir)], stdout=subprocess.PIPE,env=my_env)
process = subprocess.Popen(['eos' ,'root://cmseos.fnal.gov', 'ls', '/store/user/%s/limits/%s/'%(user,outDir)], stdout=subprocess.PIPE,env=my_env)
out, err = process.communicate()
for fileName in out.splitlines():
	print fileName
	copyCommand = ["xrdcp", "root://cmseos.fnal.gov//store/user/%s/limits/%s/%s"%(user,outDir,fileName), "%s//%s"%(outDir,fileName)]
	subprocess.call(copyCommand)

