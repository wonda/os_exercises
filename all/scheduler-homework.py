#! /usr/bin/env python

import sys
from optparse import OptionParser
import random

parser = OptionParser()
parser.add_option("-s", "--seed", default=0, help="the random seed", 
                  action="store", type="int", dest="seed")
parser.add_option("-j", "--jobs", default=3, help="number of jobs in the system",
                  action="store", type="int", dest="jobs")
parser.add_option("-l", "--jlist", default="", help="instead of random jobs, provide a comma-separated list of run times",
                  action="store", type="string", dest="jlist")
parser.add_option("-m", "--maxlen", default=10, help="max length of job",
                  action="store", type="int", dest="maxlen")
parser.add_option("-p", "--policy", default="FIFO", help="sched policy to use: SJF, FIFO, RR, PI",
                  action="store", type="string", dest="policy")
parser.add_option("-q", "--quantum", help="length of time slice for RR policy", default=1, 
                  action="store", type="int", dest="quantum")
parser.add_option("-c", help="compute answers for me", action="store_true", default=True, dest="solve")
parser.add_option("-v", "--priority", type="string", dest="priority", help="list of priority of jobs",
                  action="store", default="1,3,2")
parser.add_option("-r", "--resource", type="string", dest="resource", help="list of resource numbers occupied by jobs",
                  action="store", default="0,0,1")

(options, args) = parser.parse_args()

random.seed(options.seed)

print 'ARG policy', options.policy
if options.jlist == '':
    print 'ARG jobs', options.jobs
    print 'ARG maxlen', options.maxlen
    print 'ARG seed', options.seed
else:
    print 'ARG jlist', options.jlist

print ''

print 'Here is the job list, with the run time, priority and resource of each job: '

import operator

joblist = []
priority = []
resource = []
for pri in options.priority.split(','):
    priority.append(int(pri))
for res in options.resource.split(','):
    resource.append(int(res))
if options.jlist == '':
    for jobnum in range(0,options.jobs):
        runtime = int(options.maxlen * random.random()) + 1
        joblist.append([jobnum, runtime])
        if (jobnum > 2):
            resource.append(random.randint(0, 5))
            priority.append(random.randint(0, jobnum))
        if options.policy == 'PI':
            print '  Job', jobnum, '( length = ' + str(runtime) + ', priority = ' + str(priority[jobnum]) + ', resource = ' + str(resource[jobnum]) + ' )'
        else:
	    print '  Job', jobnum, '( length = ' + str(runtime) + ' )'
else:
    jobnum = 0
    for runtime in options.jlist.split(','):
        joblist.append([jobnum, float(runtime)])
        jobnum += 1
        if (jobnum > 2):
            resource.append(random.randint(0, 5))
            priority.append(random.randint(0, jobnum))
    for i in range(0, len(joblist)):
        if options.policy == 'PI':
            print '  Job', joblist[i][0], '( length = ' + str(joblist[i][1]) + ', priority = ' + str(priority[i]) + ', resource = ' + str(resource[i]) + ' )'
        else:
            print '  Job', joblist[i][0], '( length = ' + str(joblist[i][1]) + ' )'
print '\n'

if options.solve == True:
    print '** Solutions **\n'
    if options.policy == 'SJF':
		#YOUR CODE
    	pass
    
    if options.policy == 'PI':
	running = 0
	print "Job 0 is running"
        while len(priority) != 0:
            for i in range(len(resource)):
                if resource[i] == resource[running] and priority[i] > priority[running]:
                    priority[running] = priority[i]
                    print 'Job', running, 'inherits the priority of Job', i
            print 'Status:'
            for jobnum in range(0, len(joblist)):
                print '  Job', joblist[jobnum][0], '( length = ' + str(joblist[jobnum][1]) + ', priority = ' + str(priority[jobnum]) + ', resource = ' + str(resource[jobnum]) + ' )'

            print "Job", joblist[running][0], 'exit'
            joblist.pop(running)
            priority.pop(running)
            resource.pop(running)
            if priority != []:
                running = priority.index(max(priority))
                print "Job", joblist[running][0], 'is running'
        print 'Done.'

    if options.policy == 'FIFO':
        thetime = 0
        print 'Execution trace:'
		#YOUR CODE
         
        print '\nFinal statistics:'
        t     = 0.0
        count = 0
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for tmp in joblist:
            jobnum  = tmp[0]
            runtime = tmp[1]
            
            response   = t
            turnaround = t + runtime
            wait       = t
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (jobnum, response, turnaround, wait)
            responseSum   += response
            turnaroundSum += turnaround
            waitSum       += wait
            t += runtime
            count = count + 1
        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)
                     
    if options.policy == 'RR':
        print 'Execution trace:'
        turnaround = {}
        response = {}
        lastran = {}
        wait = {}
        quantum  = float(options.quantum)
        jobcount = len(joblist)
        for i in range(0,jobcount):
            lastran[i] = 0.0
            wait[i] = 0.0
            turnaround[i] = 0.0
            response[i] = -1

        runlist = []
        for e in joblist:
            runlist.append(e)

        thetime  = 0.0
        while jobcount > 0:
            # print '%d jobs remaining' % jobcount
            job = runlist.pop(0)
            jobnum  = job[0]
            runtime = float(job[1])
            if response[jobnum] == -1:
                response[jobnum] = thetime
            currwait = thetime - lastran[jobnum]
            wait[jobnum] += currwait
            ranfor = 0
            if runtime > quantum:
				#YOUR CODE
                print '  [ time %3d ] Run job %3d for %.2f secs' % (thetime, jobnum, ranfor)
                runlist.append([jobnum, runtime])
            else:
                #YOUR CODE
                print '  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, jobnum, ranfor, thetime + ranfor)
                turnaround[jobnum] = thetime + ranfor
                jobcount -= 1
            thetime += ranfor
            lastran[jobnum] = thetime

        print '\nFinal statistics:'
        turnaroundSum = 0.0
        waitSum       = 0.0
        responseSum   = 0.0
        for i in range(0,len(joblist)):
            turnaroundSum += turnaround[i]
            responseSum += response[i]
            waitSum += wait[i]
            print '  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i])
        count = len(joblist)
        
        print '\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (responseSum/count, turnaroundSum/count, waitSum/count)

    if options.policy != 'FIFO' and options.policy != 'SJF' and options.policy != 'RR' and options.policy != 'PI': 
        print 'Error: Policy', options.policy, 'is not available.'
        sys.exit(0)
else:
    print 'Compute the turnaround time, response time, and wait time for each job.'
    print 'When you are done, run this program again, with the same arguments,'
    print 'but with -c, which will thus provide you with the answers. You can use'
    print '-s <somenumber> or your own job list (-l 10,15,20 for example)'
    print 'to generate different problems for yourself.'
    print ''

