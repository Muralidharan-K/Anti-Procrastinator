import getpass
import time
import pickle
import psutil

while True:
    username=getpass.getuser()
    filename=r'%s.pk' % (username)
    try:
        with open (filename, 'rb') as file:
            emp_blacklist=pickle.load(file)
    except FileNotFoundError:
        emp_blacklist=dict()
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            app_n = proc.info['name'].split('.')[0]
            app_name=str(app_n).lower()
            app_p = proc.info['exe']
            app_path=str(app_p).lower()
            for key in list(emp_blacklist.keys()):
               value=emp_blacklist[key]
               if not isinstance(value, list):
                   if value in app_path:
                       proc.kill()
                   elif app_name in list(emp_blacklist.keys()):
                       proc.kill()
                   elif app_name in value:
                       proc.kill()
                   else:
                       pass
        except:
            pass
    key_list=list(emp_blacklist.keys())
    time.sleep(5)