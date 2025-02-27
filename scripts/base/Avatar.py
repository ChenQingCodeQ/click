import KBEngine
import time
import GlobalConst
import Combat
import random
import d_units
from KBEDebug import *
from Inventory import InventoryMgr
from ITEM_INFO import TItemInfo

class Avatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}]")
		self.cellData["dbid"] = self.databaseID
		self.cellData["level"] = Combat.computeLevel(self.exp)

		self.inventory = InventoryMgr(self)
		self.mapID = self.cellData["mapID"]
		self._destroyTimer = 0
		self.accountEntity = None

	def addExp(self, exp):
		oldLevel = Combat.computeLevel(self.exp)
		self.exp += exp
		newLevel = Combat.computeLevel(self.exp)
		if newLevel > oldLevel:
			self.cell.levelUp(newLevel - oldLevel)
	#--------------------------------------------------------------------------------------------
	#                              requests
	#--------------------------------------------------------------------------------------------
	
	def killUnit(self, unitID):
		data = d_units.datas.get(unitID)
		gold = 		data.get('dropGold')
		exp = 		data.get('dropExp')
		diamond = 	data.get('dropDiamond')
		items = 	data.get('dropItems')
		if gold 	!= None: self.gold += gold
		if exp 		!= None: self.exp += exp
		if diamond 	!= None: self.diamond += diamond
		if items 	!= None: self.inventory.createAndAddItems(items)
		pass
	
	def reqItemInfo(self):
		self.client.onItemInfo(self.inventoryList,self.equipList)
		pass

	def reqEquipItem(self, itemIndex, equipIndex):
		# 装备物品
		if self.inventory.equipItem(itemIndex, equipIndex) == -1:
			self.client.errorInfo(4)  # 装备失败，返回错误信息
			return
		# 通知客户端
		itemUUId = self.inventory.getInvByIndex(itemIndex)
		equipUUId = self.inventory.getEquipByIndex(equipIndex)
		itemInfo = TItemInfo()
		itemInfo.extend([0, 0, 0, itemIndex])
		equipItemInfo = TItemInfo()
		equipItemInfo.extend([0, 0, 0, equipIndex])
		if itemUUId != 0:
			itemInfo = self.inventoryList[itemUUId]
		if equipUUId != 0:
			equipItemInfo = self.equipList[equipUUId]
		self.client.onEquipItem(itemInfo, equipItemInfo)
		# 同步cell
		cell = self.cell
		cell.equipItem(equipItemInfo)

		# for key, info in self.equipItemList.items(): 
		# 	items.getItem(info[1]).use(self)  # 更新装备技能
		pass

	def reqSellItem(self, itemIndex, itemCount):
		rCount = self.inventory.removeItem( itemIndex, itemCount)
		if rCount == -1:
			self.client.errorInfo(4)  # 装备失败，返回错误信息
			return
		for i in range(rCount):
			# 处理出售
			pass
		# self.cell.dropNotify( itemId, itemUUId , itemCount)
		self.client.onSellItem(itemIndex,rCount)
		pass

	def reqUseItem(self, itemIndex, itemCount):
		itemUUId = self.inventory.getItemUidByIndex(itemIndex)
		itemC = self.itemList[itemUUId][2]

		rCount = self.inventory.removeItem( itemIndex, itemCount )
		
		if rCount == -1:
			self.client.errorInfo(4)  # 装备失败，返回错误信息
			pass
		for i in range(rCount):
			# item = items.getItem(self.itemList[itemUUId][1])
			# item.use(self)  # 使用物品
			pass
		self.client.onUseItem(itemIndex,rCount)
		pass

	def reqSwapItem(self, srcIndex, dstIndex):
		self.inventory.swapItem(srcIndex, dstIndex)
		self.client.onSwapItem(srcIndex, dstIndex)
		pass

	def reqRaffle(self, raffleID, raffleCount):
		# 抽奖
		pass

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------

	def onClientEnabled(self):
		DEBUG_MSG(f"客户端已连接 [{type(self).__name__}] id:[{self.id}]")
		self.createCellEntity(KBEngine.globalData[f"Space{self.mapID}"])
		if self._destroyTimer > 0:
			self.delTimer(self._destroyTimer)
			self._destroyTimer = 0
		
	def onClientDeath(self):
		"""
		KBEngine method.
		entity丢失了客户端实体
		"""
		DEBUG_MSG(f"客户端断开连接 [{type(self).__name__}] id:[{self.id}]")
		# 防止正在请求创建cell的同时客户端断开了， 我们延时一段时间来执行销毁cell直到销毁base
		# 这段时间内客户端短连接登录则会激活entity
		self._destroyTimer = self.addTimer(10, 0, GlobalConst.TIMER_TYPE_DESTROY)
			
	def onClientGetCell(self):
		DEBUG_MSG(f"获得cell [{type(self).__name__}] id:[{self.id}]")
		self.cell.resetItem(self.equipList)


	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		if GlobalConst.TIMER_TYPE_DESTROY == userArg:
			self.destroySelf()

	def onDestroy(self):
		DEBUG_MSG(f"entity销毁 [{type(self).__name__}] id:[{self.id}]")
		if self.accountEntity != None:
			self.accountEntity.activeAvatar = None
			self.accountEntity = None

	def destroySelf(self):
		if self.client is not None:
			return
			
		if self.cell is not None:
			# 销毁cell实体
			self.destroyCellEntity()
			return
			
		# 如果帐号ENTITY存在 则也通知销毁它
		if self.accountEntity != None:
			if time.time() - self.accountEntity.relogin > 1:
				self.accountEntity.destroy()
			else:
				DEBUG_MSG("Avatar[%i].destroySelf: relogin =%i" % (self.id, time.time() - self.accountEntity.relogin))
				
		# 销毁base
		if not self.isDestroyed:
			self.destroy()