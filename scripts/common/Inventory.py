import weakref
import KBEngine
from KBEDebug import *
import random
import d_items
from ITEM_INFO import TItemInfo
import GlobalConst

# TItemInfo = [itemUUID, itemId, itemCount, invIndex]
# invIndex2Uids = [itemIndex: UUID]
# equipIndex2Uids = [itemIndex: UUID]
# entity.itemList = {itemUUID: TItemInfo}
# entity.equipItemList = {itemUUID: TItemInfo}



class InventoryMgr:
	def __init__(self, entity):
		self._entity = weakref.proxy(entity)
		#初始化背包索引index to Uid
		self.invIndex2Uids = [0]*GlobalConst.MAX_INV_SIZE
		for key, info in self._entity.inventoryList.items():
			self.invIndex2Uids[info[3]] = key

		#初始化装备索引index to Uid
		self.equipIndex2Uids = [0]*GlobalConst.MAX_EQUIP_SIZE
		for key, info in self._entity.equipList.items():
			self.equipIndex2Uids[info[3]] = key


	# 创建并添加 返回添加失败的物品
	def createAndAddItems(self, itemDatas):
		result = InventoryMgr.createItemByData(itemDatas)
		return self.addItems(result)
	

	def createItemByData(itemDatas):
		result = []
		for itemId, info in itemDatas.items():
			probability = info.get('probability')
			if random.randint(0, 100) < probability:
				count = info.get('count')
				item = InventoryMgr.createItem(itemId, random.randint(count[0], count[1]))
				result.extend(item)
		return result
	
	# 创建物品
	def createItem(itemId, itemCount = 1):
		result = []
		# 物品设定堆叠数量
		data = d_items.datas[itemId]
		itemStack = data['stack']
		# 堆叠数量为1，不可堆叠，可能存在属性（装备类）。大于1，可堆叠，不存在属性
		if itemStack == 1:
			# 不可堆叠物品
			itemUUID = KBEngine.genUUID64()
			iteminfo = TItemInfo()
			listInfo = [itemUUID, itemId, itemCount, 0]
			attr1 = data.get('attrValue1')
			attr2 = data.get('attrValue2')
			attr3 = data.get('attrValue3')
			if attr1 != None:
				value = random.uniform(attr1[0], attr1[1])
				listInfo.append(value)
			if attr2 != None:
				value = random.uniform(attr2[0], attr2[1])
				listInfo.append(value)
			if attr3 != None:
				value = random.uniform(attr3[0], attr3[1])
				listInfo.append(value)
			iteminfo.extend(listInfo)
			result.append(iteminfo)
		else:
			# 添加数量大于堆叠上限
			full_stacks = itemCount // itemStack
			for i in range(full_stacks):
				itemUUID = KBEngine.genUUID64()
				iteminfo = TItemInfo()
				iteminfo.extend([itemUUID, itemId, itemStack, i])
				result.append(iteminfo)

			# 添加数量小于堆叠上限
			if itemCount % itemStack > 0:
				itemUUID = KBEngine.genUUID64()
				iteminfo = TItemInfo()
				iteminfo.extend([itemUUID, itemId, itemCount % itemStack, full_stacks])
				result.append(iteminfo)
			pass
		return result

	# 添加物品 返回添加失败的物品
	def addItems(self, itemInfos):
		result = []
		for itemInfo in itemInfos:
			if self.addItem(itemInfo) == False:
				result.append(itemInfo)
		return result
	
	# 添加物品 返回成功或失败
	def addItem(self, itemInfo):
		result = []
		emptyIndex = self.getEmptyInvIndex()
		# 背包已经满了
		if emptyIndex == -1: return False
		itemUUID = itemInfo[0]
		itemId = itemInfo[1]
		data = d_items.datas[itemId]
		itemInfo[3] = emptyIndex
		self.invIndex2Uids[emptyIndex] = itemUUID
		self._entity.inventoryList[itemUUID] = itemInfo
		return True

    # 移除物品
	def removeItem(self, itemIndex, itemCount):
		"""
		移除物品
		返回移除的物品数量
		"""
		itemUUID = self.invIndex2Uids[itemIndex]
		if itemUUID == 0:
			return -1

		itemId = self._entity.inventoryList[itemUUID][1]
		itemC = self._entity.inventoryList[itemUUID][2]
		itemIndex = self._entity.inventoryList[itemUUID][3]
		if itemCount < itemC:
			self._entity.inventoryList[itemUUID][2] = itemC - itemCount
		else:
			self.invIndex2Uids[itemIndex] = 0
			del self._entity.inventoryList[itemUUID]
			itemCount = itemC
		return itemCount

	# 交换物品
	def swapItem(self, srcIndex, dstIndex):
		srcUid = self.invIndex2Uids[srcIndex]
		dstUid = self.invIndex2Uids[dstIndex]
		self.invIndex2Uids[srcIndex] = dstUid
		if dstUid != 0:
			self._entity.inventoryList[dstUid][3] = srcIndex
		self.invIndex2Uids[dstIndex] = srcUid
		if srcUid != 0:
			self._entity.inventoryList[srcUid][3] = dstIndex

	# 装备或脱下
	def equipItem(self, itemIndex, equipIndex):
		invUid = self.invIndex2Uids[itemIndex]
		equipUid = self.equipIndex2Uids[equipIndex]
		#背包索引位置没有物品
		if invUid == 0 and equipUid == 0:
			return -1
		
		equipItem = {}
		if equipUid != 0:
			equipItem = self._entity.equipList[equipUid]
			del self._entity.equipList[equipUid]
			self.equipIndex2Uids[equipIndex] = 0

		if invUid != 0:
			self._entity.equipList[invUid] = self._entity.inventoryList[invUid]
			self._entity.equipList[invUid][3] = equipIndex
			self.equipIndex2Uids[equipIndex] = invUid
			del self._entity.inventoryList[invUid]
			self.invIndex2Uids[itemIndex] = 0

		if equipUid != 0:
			self._entity.inventoryList[equipUid] = equipItem
			self._entity.inventoryList[equipUid][3] = itemIndex
			self.invIndex2Uids[itemIndex] = equipUid
    
    # 获取背包索引物品
	def getInvByIndex(self, itemIndex):
		return self.invIndex2Uids[itemIndex]
	
    # 获取装备索引物品
	def getEquipByIndex(self, equipIndex):
		return self.equipIndex2Uids[equipIndex]

	# 获取空背包索引
	def getEmptyInvIndex(self):
		for emptyIndex in range(0, GlobalConst.MAX_INV_SIZE):
			if self.invIndex2Uids[emptyIndex] == 0:
				return emptyIndex
		return -1

	# 处理物品溢出
	def handleItemOverflow(self, itemId, count):
		result = []