import d_units
import KBEngine
from KBEDebug import *

TIMER_TYPE_SPAWN = 1

class SpawnPoint(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG(f"初始化 cell [{type(self).__name__}] id:[{self.id}]")
		self.creepID = self.creepSpawnInfo.get('id')
		self.reviveTime = self.creepSpawnInfo.get('reviveTime')
		self.addTimer(1, 0, TIMER_TYPE_SPAWN)

	def spawnTimer(self):
		params = {
			"spawnID": self.id,
			"spawnPos": tuple(self.position),
			"mapID": self.mapID,
			"unitID": self.creepID,
			"reviveTime" : self.reviveTime
		}
		e = KBEngine.createEntity('Monster', self.spaceID, tuple(self.position), tuple(self.direction), params)

	def onTimer(self, tid, userArg):
		if TIMER_TYPE_SPAWN == userArg:
			self.spawnTimer()
		

	def onRestore(self):
		"""
		KBEngine method.
		entity的cell部分实体被恢复成功
		"""
		self.addTimer(1, 0, TIMER_TYPE_SPAWN)
		
	def onDestroy(self):
		"""
		KBEngine method.
		当前entity马上将要被引擎销毁
		可以在此做一些销毁前的工作
		"""
		DEBUG_MSG("onDestroy(%i)" % self.id)
	    
	def onEntityDestroyed(self):
		"""
		defined.
		出生的entity销毁了 需要重建?
		"""
		self.addTimer(self.reviveTime, 0, TIMER_TYPE_SPAWN)
    