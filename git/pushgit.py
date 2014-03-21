#-* coding:UTF-8 -*                                                                                                 
#!/usr/bin/env python
import getopt, sys
import subprocess
import os

def pushmygit(repo, commit_comment):
    subprocess.check_call('bash /data/git/pullgit.sh', shell=True)
    os.chdir('/data/git/%s' %(repo))
    subprocess.check_call('git add --all .', shell=True)
    subprocess.check_call('git commit -m "%s"' %(commit_comment), shell=True)
    #subprocess.check_call('git push -u origin master', shell=True)
    condition = 1
    while condition :
        ret = subprocess.call('git push -u origin master', shell=True)
        if ret == 0 :
            condition = 0

def usage():
    '''Command help'''
    print("Usage:%s [-h|-r|-c] [--help|--repo=""|--commit=""] args...." % sys.argv[0]);

def parseargv():
    '''Parse argv '''
    try:                                                                                                            
        opts, args = getopt.getopt(sys.argv[1:], "hr:c:", ["help", "repo=", "commit="])
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-r", "--repo"):
            repo = a
        elif o in ("-c", "--commit"):
            commit = a
        else:
            assert False, "unhandled option"
    if repo and commit :
        print repo, commit
        return repo,commit
    else:
        print "Please get more option"
        sys.exit(1)

def main():
    repo, commit_comment = parseargv()    
    pushmygit(repo, commit_comment)

if __name__ == "__main__" :
    main()
