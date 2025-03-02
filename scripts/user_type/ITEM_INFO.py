import KBEngine
from KBEDebug import * 
"""
物品属性数量[3]，最多支持3个属性，空值填0
"""


class TItemInfo(list):
	"""
	"""
	def __init__(self):
		"""
		"""
		list.__init__(self)
		
	def asDict(self):
		data = {
			"UUID"			: self[0],
			"itemId"		: self[1],
			"itemCount"		: self[2],
			"itemIndex"		: self[3],
			"itemAttr1"		: self[4],
			"itemAttr2"		: self[5],
			"itemAttr3"		: self[6],
		}
		
		return data

	def createFromDict(self, dictData):
		self.extend([dictData["UUID"], dictData["itemId"], dictData["itemCount"], dictData["itemIndex"], dictData["itemAttr1"], dictData["itemAttr2"], dictData["itemAttr3"]])
		return self
		
class ITEM_INFO_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TItemInfo().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TItemInfo)

item_info_inst = ITEM_INFO_PICKLER()


class TItemInfoList(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		datas = []
		dct = {"values" : datas}

		for key, val in self.items():
			datas.append(val)
			
		return dct

	def createFromDict(self, dictData):
		for data in dictData["values"]:
			self[data[0]] = data
		return self
		
class AVATAR_INFO_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TItemInfoList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TItemInfoList)

item_info_list_inst = AVATAR_INFO_LIST_PICKLER()