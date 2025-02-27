import random
import math
import GlobalConst
import Math
import d_items

from Mathf import Vector
from interfaces.AI import AI
from interfaces.Unit import Unit

import KBEngine
from KBEDebug import *


class Monster(KBEngine.Entity,Unit,AI):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        Unit.__init__(self)
        AI.__init__(self)
        DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}] spaceID:[{self.spaceID}]")
        self.isEnable = False

        self.updateTimerID = -1
        self.onDeadCallback = self._onDead

    @property
    def uPosition(self):
        return Math.Vector3(self.position.x, self.position.z, 0)

    @uPosition.setter
    def uPosition(self, position):
        self.position = Math.Vector3(position.x, 0, position.y)

    def enable(self):
        DEBUG_MSG(f"启用 [{type(self).__name__}] id:[{self.id}] spaceID:[{self.spaceID}]")
        if self.isEnable: return
        self.isEnable = True
        if self.updateTimerID == -1:
            self.updateTimerID = self.addTimer(GlobalConst.DATA_MONSTER_DELAY_SPAWN_TIME, GlobalConst.DATA_FIX_UPDATE_TIME, GlobalConst.TIMER_TYPE_UPDATE)
        # 延迟一段时间生成 ，如果离开了视图再激活，刷新这个怪物的属性
        self.addTimer(GlobalConst.DATA_MONSTER_DELAY_SPAWN_TIME, 0, GlobalConst.TIMER_TYPE_SPAWN)
    
    def disable(self):
        DEBUG_MSG(f"禁用 [{type(self).__name__}] id:[{self.id}] spaceID:[{self.spaceID}]")
        if not self.isEnable: return
        self.isEnable = False
        if self.updateTimerID != -1:
            self.delTimer(self.updateTimerID)
            self.updateTimerID = -1

    def update(self,dataTime):
        AI.update(self, dataTime)
        Unit.update(self, dataTime)

    #--------------------------------------------------------------------------------------------
	#                              Unit_Callbacks
	#--------------------------------------------------------------------------------------------
    def _onDead(self):
    	# 死亡
        if self.updateTimerID != -1: 
            self.delTimer(self.updateTimerID)
            self.updateTimerID = -1
        # 通知生成器，自己被销毁，生成器可以重新生成
        if self.spawnID > 0:
            spawner = KBEngine.entities.get(self.spawnID)
            if spawner:
                spawner.onEntityDestroyed()
        self.addTimer(GlobalConst.DATA_MONSTER_DELAY_SPAWN_TIME,0,GlobalConst.TIMER_TYPE_DESTROY)
        # self.destroy()
        
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------

    def onTimer(self, id, userArg):
        if userArg == GlobalConst.TIMER_TYPE_UPDATE:
            self.update(GlobalConst.DATA_FIX_UPDATE_TIME)
        elif userArg == GlobalConst.TIMER_TYPE_DESTROY:
            self.destroy()
        elif userArg == GlobalConst.TIMER_TYPE_SPAWN:
            self.revive()

    def onWitnessed(self,isWitnessed):
        if isWitnessed:
            self.enable()
        else:
            self.disable()

    def onDestroy(self):
        # AI.onDestroy(self)
        pass
