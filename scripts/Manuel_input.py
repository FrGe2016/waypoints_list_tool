#!/usr/bin/env python

from rospy import init_node, is_shutdown

if __name__ == '__main__':

  init_node('input_test')

  one_number=0
  one_string=""


  while not is_shutdown():

	  print ("Enter a string between quotes, please?")
	  one_string = raw_input()
	  print(one_string)
	  print ("Enter a number, please?")
	  one_number = input()	  
	  print(one_number)
	  print ("thanks for giving me "+ one_string + str(one_number))
	  print (is_shutdown()) #ctrl+shift+C