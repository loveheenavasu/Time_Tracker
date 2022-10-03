from datetime import datetime
from datetime import datetime, date
import time 
import os



# def screenshort():
#     # path='C:\\Users\\lovet\\Time_Tracker'
#     # os.chdir(path)
#     # current_date = date.today().strftime("%b-%d-%Y~")
#     # current_time = datetime.now().strftime("%H-%M-%S")
#     # usernamefolder = "user"
#     # print(usernamefolder)
#     # newfolder = str(usernamefolder)
#     # os.makedirs(newfolder)
#     # path2 = path+'\\'+newfolder 
#     # os.chdir(path2)
#     # usernamefolder1 = str(current_date)
#     # print(usernamefolder1)
#     # newfolder = str(usernamefolder1)
#     # os.makedirs(newfolder)

def folder():
    path='C:\\Users\\lovet\\Time_Tracker\\screenshorts'
    os.chdir(path)
    current_date = date.today().strftime("%b-%d-%Y")
    current_time = datetime.now().strftime("%H-%M-%S")
    folder1 = 'users'
    newfolder = str(folder1)
    os.makedirs(newfolder)
    path2 = path+'\\'+newfolder
    os.chdir(path2)
    slicedate = current_date[7:]
    print(slicedate)
    os.makedirs(slicedate)
    path3 = path2+'\\'+slicedate
    os.chdir(path3)
    month = current_date[0:3]
    os.makedirs(month)
    print(path3) 
folder()




