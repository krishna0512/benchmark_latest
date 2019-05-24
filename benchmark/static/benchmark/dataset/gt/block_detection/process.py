import xml.etree.ElementTree as et

root = et.parse('text.xml').getroot()
f = open('block.csv', 'w')
count = 0
for row in root:
    count+=1
    print(count)
    filename = '{}_Book_{:04}.tif,'.format(row[0].text, int(row[1].text))
    ret = ';'.join(str(row[3].text).strip().split('\n'))
    linenumber = str(row[2].text)
    #rect = ',{},{},{},{}\n'.format(row[4].text, row[5].text, row[6].text, row[7].text)
    f.write(filename+ret)
f.close
