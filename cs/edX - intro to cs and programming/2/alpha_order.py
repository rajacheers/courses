s = 'abcbcd'
#s = 'abcdefghajdkfnab'
s = 'azcbobobegghakl'
#print "Input string: ",s 
i = 0
c2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
c3 = 0
c4 = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
while i<len(s):
    
    #print "Outer loop ",s[i]
    c3 = c3+1
    c4[c3] = c4[c3]+s[i]
    
    count = 1
    
    while i<len(s)-1:
        #print "Inner Loop: ",s[i] ,s[i+1]
        if s[i] <= s[i+1]:
            
            i +=1
            c4[c3] = c4[c3]+s[i]
            count += 1
            c2[c3]=count
            #print c2
            #print c4
        else:
            break
    i +=1
fin = c2.index(max(c2))
print "Longest substring in alphabetical order is: "+c4[fin]
