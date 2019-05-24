import os
import xml.etree.ElementTree as et

root = et.parse('line.xml').getroot()
count = 0
os.chdir('gt')
oldfilename = '9812_Book12_Img_600_Smooth_Page_0008.txt'
f = open(oldfilename, 'w')
for row in root:
    count+=1
    print(count)
    filename = '{}_Book12_Img_600_Smooth_Page_{:04}.txt'.format(row[0].text, int(row[1].text))
    if filename != oldfilename:
        oldfilename = filename
        f.close()
        f = open(filename, 'w')
    linenumber = str(row[3].text)
    rect = '{},{},{},{}\n'.format(row[5].text, row[7].text, row[6].text, row[8].text)
    f.write(rect)
f.close
