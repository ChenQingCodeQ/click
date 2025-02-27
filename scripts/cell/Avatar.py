import KBEngine
import Math
import Combat
from KBEDebug import *
import GlobalConst
import d_items
from interfaces.Unit import Unit
from Mathf import Vector

class Avatar(KBEngine.Entity,Unit):
	def __init__(self):
        # 调用KBEngine.Entity的初始化方法
		KBEngine.Entity.__init__(self)
        # 调用Unit的初始化方法
		Unit.__init__(self)
        # 打印初始化信息
		DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}]")
		self.updateTimerID = -1										# 更新定时器ID
		self.proxHateID = -1                                        # 仇恨代理ID
		self.equipItemInfos = []                                 	# 装备列表

		self.onKillCallback = self._onKill
		self.onDeadCallback = self._onDead
		self.onReviveCallback = self._onRevive

	def isPlayer(self): 
		return True
	
	@property
	def uPosition(self):
		return Math.Vector3(self.position.x, self.position.z, 0)

	@uPosition.setter
	def uPosition(self, position):
		self.position = Math.Vector3(position.x, 0, position.y)
	
	def update(self, dt):
		# 获取当前敌对目标的ID
		self.hateTargetID = self.getDirectTargetID()
		# 如果没有敌对目标，直接返回
		if self.hateTargetID == -1: return
		# 根据敌对目标ID获取敌对目标实体
		hateTarget = KBEngine.entities.get(self.hateTargetID)
		# 如果敌对目标不存在、被销毁或已死亡，直接返回
		if hateTarget == None or hateTarget.isDestroyed or hateTarget.isDead: return
		# 计算当前实体与敌对目标之间的二维距离
		dis = Vector.distance2d(self.uPosition, hateTarget.uPosition)
		# 如果距离在攻击范围内，执行攻击操作
		if dis <= self.attackRange: 
			self.performAttack(hateTarget)
			self.attack = self.attack + 1.0
		# 结束函数，无实际作用
		pass
	
	#--------------------------------------------------------------------------------------------
	#                              item
	#--------------------------------------------------------------------------------------------
	# itemInfo => [UUID, itemId, itemCount, itemIndex, itemAttr1, itemAttr2, itemAttr3]
	def resetItem(self,equipInfoList):
		self.equipItemInfos = equipInfoList
		for itemInfo in equipInfoList:
			self.equipItem(itemInfo)
	
	def equipItem(self, itemInfo):
		index = itemInfo[3]
		oldItemInfo = self.equipItemInfos[index]
		oldItemId = oldItemInfo[1]
		newItemId = itemInfo[1]
		if oldItemInfo != 0:
			data = d_items.datas.get(oldItemId)
			if oldItemInfo[4] != 0: self.updateAttr(data['attrKey1'], -oldItemInfo[4])
			if oldItemInfo[5] != 0: self.updateAttr(data['attrKey2'], -oldItemInfo[5])
			if oldItemInfo[6] != 0: self.updateAttr(data['attrKey3'], -oldItemInfo[6])
		if newItemId != 0:
			data = d_items.datas.get(newItemId)
			if itemInfo[4] != 0: self.updateAttr(data['attrKey1'], itemInfo[4])
			if itemInfo[5] != 0: self.updateAttr(data['attrKey2'], itemInfo[5])
			if itemInfo[6] != 0: self.updateAttr(data['attrKey3'], itemInfo[6])
		self.equipItemInfos[index] = itemInfo
		pass
	
	def levelUp(self, levelUp):
		Unit.levelUp(self, levelUp)
		pass

	#--------------------------------------------------------------------------------------------
	#                              Unit
	#--------------------------------------------------------------------------------------------
	def _onKill(self,victim):
		if victim.entityName == "Avatar":
			# self.addExp(param.exp)
			pass
		elif victim.entityName == "Monster":
			self.base.killUnit(victim.unitID)

	def _onRevive(self):
		if self.proxHateID == -1:
			self.proxHateID = self.addProximity(GlobalConst.DATA_HATE_RANGE, 0, GlobalConst.TRAP_TYPE_HATE)
		if self.updateTimerID == -1:
			self.updateTimerID = self.addTimer(GlobalConst.DATA_FIX_UPDATE_TIME, GlobalConst.DATA_FIX_UPDATE_TIME, GlobalConst.TIMER_TYPE_UPDATE)
	
	def _onDead(self):
		if self.proxHateID != -1:
		    self.cancelController(self.proxHateID)
		    self.proxHateID = -1

		if self.updateTimerID != -1:
			self.cancelTimer(self.updateTimerID)
			self.updateTimerID = -1

		if len(self.hateTargetIDs) > 0:
			for targetID in self.hateTargetIDs:
				KBEngine.entities.get(targetID).removeTarget(self.id)

		self.hateTargetIDs = []
		self.hateTargetID = -1
		pass

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, id, userArg):
		if self.isDead: return
		if userArg == GlobalConst.TIMER_TYPE_UPDATE:
			self.update(GlobalConst.DATA_FIX_UPDATE_TIME)
			Unit.update(self, GlobalConst.DATA_FIX_UPDATE_TIME)

	def onGetWitness(self):
		DEBUG_MSG(f"绑定观察者 [{type(self).__name__}] id:[{self.id}]")
		self.revive()

	def onLoseWitness(self):
		DEBUG_MSG(f"解绑观察者 [{type(self).__name__}] id:[{self.id}]")
		self.forceKill()

	def onEnterTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
		if userArg == GlobalConst.TRAP_TYPE_HATE:
			# 如果 实体被摧毁 || 实体死亡 || 自己死亡
			if hasattr(entity, 'isDead') == False or entity.isDead or self.isDead: return
			entity.addTarget(self.id)
			self.addTarget(entity.id)
		        
	def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg ):
		if userArg == GlobalConst.TRAP_TYPE_HATE:
			# 如果 实体没被摧毁
			if hasattr(entity, 'isDead') and not entity.isDestroyed:
				entity.removeTarget(self.id)
			
			self.removeTarget(entity.id)

	def onDestroy(self):
		DEBUG_MSG(f"entity销毁 [{type(self).__name__}] id:[{self.id}]")
	