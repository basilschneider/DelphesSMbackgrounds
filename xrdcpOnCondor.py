import os,sys,datetime,time
from ROOT import *
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")
runDir=os.getcwd()

start_time = time.time()

pileup = sys.argv[1]

#Directories for EOSSafeUtils commands should be full (fuse mount) paths
inputDir='/eos/uscms/store/user/snowmass/noreplica/DelphesFromLHE_333pre16hadd_2016Aug/'
outputDir='/store/group/upgrade/delphes_output/DelphesFromLHE_333pre16hadd_2016Aug/'
condorDir='/uscms_data/d3/jmanagan/test/'

cTime=datetime.datetime.now()

#Control xrootd access paths
inDir=inputDir[10:]
xrdinDir='root://cmseos.fnal.gov/'+inDir
xrdOutput='root://eoscms.cern.ch/'
xrdoutDir=xrdOutput+outputDir

print 'Getting proxy'
proxyPath=os.popen('voms-proxy-info -path')
proxyPath=proxyPath.readline().strip()

dirList = [
    'B-4p-0-1-v1510_14TEV',
    'BB-4p-0-300-v1510_14TEV',
    'BB-4p-1300-2100-v1510_14TEV',
    'BB-4p-2100-100000-v1510_14TEV',
    'BB-4p-300-700-v1510_14TEV',
    'BB-4p-700-1300-v1510_14TEV',
    'BBB-4p-0-600-v1510_14TEV',
    'BBB-4p-1300-100000-v1510_14TEV',
    'BBB-4p-600-1300-v1510_14TEV',
    'Bj-4p-0-300-v1510_14TEV',
    'Bj-4p-1100-1800-v1510_14TEV',
    'Bj-4p-1800-2700-v1510_14TEV',
    'Bj-4p-2700-3700-v1510_14TEV',
    'Bj-4p-300-600-v1510_14TEV',
    'Bj-4p-3700-100000-v1510_14TEV',
    'Bj-4p-600-1100-v1510_14TEV',
    'Bjj-vbf-4p-0-700-v1510_14TEV',
    'Bjj-vbf-4p-1400-2300-v1510_14TEV',
    'Bjj-vbf-4p-2300-3400-v1510_14TEV',
    'Bjj-vbf-4p-700-1400-v1510_14TEV',
    'H-4p-0-300-v1510_14TEV',
    'H-4p-1500-100000-v1510_14TEV',
    'H-4p-300-800-v1510_14TEV',
    'H-4p-800-1500-v1510_14TEV',
    'LL-4p-0-100-v1510_14TEV',
    'LL-4p-100-200-v1510_14TEV',
    'LL-4p-1400-100000-v1510_14TEV',
    'LL-4p-200-500-v1510_14TEV',
    'LL-4p-500-900-v1510_14TEV',
    'LL-4p-900-1400-v1510_14TEV',
    'LLB-4p-0-400-v1510_14TEV',
    'LLB-4p-400-900-v1510_14TEV',
    'LLB-4p-900-100000-v1510_14TEV',
    'tB-4p-0-500-v1510_14TEV',
    'tB-4p-1500-2200-v1510_14TEV',
    'tB-4p-2200-100000-v1510_14TEV',
    'tB-4p-500-900-v1510_14TEV',
    'tB-4p-900-1500-v1510_14TEV',
    'tj-4p-0-500-v1510_14TEV',
    'tj-4p-1000-1600-v1510_14TEV',
    'tj-4p-1600-2400-v1510_14TEV',
    'tj-4p-2400-100000-v1510_14TEV',
    'tj-4p-500-1000-v1510_14TEV',
    'tt-4p-0-600-v1510_14TEV',
    'tt-4p-1100-1700-v1510_14TEV',
    'tt-4p-1700-2500-v1510_14TEV',
    'tt-4p-2500-100000-v1510_14TEV',
    'tt-4p-600-1100-v1510_14TEV',
    'ttB-4p-0-900-v1510_14TEV',
    'ttB-4p-1600-2500-v1510_14TEV',
    'ttB-4p-2500-100000-v1510_14TEV',
    'ttB-4p-900-1600-v1510_14TEV',
    ]

count = 0
for sample in dirList:

    sample = sample+'_'+pileup
    thisoutDir = outputDir+sample    
    os.system('eos '+xrdOutput+' mkdir -p '+thisoutDir)
    if not os.path.exists(condorDir+'/'+sample): os.system('mkdir -p '+condorDir+'/'+sample)
    
    rootfiles = EOSlist_root_files(inputDir+'/'+sample)
    for file in rootfiles:
        dict={'RUNDIR':runDir, 'RELPATH':sample, 'FILENAME':file, 'PROXY':proxyPath, 'INPUTDIR':xrdinDir, 'OUTPUTDIR':xrdoutDir}

        jdfName=condorDir+'/%(RELPATH)s/xrdcp_%(FILENAME)s.jdl'%dict
        print jdfName
        jdf=open(jdfName,'w')
        jdf.write(
            """x509userproxy = %(PROXY)s
universe = vanilla
Executable = %(RUNDIR)s/xrdcpOnCondor.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Output = xrdcp_%(RELPATH)s.out
Error = xrdcp_%(RELPATH)s.err
Log = xrdcp_%(RELPATH)s.log
Notification = Never
Arguments = %(INPUTDIR)s %(RELPATH)s %(FILENAME)s %(OUTPUTDIR)s

Queue 1"""%dict)
        jdf.close()
        os.chdir('%s/%s'%(condorDir,sample))
        os.system('condor_submit xrdcp_%(FILENAME)s.jdl'%dict)
        os.system('sleep 0.5')                                
        os.chdir('%s'%(runDir))
        print count, "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))



