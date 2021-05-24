pairs = 25
th = 3

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
process=0
first_index=0
for i in range (0+th,pairs+th,th):
    fin = i -1
    if (fin>=pairs) : fin = pairs -1
    print (f'process: {process} debut: {first_index} fin: {fin}')
    first_index=i
    process +=1
    
