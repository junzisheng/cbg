<<<<<<< HEAD
# encoding: utf-8
"""将templates中的文件js的域从梦幻改为/static/"""
import re
import os
cbg_backup_file = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(cbg_backup_file)
os.chdir(os.path.join(cbg_backup_file, 'templates', 'crawl_url'))
file_conte_dict = {}
for file in os.listdir('.'):
    with open(os.path.join(cbg_backup_file, 'templates', 'crawl_url', file), 'r', encoding='utf-8') as f:
        file_conte_dict[file] = f.read()

for file, content in file_conte_dict.items():
    with open(os.path.join(cbg_backup_file, 'templates', 'crawl_url', file), 'w', encoding='utf-8') as f:
        res = re.sub('<script\s+type="text/javascript"\s+src="http://res\.xyq\.cbg\.163.com/', '<script src="/static/', content)
        f.write(res)



