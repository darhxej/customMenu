import os 
import functools
from msvcrt import getch
import this
#clear terminal
class IterableArray:
	def __init__( self, arr ):
		self.arr = arr
		self.index = 1
		self.index_max = len( self.arr ) - 1
		self.used = False

	def next( self ):
		self.used = True
		if self.index == self.index_max:
			self.index = 0
			return self.arr[ self.index ]
		self.index += 1
		return self.arr[ self.index ]
	
	def prev( self ):
		self.used = True
		if self.index == 0:
			self.index = len( self.arr )
		self.index -= 1
		return self.arr[ self.index ]

	def restart( self ):
		self.index = 1
	def get(self):
		return self.arr[ self.index ]
	def is_max(self):
		return self.index == self.index_max
	def is_min(self):
		return self.index == 0

def getInput():
	userInput = ''
	while True:
		ch = getch()
		if ( ch == b'H' or ch == b'K' ):
			return 'Prev'
		elif ( ch == b'P' or ch == b'M' ):
			return 'Next'
		elif ( ch == b'\r' ):
			return userInput
		elif ( ch == b'\xe0' ):
			pass
		elif( ch == b'\b' ):
			if ( len( userInput ) > 0 ):
				userInput = userInput[:-1]
				print( '\b \b', end = '', flush = True )
		else:
			userInput += ch.decode()
			print( ch.decode(), end = '', flush = True )

#clear terminal
def clearScreen( ):
	os.system('cls' if os.name == 'nt' else 'clear')

#wait for user to press enter
def pause( text = 'Press enter to continue...'):
	input( text )

