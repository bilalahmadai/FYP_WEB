from db import rollNumGet

rollno='5'
cur_time='18:31'

import datetime
now = datetime.datetime.now()
# cur_time = now.strftime("%H:%M")

rollNumGet(rollno,cur_time)