import os
import curses
def menu(title,belowby:int,titlecolor,options,win):
	onselect=0
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
	while(1):
		win.clear()
		win.addnstr(0,0,title,256,titlecolor)
		for i in range(len(options)):
			if i == onselect:
				win.addnstr(i+belowby,0, options[i],256, curses.color_pair(1))
			else:
				win.addnstr(i+belowby,0, options[i],256)
		win.refresh()
		char = win.getch()
		
		win.refresh()
		
		if char == curses.KEY_UP: 
			
			if onselect > 0:
				onselect -= 1
		elif char == curses.KEY_DOWN: 
			
			if onselect < len(options)-1:
				onselect += 1
		
		elif char == curses.KEY_RIGHT:
			return options[onselect]


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
		try:
			files = os.listdir(path)
		except Exception as x:
			curses.endwin()
			print('This program does not have permission to access that directory, perhaps try running it with \'sudo python fileExplorer.py\' instead')
			return 1
		win.clear()
		win.addnstr(0,0,path,256, curses.color_pair(3))
		for i in range(onfile,len(files)):
			if i-onfile+1 == 42: break
		
			if i == onfile: 
				win.addnstr(
					i-onfile+1
					,0,files[i],10, 
					curses.color_pair(1))
		
			else: win.addnstr(
				i-onfile+1,0,
				files[i],10)
		
			if os.path.isdir(
				f'{path}/{files[i]}/'):
					win.addnstr(
						i-onfile+1,15,
						'	Directory\n', 21)
		
			else:
				win.addnstr(
					i-onfile+1,15,
					'	File\n',15)
		
			if notADir: 
				win.addnstr(41,0,
					'NOT A DIRECTORY',25, 
					curses.color_pair(2))
			win.addnstr(os.get_terminal_size()[1]-1,0,
				'Go back a dir[LeftArrow] Enter selected dir[RightArrow] Move up [UpArrow] Move down [DownArrow] Exit [Esc]',256,curses.color_pair(3))
		char = ''
		
		win.refresh()
		
		char = win.getch()
		
		if char == curses.KEY_UP: 
			
			if onfile > 0:
				onfile -= 1
			notADir = False
		
		elif char == curses.KEY_DOWN: 
			
			if onfile < len(files)-1:
				onfile += 1
			notADir = False
		
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
			notADir = False
			path = ''
			for i in range(len(split)-1):
				path += '/'+split[i]
			
			path += '/'
			onfile=0
		elif char == 27:
			options = ["Yes","No"]
			response = menu("Do you want to really exit?",2,curses.color_pair(3),options,win)
			if response == 'Yes':
				break
	curses.endwin()
	print('Program finished with no errors, and a file path of\n'+path)

curses.wrapper(explorer)
