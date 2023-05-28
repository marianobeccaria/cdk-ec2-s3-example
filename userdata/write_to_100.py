#!/usr/bin/python3

def write_to_num(val):

  file = open("/tmp/mydatafile.txt","w")

  for num in range(1,val):
    file.write(f'data: {num}\n')
    print(f'data: {num}')

  file.close()

write_to_num(100)