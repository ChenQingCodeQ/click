import KBEngine
from KBEDebug import *

class NPC(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}]")
        self.createCellEntity(self.createToCell)
        