class simpleMenu( ):
	#default back function that enables loop exit
	def Back( self ):
		self.run = False

	#deletes the first default option and sets the offset to 1
	def delBackAndOffset( self ):
		del self.menuOptions[ '0' ]
		self.currentAutoIndex = 1

	def reset( self, title ):
		#sets default values
		#creates menuOptions used to store the functions related to the menu
		#creates menuNames that stores user readable name
		#with the same index as the function related to it

		self.menuOptions = 	{ '0': [ self.Back, 'Back' ] }
		if ( title != '' ):
			self.title = title
		
		#prints afther the menu
		self.description = ''

		#should it still run
		self.run = True

		#for breaking outside the loop
		self.breaking = False

		#for adding space in between the option
		self.spacing = []

		#for currect indexing when a str is added as a key
		self.currentAutoIndex = 1

		#currently selected key
		self.selection = ''

		self.menuOptionsExtra = {}

		self.menuOptionsExtra_onSelection  = {}
		self.menuOptionsExtra_always = {}
		self.menuPrintableList = []
		self.parent=None
	def __init__( self, title, defaultFunction = False, depth=0 ):
		#sets title calls reset to set values
		self.title = title
		self.reset( title )
		self.defaultFunction = defaultFunction
		self.depth = depth
	def add_subMenu(self, key, subMenu, onSelection=False, always=False):
		subMenu.depth= self.depth+1
		subMenu.add_subMenu_depths()
		subMenu.menu_build()
		subMenu.set_menuPrintableList()
		subMenu.parent = self
		self.menuOptionsExtra[key] = subMenu
		if(onSelection):
			self.menuOptionsExtra_onSelection[key] = True
		if(always):
			self.menuOptionsExtra_always[key]=True
	def add_subMenu_depths(self):
		for key,subMenu in self.menuOptionsExtra.items():
			subMenu.depth = self.depth + 1
			subMenu.menu_build()
			subMenu.set_menuPrintableList()
	def add_dict_menuOptionsExtra( self, key, arr, ignoreList = ['Back']):
		self.menuOptionsExtra[key] = arr
	''''
		for value in arr:
			if (value not in ignoreList):
				if ( self.menuOptionsExtra.get( key, False ) ):
					self.menuOptionsExtra[ key ].append(value)
				else:
					self.menuOptionsExtra[ key ] = [value]
	'''

	def add_menuOptionsExtra( self, key, value ):
		if ( self.menuOptionsExtra.get( key, False ) ):
			self.menuOptionsExtra[ key ].append(value)
		else:
			self.menuOptionsExtra[ key ] = [value]

	def get_MenuOptions(self):
		return self.menuOptions

	def outside_loop_break(self):
		self.run = False
		self.breaking = True

	def change_back_to_outside_loop_break(self, name = 'Back'):
		self.menuOptions['0'] = [ self.outside_loop_break, name ]

	def change_backFunction( self, key, func, name, args=False ):
		#replaces key value function for the first value
		if( args ):
			func_custom = functools.partial( func, args )
		else:
			func_custom = func
		
		self.menuOptions[ key ] = self.menuOptions['0']
		del self.menuOptions['0']
		self.menuOptions[ key ] = [ func_custom,name ]

	def menu_option_add( self, func, name, customKey=False, args=False ):
		#adds a new function to menuOptions with a int key
		#and stores a user readable name with same index
		
		#checks if args are present
		if( args ):
			func_custom = functools.partial( func, args )
			
		else:
			func_custom = func
		
		if( customKey ):
			self.menuOptions.update( { str(customKey) : [ func_custom,name ] } )
		
		else:
			#sets the key value to be the next number in line
			self.menuOptions.update( { str(self.currentAutoIndex) : [ func_custom, name ] } )
			self.currentAutoIndex += 1
	
	def menu_option_remove( self, key ):
		del self.menuOptions[ key ]

	def defaultFunction_SetTo( self, func, args = False):
		if( args ):
			func_custom = functools.partial( func, args )
		else:
			func_custom = func
		self.defaultFunction = func_custom

	def set_menuPrintableList(self, choiceOverwrite=None):
		self.menuPrintableList=[]
		for key,value in self.menuOptions.items():
			temp=' '*(6*self.depth)
			if(self.choiceIteration.get() == str( key ) and choiceOverwrite==None):
				temp += '->'
			elif(choiceOverwrite== str( key )):
				temp += '->'
			else:
				temp += '  '
			temp += '[' + str(key) + ']'
			self.menuPrintableList.append ( temp + '' + value[1] )
			if (self.menuOptionsExtra.get( self.choiceIteration.get(), False ) and self.choiceIteration.get() == str( key )):
				subMenu=self.menuOptionsExtra[self.choiceIteration.get()]
				for item in subMenu.menuPrintableList:
					self.menuPrintableList.append ( item )
	
	def menu_print( self):
		#prints the title and adds '-' as a seperator
		#with the length as the title
		print( self.title )
		seperator = ''
		for _ in self.title:
			seperator +='-'
		print( seperator )
		#prints all the use readable names
		#in format '[key] name'
		#print(self.menuOptions)
		'''for key,value in self.menuOptions.items():
			
			if( currentSelection == str( key ) ):
				temp = '->'
			else:
				temp = '  '
			temp += '[' + str(key) + ']'
			print ( temp, value[1] )
			if 	( self.menuOptionsExtra.get( key, False ) and ( self.menuOptionsExtra_onSelection.get( currentSelection, False ) or self.menuOptionsExtra_always.get( key, False ))):
				for keyExtra,valueExtra in self.menuOptionsExtra[key].items():
					print(' '*( 6*self.extraIndentation + len( str(keyExtra) )) +'[' + str(keyExtra) + ']', valueExtra[1])
			if key in self.spacing:
				print()'''
		
		#self.set_menuPrintableList()
		for menuItem in self.menuPrintableList:
			print(menuItem)
		print()
		print( self.description )
		self.description = ''
	
	def set_Iterator(self):
		self.choiceIteration = IterableArray( list( self.menuOptions.keys() ) )

	def setInput(self,inp,childInp=False):
		if (self.menuOptionsExtra.get( self.choiceIteration.get(), False ) and not childInp):
			self.menuOptionsExtra[self.choiceIteration.get()].setInput(inp)
			self.set_menuPrintableList()
			return
		if ( inp == 'Next'):
			if (self.choiceIteration.is_max()):
				self.parent.setInput(inp, childInp=True)
			else:
				self.choiceIteration.next()
				self.set_menuPrintableList()
		elif ( inp == 'Prev'):
			if (self.choiceIteration.is_min()):
				self.parent.setInput(inp, childInp=True)
			else:
				self.choiceIteration.prev()
				self.set_menuPrintableList()
		else:
			if( inp != '' ):
				menuOption = self.menuOptions.get( inp, False )
			else:
				menuOption = self.menuOptions.get( self.choiceIteration.get(), False )
				#self.select()
			if( menuOption ):
				menuOption[ 0 ]()
			else:
				print( inp, 'is not on list' )
				pause()
		
	def menu_build(self):
		self.set_Iterator()
		self.set_menuPrintableList()

	def menu_start( self ):
		while ( True ):
			#if the loop should still run
			if(self.run):
				
				#clears terminal
				clearScreen()

				if(self.defaultFunction):
					self.defaultFunction()
				
				#prints the menu
				self.menu_print()
				print( 'Choice -> ', end = '', flush = True )
				inp = getInput()
				#send next, prev, enter to child
				self.setInput(inp)
				'''
				if ( inp == 'Next'):
					self.next()
				elif ( inp == 'Prev'):
					self.prev()
				else:
					if( inp != '' ):
						menuOption = self.menuOptions.get( inp, False )
					else:
						menuOption = self.menuOptions.get( self.choiceIteration.get(), False )
						#self.select()
					if( menuOption ):
						menuOption[ 0 ]()
					else:
						print( inp, 'is not on list' )
						pause()'''

			else:
				break