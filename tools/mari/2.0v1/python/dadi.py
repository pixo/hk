import mari
import PythonQt

gui = PythonQt.QtGui 
core = PythonQt.QtCore 

"""Flip PaintBuffer"""
def paintBufferFlip( scaleFactor ):
    paintBuffer = mari.canvases.paintBuffer()
    scale = paintBuffer.scale()
    scale = core.QSizeF( scale.width() * scaleFactor[0], scale.height() * scaleFactor[1] )
    paintBuffer.setScale( scale )
    
"""Bake PaintBuffer
def paintBufferBake():
    paintBuffer = mari.canvases.paintBuffer()
    scale = paintBuffer.scale()
    paintBuffer.bake()
    paintBuffer.setScale( scale )
"""    

"""Create PaintBuffer menu Actions"""
def createPaintBufferActions():
    description="Paint Buffer %s"
    
    #create actions
    actionFlipX = mari.actions.create( '/Dadi/PaintBuffer/Flip Horizontally', 'paintBufferFlip((-1,1))' )
    actionFlipY = mari.actions.create( '/Dadi/PaintBuffer/Flip Vertically', 'paintBufferFlip((1,-1))' )
    
    #add actions to the Dadi menu
    mari.menus.addAction( actionFlipX, "MainWindow/D&adi/&Paint Buffer" )
    mari.menus.addAction( actionFlipY, "MainWindow/D&adi/&Paint Buffer" )
    
    #create shorcut
    actionFlipX.setShortcut("Shift+F")
    actionFlipY.setShortcut("Shift+Alt+F")

"""Create Clean Actions """
def createClearActions():
    """clear garbage collector """
    actionClearGabarge = mari.actions.create( '/Dadi/Clear/Garbage Collection', 'mari.ddi.garbageCollect()' )
    mari.menus.addAction( actionClearGabarge, "MainWindow/D&adi/&Clear" )
    
    """clear history """
    actionClearHistory = mari.actions.create('Dadi/Clear/History','mari.projects.current().save();mari.history.clear(show_dialog=True)')
    mari.menus.addAction( actionClearHistory, "MainWindow/D&adi/&Clear" )

""" Create Pixo's Actions"""
def createActions():
    createPaintBufferActions()
    createClearActions()

createActions()
