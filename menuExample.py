from simpleMenu import simpleMenu, pause

sMenu = simpleMenu('Main Menu')

#first selection
def option_1():
	print('You have selected the First option')
	pause()

#second selection
def option_2():
	print('You have selected the Second option')
	pause()

#third selection with arguments
def option_args(args):
	print('You have selected the second option')
	print('arg1 is \''+ args[0]+'\' , arg2 is \''+ args[1]+'\'')
	pause()

def option_customKey():
	print('You have selected the option with the letter e')
	pause()

def option_description():
	sMenu.description = 'You have selected the option with the letter d'

def option_indexCheck():
	sMenu.description = 'Index should be 4'


def option_newMenu_selection_depth1( getOptions = False ):
	sMenuBranched = simpleMenu('Branched menu selection')

	def option_description_branched_1():
		sMenuBranched.description = 'You have selected the branched the First option 1'

	def option_description_branched_2():
		sMenuBranched.description = 'You have selected the branched the Second option 1'
	
	sMenuBranched.menu_option_add(option_description_branched_1, 	'First option 1')
	sMenuBranched.menu_option_add(option_description_branched_2, 	'Second option 1')
	sMenuBranched.menu_option_add(option_branched_backOffsetMenu,	'Offset Menu 1')
	sMenuBranched.menu_build()

	return sMenuBranched
	#if(not getOptions):
	#	sMenuBranched.menu_start()
	#else:
	#	return sMenuBranched.get_MenuOptions()

def option_newMenu_selection( getOptions = False ):
	sMenuBranched = simpleMenu('Branched menu selection')

	def option_description_branched_1():
		sMenuBranched.description = 'You have selected the branched the First option'

	def option_description_branched_2():
		sMenuBranched.description = 'You have selected the branched the Second option'
	
	sMenuBranched.menu_option_add(option_description_branched_1, 	'First option')
	sMenuBranched.menu_option_add(option_description_branched_2, 	'Second option')
	sMenuBranched.menu_option_add(option_branched_backOffsetMenu,	'Offset Menu')
	sMenuBranched.add_subMenu( '2', option_newMenu_selection_depth1(), onSelection=True )
	sMenuBranched.menu_build()

	return sMenuBranched
	#if(not getOptions):
	#	sMenuBranched.menu_start()
	#else:
	#	return sMenuBranched.get_MenuOptions()

def option_newMenu_always( getOptions = False ):
	sMenuBranched = simpleMenu('Branched menu always')

	def option_description_branched_1():
		sMenuBranched.description = 'You have selected the branched the First option'

	def option_description_branched_2():
		sMenuBranched.description = 'You have selected the branched the Second option'
	
	sMenuBranched.menu_option_add(option_description_branched_1, 	'First option')
	sMenuBranched.menu_option_add(option_description_branched_2, 	'Second option')
	sMenuBranched.menu_option_add(option_branched_backOffsetMenu,	'Offset Menu')
	return sMenuBranched
	#if(not getOptions):
	#	sMenuBranched.menu_start()
	#else:
	#	return sMenuBranched.get_MenuOptions()


def option_branched_backOffsetMenu():
	sMenuOffset = simpleMenu('Offset menu')

	def option_offset_1():
		sMenuOffset.description = 'You have selected the offset the First option'

	def option_offset_2():
		sMenuOffset.description = 'You have selected the offset the Second option'
	
	sMenuOffset.delBackAndOffset()
	sMenuOffset.menu_option_add( option_offset_1, 'First option' )
	sMenuOffset.menu_option_add( option_offset_2, 'Second option' )
	sMenuOffset.menu_option_add( sMenuOffset.Back, 'Back' )

sMenu.spacing = [ '3','d' ]
sMenu.menu_option_add(option_1, 			'First option' ) #1
sMenu.menu_option_add(option_2, 			'Second option' ) #2
sMenu.menu_option_add(option_args, 			'Option with passed arguments', 	args=['firstArg', 'secondArg'] ) #3
sMenu.menu_option_add(option_customKey, 	'Option with a string selection',	customKey='e' ) #e
sMenu.menu_option_add(option_description, 	'Descrition Option', 				customKey='d' ) #d
sMenu.menu_option_add(option_indexCheck, 	'autoIndexOption check' ) #4
sMenu.menu_option_add(option_newMenu_selection, 		'Branched menu on Select' ) #5
#subMenu = option_newMenu_selection()
sMenu.add_subMenu( '5', option_newMenu_selection(), onSelection=True )
sMenu.menu_option_add(option_newMenu_always, 		'Branched menu allways' ) #6
sMenu.add_subMenu( '6', option_newMenu_always(), always=True )
sMenu.menu_build()
sMenu.menu_start()