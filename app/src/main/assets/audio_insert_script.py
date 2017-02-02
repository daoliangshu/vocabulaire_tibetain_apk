#!python3

import os, sqlite3, shutil, re

conn = sqlite3.connect("fr_tb_dic.db")
cursor = conn.cursor()
q = "SELECT _id, trans FROM basic_dic WHERE lesson=?;"
res_dic = {}
for row in cursor.execute(q, ["2",]).fetchall():
	res_dic[row[0]] = row[1]


if not os.path.exists('temp_ogg_files'):
	os.makedirs('temp_ogg_files')


cursor2 = conn.cursor()
q2 = "UPDATE basic_dic SET sound_ogg=? WHERE _id=?"

regex = re.compile(r"\(.*\)", re.IGNORECASE)

for key, value in res_dic.items():
	if value == '':
		continue
	v = value
	if ',' in value:
		v = value.replace(',', '. ')
	if '(' in value:
		v = regex.sub('', v)
	filename = 'temp_ogg_files/'+ str(key) + '.wav'
	os.system('ekho -v \'Tibetan\' \"' + v + 
				'\" -t wav -o \'' + filename + '\' -s -15')
	print(str(key) + ' <---> ' + str(v))
	with open(filename, 'rb') as f:
		ablob = f.read()
	
	cursor2.execute(q2, [sqlite3.Binary(ablob), key,])

conn.commit()


cursor3 = conn.cursor()
q3 = "SELECT sound_ogg FROM basic_dic WHERE _id=3"
cursor3.execute(q3)
res = cursor3.fetchone()
f = open('TEST', 'wb')
f.write(res[0])
f.close()

conn.close()

# Cleaning
#if os.path.exists('temp_ogg_files'):
#	shutile.rmtree('temp_ogg_files', ignore_errors=True)

