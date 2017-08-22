import os
if os.path.exists('data'): os.chdir('data')
if not os.path.exists('data.py'): open('data.py', 'x').close()
with open("data.py", 'w') as f:
    f.write('assessment = {}')


