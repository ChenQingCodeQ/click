import d_space
import KBEngine
from KBEDebug import *

TIMER_TYPE_SPACE_SPAWN_TICK = 1

class Space(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}]")
        self.avatarList = []
        # 请求在cellbase上创建一个cell空间
        self.createCellEntityInNewSpace(None)
        self.mapID = self.cellData['mapID']
        # KBEngine.globalData[f"Space{self.mapID}"] = self

        # 初始化
        self.initAlloc()


    def initAlloc(self):
        pass

    def onTimer(self, tid, userArg):
        if TIMER_TYPE_SPACE_SPAWN_TICK == userArg:
            creeps = d_space.datas[self.mapID].get('creeps')
            for creepSpawnInfo in creeps:
                KBEngine.createEntityAnywhere("SpawnPoint", {'createToCell':self.cell,'creepSpawnInfo':creepSpawnInfo,'position':creepSpawnInfo['position'],'mapID':self.mapID})
            self.delTimer(tid)

    def onGetCell(self):
        """
        entity的cell部分实体被创建成功
        """
        DEBUG_MSG("Space::onGetCell: %i" % self.id)
        self.addTimer(0.1, 0.1, TIMER_TYPE_SPACE_SPAWN_TICK)
        