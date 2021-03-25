import os
import curses

def explorer(win = curses.initscr()):
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
	win.keypad(True)
	curses.cbreak()
	curses.echo()
	path = '/home/'
	onfile = 0
	notADir = False
	while(1):
		
		files = os.listdir(path)
		win.clear()
		win.addnstr(0,0,path,256, curses.color_pair(3))
		for i in range(onfile,len(files)):
			if i-onfile == 30: break
			if i == onfile: win.addnstr((i-onfile)+1,0,files[i],10, curses.color_pair(1))
			else: win.addnstr((i-onfile)+1,0,files[i],10)
			if os.path.isdir(f'{path}/{files[i]}/'): win.addnstr((i-onfile)+1,15,'	Directory\n', 21)
			else: win.addnstr((i-onfile)+1,15,'	File\n',15)
			if notADir: win.addnstr(30,30,'NOT A DIRECTORY',25, curses.color_pair(2))
		
		char = ''
		win.refresh()
		char = win.getch()
		
		win.refresh()
		
		if char == curses.KEY_UP: 
			if onfile > 0:
				onfile -= 1
		elif char == curses.KEY_DOWN: 
			if onfile < len(files)-1 and onfile < 29:
				onfile += 1
		elif char == curses.KEY_RIGHT:
			if os.path.isdir(f'{str(path)}{files[onfile]}/'): 
				path = f'{path}{files[onfile]}/'
				notADir = False
				onfile=0
			else: notADir = True
		elif char == curses.KEY_LEFT:
			split = path[1:]
			split = split[:len(split)-1]
			split = split.split('/')
			path = ''
			for i in range(len(split)-1):
				path += '/'+split[i]
			path += '/'
			onfile=0
		win.refresh()

curses.wrapper(explorer)
