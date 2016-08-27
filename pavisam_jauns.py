dimport csv,sqlite3
import matplotlib.pyplot as plt

con = sqlite3.connect('datatable.db')
c = con.cursor()
def getUserIntegerInput(question):
    while True:
        try:
            dis = raw_input(question)
            dis = int(dis)
            break
        except:
            print'\n Integer -- please.\n'
            pass
    return dis

def checkValue(val,max):
    if val <= max:
        return True
    return False

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def createTable(c):
    c.execute('DROP TABLE IF EXISTS main_data;')
    c.execute('CREATE TABLE main_data (id INTEGER PRIMARY KEY AUTOINCREMENT, x Decimal(10,3), y Decimal(10,3), z Decimal(10,3));')

def processChank(chunk, c):
    for d in chunk:
        #print d,'\n'
        c.execute('INSERT INTO main_data ( x, y, z) VALUES (?, ?, ?);', (d[0], d[3], d[6]))
    con.commit()
data = csv.reader(open('test2.csv','rb'), delimiter=' ') 

def readData(c,table):
    d = c.execute('select * from %s;'%(table))
    for x in d:
        print x,'\n'
    return d
def writeChunk(name1,last_id1,line1):
    with open(name1+'.csv', 'a') as f:
        c.execute('SELECT id,x,y,z FROM main_data where id >= ? and id < ?;',(last_id1,line1,))
        writer = csv.writer(f, dialect='excel', lineterminator='\n')
        writer.writerows(c)
        f.close()
def writeFile(c):
    #c.execute('SELECT id,x,y,replace(z, "\r\n", "") FROM main_data;')
    while True:
        while True:
            name = raw_input('Please enter output file name : ')
            name.strip()
            if name != '':
                break
        try:
            f = open(name+'.csv', 'w')
            #c.execute('SELECT id,x,y,z FROM main_data;')
            writer = csv.writer(f, dialect='excel', lineterminator='\n')
            writer.writerow(['id','x', 'y','z'])
            f.close()
            last_id = 0
            total = c.execute('SELECT count(id) FROM main_data;').fetchall()
            for line in range(0,total[0][0],100):
                writeChunk(name,last_id,line)
                last_id = line+1
            writeChunk(name,last_id,total[0][0]+1)
            f.close()
            break
        except:
            print 'Error writing file - pleas check the file name. '

def XY_table(c):
    table_size = []

    max_val = c.execute('SELECT max(x),max(y),max(z) FROM main_data;').fetchall()
    min_val = c.execute('SELECT min(x),min(y),min(z) FROM main_data;').fetchall()
    x = max_val[0][0]-min_val[0][0]
    table_size.append(x)
    y = max_val[0][1]-min_val[0][1]
    table_size.append(y)
    return table_size

def createTableKiKy(c):
    c.execute('DROP TABLE IF EXISTS normalized_main_data_Ki_Ky;')
    c.execute('CREATE TABLE normalized_main_data_Ki_Ky (id INTEGER PRIMARY KEY AUTOINCREMENT, x Decimal(10,3), y Decimal(10,3),z Decimal(10,3), Ki Decimal(10), Ky Decimal(10));')

