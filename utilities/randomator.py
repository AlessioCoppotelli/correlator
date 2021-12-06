from random import random
import mathmethod as mat


def changerandform(value,center,extension) :
    out = value*extension + center
    return out


''' ---------  randlist function --------- '''
# randlist() :
#   output  = list of rand value
#   input   = 
#             lenght : length of list (if==1 resutn a float)
#             center : center of the random values
#             ssextension : single-sided extension -> distance from center and maximum number
def randlist(length=1,center=0.5,ssextension=0.5) :
    def changerandform(value,center,extension) :
        old_center = 0.5
        old_extensionc = 0.5
        out = (value-old_center)*extension/0.5 + center 
        return out

    if length is None :
        return random()
    out = [changerandform(random(),center,ssextension) for x in range(length)]
    if length == 1 :
        out = out[0]
    return out




#-------------------------------------------
#-------------------------------------------
#--------- M A I N -------------------------
#-------------------------------------------
#-------------------------------------------
if __name__ == '__main__' :
    import sys
    if len(sys.argv)==1:
        out = randlist()
    elif len(sys.argv)==2 :
        out = randlist(int(sys.argv[1]))
    elif len(sys.argv)==3 :
        out = randlist(int(sys.argv[1]),float(sys.argv[2]))
    elif len(sys.argv)==4 :
        out = randlist(int(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]))
    else :
        print('Only first 3 inputs will be used.')
        out = randlist(int(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]))
    print('random outut : ',out)
    print('output average : ', mat.average(out))
    
