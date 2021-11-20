#!/usr/bin/env python

from time import sleep
from rospy import init_node, is_shutdown
from pynput import keyboard

# https://www.delftstack.com/fr/howto/python/python-detect-keypress/
# https://pypi.org/project/pynput/


def on_press(key):
	try:
		print('Alphanumeric key pressed: {0} '.format(
			key.char))
		if(key.char=="a"):
			print("Enter a number ? ")
			something=1 #a number to avoid requesting quote in the input
			something = raw_input()
			print(something)
			print ("thanks for giving me " + str(something))
	except AttributeError:
		print('special key pressed: {0}'.format(
			key))

def on_release(key):
	print('Key released: {0}'.format(
		key))
	if key == keyboard.Key.esc:
		print("Existing key capture")
		l.stop()	
		return False



#if __name__ == '__main__':

init_node('input_test')

print("Press a key")

"""	
# Collect events until released
 keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
	listener.join() 
"""
l = keyboard.Listener(on_press=on_press,on_release=on_release)
l.start()
l.join()




"""
# ...or, in a non-blocking fashion:
listener =keyboard.Listener(
	on_press=on_press,
	on_release=on_release)
listener.start()
"""

#while True:
#	print(key)
#		sleep()#		break		
		
""" 
List of typical results for special keys
special key pressed: Key.shift
special key pressed: Key.ctrl
special key pressed: Key.alt
Alphanumeric key pressed: None 
special key pressed: Key.left
special key pressed: Key.down
special key pressed: Key.up
special key pressed: Key.right
special key pressed: Key.insert
special key pressed: Key.delete
special key pressed: Key.end
special key pressed: Key.home
special key pressed: Key.page_up
special key pressed: Key.page_down
special key pressed: Key.pause
special key pressed: Key.scroll_lock
special key pressed: Key.print_screen
special key pressed: Key.esc
special key pressed: Key.f1
special key pressed: Key.f2
special key pressed: Key.f3
special key pressed: Key.f4
special key pressed: Key.f5
special key pressed: Key.f6
special key pressed: Key.f7
special key pressed: Key.f8
special key pressed: Key.f9
special key pressed: Key.f10
special key pressed: Key.f11
special key pressed: Key.f12
special key pressed: Key.enter

special key pressed: Key.tab
		special key pressed: Key.caps_lock
special key pressed: Key.caps_lock
special key pressed: Key.shift		 
"""
 