def calculate_dd_ki(c,count,count_Ki,ll,variabl,variabl1,result,other):
    dataSel = c.execute('select x,y,z from main_data where x = ? order by y asc;',(ll,)).fetchall()
    print dataSel
    for val in range(len(dataSel)):
        if val == 0:
            #c.execute('insert into normalized_main_data_Ki_Ky (x,y,z,Ki) values (?,?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],0,))
            c.execute('insert into normalized_main_data_Ki_Ky (x,y,z) values (?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],))
            count +=1
        elif dataSel[val][1]-dataSel[val-1][1] == 1:
            #c.execute('insert into normalized_main_data_Ki_Ky (x,y,z,Ki) values (?,?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],1,))
            c.execute('insert into normalized_main_data_Ki_Ky (x,y,z) values (?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],))
            count +=1
            count_Ki +=1
        elif dataSel[val][1]-dataSel[val-1][1] > 1:
            dist = dataSel[val][1]-dataSel[val-1][1]
            #c.execute('insert into normalized_main_data_Ki_Ky (x,y,z,Ki) values (?,?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],dist,))
            c.execute('insert into normalized_main_data_Ki_Ky (x,y,z) values (?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],))
            other.append((count,dataSel[val][0],dataSel[val][1], dist))
            count+=1
        result.append((ll,dataSel[val][1],count_Ki))
        #c.execute('insert into normalized_main_data_Ki_Ky (x,y,z,Ki) values (?,?,?,?)',(dataSel[val][0],dataSel[val][1],dataSel[val][2],dist,))
        c.execute('update normalized_main_data_Ki_Ky set Ki = ? where x=?',(count_Ki,ll,))


def calculate_points_Ki(variabl,variabl1,step):
    result=[]
    count =0
    other =[]
    max_val1 = c.execute('SELECT max(x) FROM main_data;').fetchall()
    min_val1 = c.execute('SELECT min(x) FROM main_data;').fetchall()
    mid_x = (min_val1[0][0]+max_val1[0][0]+1)/2
    print max_val1[0][0],'\n Middle Y ::: ====',mid_x,'\n',min_val1[0][0],'\n'
    line = 0
    if max_val1[0][0]-mid_x > mid_x-min_val1[0][0]:
        arange = int((max_val1[0][0]-mid_x)/step)
    else:
        arange = int((mid_x-min_val1[0][0])/step)
    #dataSel1 = c.execute('select * from main_data where x >= ? and x <= ?;',(min_val1,max_val1,)).fetchall()
    #for nr in dataSel1:
    #    print nr
    for aa in range(0,arange,1):
        count_Ki =0
        if aa == 0:
            ll = mid_x
            calculate_dd_ki(c,count,count_Ki,variabl,variabl1,ll,result,other)
        else:
            ll = mid_x+(aa*step)
            print ll
            calculate_dd_ki(c,count,count_Ki,variabl,variabl1,ll,result,other)
            ll = mid_x-(aa*step)
            print ll
            calculate_dd_ki(c,count,count_Ki,variabl,variabl1,ll,result,other)

    return result

def calculate_points_Ky(variabl,variabl1,step):
    result=[]
    count =0
    other =[]
    #dataSel1 = c.execute('select * from main_data where x >= ? and x <= ?;',(min_val1,max_val1,)).fetchall()
    #for nr in dataSel1:
    #    print nr
    max_val1 = c.execute('SELECT max(y) FROM normalized_main_data_Ki_Ky;').fetchall()
    min_val1 = c.execute('SELECT min(y) FROM normalized_main_data_Ki_Ky;').fetchall()
    mid_y = (min_val1[0][0]+max_val1[0][0]+1)/2
    print max_val1[0][0],'\n Middle Y ::: ====',mid_y,'\n',min_val1[0][0],'\n'
    line = 0
    if max_val1[0][0]-mid_y > mid_y-min_val1[0][0]:
        arange = int((max_val1[0][0]-mid_y)/step)
    else:
        arange = int((mid_y-min_val1[0][0])/step)
    print 'value = ',arange
    for a in frange(0,arange+1,1):
        count_Ky =0
        print '\n xxx = ',a
        ll = mid_y+(a*step)
        print '\nsearchll : ',ll,'\n\n'
        dataSel = c.execute('select %s,%s,z from normalized_main_data_Ki_Ky where %s = ? order by %s asc;'%(variabl,variabl1,variabl1,variabl),(ll,)).fetchall()
        print dataSel
        for val in range(len(dataSel)):
            if val == 0:
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(0,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                count +=1
            elif dataSel[val][0]-dataSel[val-1][0] == step:
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(1,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                count +=1
                count_Ky +=1
            elif dataSel[val][0]-dataSel[val-1][0] > step:
                dist = dataSel[val][0]-dataSel[val-1][0]
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(dist,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                other.append((count,dataSel[val][0],dataSel[val][1], dist))
                count+=1
            result.append((ll,dataSel[val][0],count_Ky))
            c.execute('update normalized_main_data_Ki_Ky set Ky = ? where y=?',(count_Ky,ll,))
        ll = mid_y-(a*step)
        print '\nsearchll : ',ll,'\n\n'
        dataSel = c.execute('select %s,%s,z from normalized_main_data_Ki_Ky where %s = ? order by %s asc;'%(variabl,variabl1,variabl1,variabl),(ll,)).fetchall()
        print dataSel
        for val in range(len(dataSel)):
            if val == 0:
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(0,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                count +=1
            elif dataSel[val][0]-dataSel[val-1][0] == 1:
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(1,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                count +=1
                count_Ky +=1
            elif dataSel[val][0]-dataSel[val-1][0] > 1:
                dist = dataSel[val][0]-dataSel[val-1][0]
                #c.execute('update normalized_main_data_Ki_Ky set Ky = ? where x=? and y=? and z=?',(dist,dataSel[val][0],dataSel[val][1],dataSel[val][2],))
                other.append((count,dataSel[val][0],dataSel[val][1], dist))
                count+=1
            result.append((ll,dataSel[val][0],count_Ky))
            c.execute('update normalized_main_data_Ki_Ky set Ky = ? where y=?',(count_Ky,ll,))

    return result


def printMaxAvgMin(c):
    max_val = c.execute('SELECT max(x),max(y),max(z) FROM main_data;').fetchall()
    avg_val = c.execute('SELECT avg(x),avg(y),avg(z) FROM main_data;').fetchall()
    min_val = c.execute('SELECT min(x),min(y),min(z) FROM main_data;').fetchall()
    x_max = max_val[0][0]
    y_max = max_val[0][1]
    z_max = max_val[0][2]
    x_min = min_val[0][0]
    y_min = min_val[0][1]
    z_min = min_val[0][2]
    x_avg = (max_val[0][0]+min_val[0][0])/2
    y_avg = (max_val[0][1]+min_val[0][1])/2
    z_avg = (max_val[0][2]+min_val[0][2])/2
    print 'Current     X max : ', x_max,'      Y max : ',y_max,'      Z max : ',z_max,'\n'
    print 'Current X average : ', x_avg,'  Y average : ',y_avg,'  Z average : ',z_avg,'\n'
    print 'Current     X min : ', x_min,'      Y max : ',y_min,'      Z min : ',z_min,'\n'

def calculate_Ki(c):
    final_results = []
    printMaxAvgMin(c)
    max_val = c.execute('SELECT max(x),max(y),max(z) FROM main_data;').fetchall()
    while True:
        qq = raw_input('Would you like to normalize data y/n?')
        qq = qq.lower()
        if qq =='y':
            while True:
                q2 = raw_input('Which column do you wish to normalize ( x , y , z , c(cancel))?')
                q2 = q2.lower()
                if q2 == 'x' or q2 == 'y' or q2 == 'z':
                    while True:
                        entered_val = getUserIntegerInput('Please insert integer value between 1 and '+q2+' max :')
                        if q2 == 'x':
                            valid = checkValue(entered_val,max_val[0][0])
                            if valid == True:
                                c.execute('UPDATE main_data SET x = x - ?',(entered_val,))
                                printMaxAvgMin(c)
                                break
                        elif q2 == 'y':
                            valid = checkValue(entered_val,max_val[0][1])
                            if valid == True:
                                c.execute('UPDATE main_data SET y = y - ?',(entered_val,))
                                printMaxAvgMin(c)
                                break
                        elif q2 == 'z':
                            valid = checkValue(entered_val,max_val[0][2])
                            if valid == True:
                                c.execute('UPDATE main_data SET z = z - ?',(entered_val,))
                                printMaxAvgMin(c)
                                break
                        else:
                            print ' Invalid input !!!'
                elif q2 == 'c':
                    break
                else:
                    print ' Invalid input !!!'
            print'\n Writing normalized data file. \n'
            writeFile(c)
            break
        elif qq =='n':
            break
        else:
            print ' Invalid input !!!'
    while True:
        step1 = getUserIntegerInput('Please enter spacing :')
        if step1:
            break
    createTableKiKy(c)
    # calculate Ki for points
    x_ki=calculate_points_Ki('y','x',step1)
    # calculate Ky for points
    #y_ki=calculate_points_Ky('x','y',step1)
    #final_results.append(calculate_points(z_min,z_max))
    #for a in x_ki:
    #    #for aa in a:
    #    print a,'\n'
    #print '\n\n vertical ==============='
    #for b in y_ki:
    #    #for bb in b:
    #    print b,'\n'
    #print '\n\n'
    #print final_results

def writeResultChunk(name1,last_id1,line1):
    with open(name1+'.csv', 'a') as f:
        c.execute('SELECT id,x,y,z,Ki,Ky FROM normalized_main_data_Ki_Ky where id >= ? and id < ?;',(last_id1,line1,))
        writer = csv.writer(f, dialect='excel', lineterminator='\n')
        writer.writerows(c)
        f.close()
def writeResultFile(c):
    #c.execute('SELECT id,x,y,replace(z, "\r\n", "") FROM main_data;')
    while True:
        while True:
            name = raw_input('Please enter output file name : ')
            name.strip()
            if name != '':
                break
        try:
            f = open(name+'.csv', 'w')
            #c.execute('SELECT id,x,y,z FROM main_data;')
            writer = csv.writer(f, dialect='excel', lineterminator='\n')
            writer.writerow(['id','x', 'y','z','Ki','Ky'])
            f.close()
            last_id = 0
            total = c.execute('SELECT count(id) FROM main_data;').fetchall()
            for line in range(0,total[0][0],100):
                writeResultChunk(name,last_id,line)
                last_id = line+1
            writeResultChunk(name,last_id,total[0][0]+1)
            break
        except:
            print 'Error writing file - pleas check the file name. '

def plot_points(c):
    data = c.execute('SELECT x,y FROM normalized_main_data_Ki_Ky').fetchall()
    for valp in range(len(data)):
        #print d
        plt.scatter(data[valp][0],data[valp][1])
    plt.show()

#  =============RUN =======================
chunk, chunkSize = [], 100
createTable(c)

for i,d in enumerate(data):
    if(i % chunkSize == 0 and i > 0):
        processChank(chunk,c)
        del chunk[:]
    chunk.append(d)

processChank(chunk,c)

#adata = readData(c)
table_XY = XY_table(c)

#print table_XY
calculate_Ki(c)
#readData(c,'main_data')
readData(c,'normalized_main_data_Ki_Ky')

#writeFile(c)
#//writeResultFile(c)

plot_points(c)

con.close()