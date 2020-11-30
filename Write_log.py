if __name__ == '__main__':
    f =open('log.txt','a+')
    for i in range(1,3):
        x = 0
        y = 0
        z = i
        line = "X="+str(x) + ",Y=" + str(y)+",Z="+str(z)+"\n"
        f.write(line)