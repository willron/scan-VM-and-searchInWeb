sys.path.append('/root/python/FindVM') #manage.py的目录
os.environ['DJANGO_SETTINGS_MODULE'] = 'test.settings' #setting的目录

def RunCheckAllVM():
    RUNORNORUN = commands.getoutput('ps ax|grep checkallvm|grep -v grep')
    FINDCHECKALLVM = RUNORNORUN.find('checkallvm.py')
    if FINDCHECKALLVM == -1:
        (RUNSTATUS, RUNOUTPUT) = commands.getstatusoutput('python /root/python/FindVM/manage.py rundirect /root/python/FindVM/checkallvm.py\&')
        return RUNSTATUS, RUNOUTPUT