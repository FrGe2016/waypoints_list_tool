#!/usr/bin/env python

from time import sleep
from rospy import init_node, is_shutdown
from pynput import keyboard

# https://www.delftstack.com/fr/howto/python/python-detect-keypress/
# https://pypi.org/project/pynput/


current_selection=0
current_selection_label="Make a first choice "
current_manage_mode="Manage list non active"
current_manage_sub_mode="Navigate"
selected_waypoint=0
x=0
y=0
stepX=0.01
stepY=0.01

def print_menu():
	global selected_waypoint, x, y, stepX, stepY, current_selection_label, current_selection ,current_manage_mode,current_manage_sub_mode
	print("")
	print("")
	print("1.New path")
	print("2.Import path from csv")
	print("3.Manage list ")
	print("4.Rearange orientations")
	print("5.Simulate all")
	print("6.Simulate range")
	print("7.Save")
	print("8.Quit")	
	print("")

	print(current_selection_label)
	print("Waypoint is "+str(selected_waypoint)+"	x ="+str(x)+"	y ="+str(y))
	if current_selection!=3:
		current_manage_mode="manage list non active"
	else:	
		current_manage_mode="Manage list active: PgUp next Point, PgDn Previous point, d for delete, i for insert, m For modify"
		print(current_manage_mode)
	
	if current_selection==3:
		print(current_manage_sub_mode)

	print("")	
	print("Enter your choice")
	


def on_press(key):
	global selected_waypoint, x, y, stepX, stepY, current_selection_label, current_selection, current_manage_mode,current_manage_sub_mode
	try:
	#	print('Alphanumeric key pressed: {0} '.format(
	#		key.char))
		if(key.char=="1"):
			current_selection=1	
			current_selection_label="1.New path"
			print_menu()		
		if(key.char=="2"):
			current_selection=2
			current_selection_label="2.Import path from csv"
			i=0	
			sleep(1)
			print(i)
			i=i+1
			sleep(1)
			print(i)
			i=i+1
			sleep(1)
			print(i)
			i=i+1
			sleep(1)
			print(i)
			i=1+1
			print("import completed")
			print_menu()			
		if(key.char=="3"):
			current_selection=3
			current_manage_mode="Manage list active: PgUp next Point, PgDn Previous point, d for delete, i for insert, m For modify"
			current_selection_label="3.Manage list"
			current_manage_sub_mode="Navigate"
			print_menu()						
		if(key.char=="4"):
			current_selection=4
			current_selection_label="4.Rearange orientations"
			print_menu()			
		if(key.char=="5"):
			current_selection=5
			current_selection_label="5.Simulate all"
			print_menu()					
		if(key.char=="6"):
			current_selection=6
			current_selection_label="6.Simulate range"
			print_menu()			
		if(key.char=="7"):
			current_selection=7
			current_selection_label="7.Save"
			print_menu()				
		if(key.char=="8"):
			current_selection=8
			current_selection_label="8.Quit"
			print_menu()					
		if(key.char=="i"):
			current_manage_sub_mode="Insert after the selected point"
			print_menu()			
		if(key.char=="d"):
			current_manage_sub_mode="Delete the selected point"
			print_menu()
		if(key.char=="m"):
			current_manage_sub_mode="Modify the selected point x and y cordinates with arrows  c to confirm position (pg_up or pg) _dn to cacel"
			print_menu()
		if(key.char=="c"):
			print("Confirmed_new position")
			current_manage_sub_mode="Navigate"
			print_menu()	

	except AttributeError:
		#print('special key pressed: {0}'.format(
		#	key))
		if(current_selection==3):
			if key == keyboard.Key.page_up:
				current_manage_sub_mode="Navigate"
				selected_waypoint=selected_waypoint+1
				print_menu()	
			if key == keyboard.Key.page_down:
					current_manage_sub_mode="Navigate"
					selected_waypoint=selected_waypoint+1
					print_menu()
			if (current_manage_sub_mode=="Modify the selected point x and y cordinates with arrows  c to confirm position (pg_up or pg) _dn to cacel"):		
				if 	key == keyboard.Key.up:
					y=y+stepY
					print_menu()			
				if 	key == keyboard.Key.down:
					y=y-stepY
					print_menu()						
				if 	key == keyboard.Key.right:
					x=x+stepX
					print_menu()
				if 	key == keyboard.Key.left:
					x=x-stepX
					print_menu()

def on_release(key):
	#print('Key released: {0}'.format(
	#	key))
	if key == keyboard.Key.esc:
		print("Existing key capture")
		l.stop()	
		return False



#if __name__ == '__main__':

init_node('input_test')

print_menu()


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
 