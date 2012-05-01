    #read information from filename
def read(filename):
    records = []
    try:
        for line in open(filename):
            records.append(line.strip().split("#"))
    except IOError:
        pass
    return records

    #save information into filename     
def save(records,filename):
    out = open(filename,'w')
    for items in records:
        out.write('#'.join(items)+'\n')
    out.close()

    #sort content of the filename by name
def sort_content(filename):
    file = open(filename)
    records = {}
    t=[]
    for line in file:
        t = line.split("#")
        records[t[0]]=t[1:]
    k=records.keys()
    k.sort()
    out = open(filename,'w')
    l=map(lambda key:(key,records[key]),k)
    for items in l:
        out.write(items[0]+"#")
        out.write('#'.join(items[1]))
    out.close()
 
                    
                    
        
