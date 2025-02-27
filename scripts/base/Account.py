# -*- coding: utf-8 -*-
import KBEngine
import random
import time
from KBEDebug import *

class Account(KBEngine.Proxy):
	"""
	账号实体
	客户端登陆到服务端后，服务端将自动创建这个实体，通过这个实体与客户端进行交互
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		DEBUG_MSG(f"初始化 [{type(self).__name__}] id:[{self.id}]")
		self.activeAvatar = None
		self.relogin = time.time()

	def reqAvatarInfo(self):
		"""
		exposed.
		客户端请求角色信息
		"""
		DEBUG_MSG("Account[%i].reqAvatarInfo" % self.id)
		self.client.onReqAvatarInfo(self.playerName)

	def reqSetAvatar(self, name):
		"""
		exposed.
		客户端请求设置角色名
		"""
		if len(name) <= 2:
			DEBUG_MSG("名称太短")
			self.client.onReqAvatarInfo(3, "名称太短")
			return

		props = {
			"locked"			: 0,
			"name"				: name,
			"exp"				: 0,
			"gold"				: 0,
			"diamond"			: 0,
			"mapID"				: 10001,
			"direction"			: (0, 0, 0),
			"position"			: (0, 0, 0),
		}
			
		avatar = KBEngine.createEntityLocally('Avatar', props)
		if avatar:
			avatar.writeToDB(self._onAvatarSaved)
		
		DEBUG_MSG("Account:[%i] name:%s." % (self.id, name))
	
	def selectAvatarGame(self):
		"""
		exposed.
		客户端选择角色进行游戏
		"""
		DEBUG_MSG("Account[%i].selectAvatarGame:%i. self.activeAvatar=%s" % (self.id, self.dbid, self.activeAvatar))
		# 注意:使用giveClientTo的entity必须是当前baseapp上的entity
		if self.activeAvatar:
			self.giveClientTo(self.activeAvatar)
		else:
			KBEngine.createEntityFromDBID("Avatar", self.dbid, self._onAvatarCreated)
			


	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------

	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG("Account[%i]::onLogOnAttempt: ip=%s, port=%i, selfclient=%s" % (self.id, ip, port, self.client))

		# 如果一个在线的账号被一个客户端登陆并且onLogOnAttempt返回允许
		# 那么会踢掉之前的客户端连接
		# 那么此时self.activeAvatar可能不为None， 常规的流程是销毁这个角色等新客户端上来重新选择角色进入
		if self.activeAvatar:
			if self.activeAvatar.client is not None:
				self.activeAvatar.giveClientTo(self)

			self.relogin = time.time()
			self.activeAvatar.destroySelf()
			self.activeAvatar = None
			
		return KBEngine.LOG_ON_ACCEPT


	def onClientEnabled(self):
		DEBUG_MSG(f"客户端已连接 [{type(self).__name__}] id:[{self.id}]")


	def onClientDeath(self):
		DEBUG_MSG(f"客户端实体销毁 [{type(self).__name__}] id:[{self.id}]")
		if self.activeAvatar:
			self.activeAvatar.accountEntity = None
			self.activeAvatar = None

		self.destroy()		
		
	def onDestroy(self):
		"""
		entity销毁
		"""
		DEBUG_MSG(f"entity销毁 [{type(self).__name__}] id:[{self.id}]")
		
		if self.activeAvatar:
			self.activeAvatar.accountEntity = None

			try:
				self.activeAvatar.destroySelf()
			except:
				pass
				
			self.activeAvatar = None
			
	def _onAvatarCreated(self, baseRef, dbid, wasActive):
		"""
		选择角色进入游戏时被调用
		"""
		INFO_MSG(type(baseRef))
		if baseRef is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): 您要创建的角色不存在！" % (self.id))
			return
		if wasActive:
			avatar = baseRef
			# ERROR_MSG("Account::__onAvatarCreated:(%i): 这个角色现在在世界上！" % (self.id))
		else:
			avatar = KBEngine.entities.get(baseRef.id)

		if avatar is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
			return
		
		if self.isDestroyed:
			ERROR_MSG("Account::__onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
			avatar.destroy()
			return
			
		avatar.accountEntity = self
		self.activeAvatar = avatar
		self.giveClientTo(avatar)
		
	def _onAvatarSaved(self, success, avatar):
		"""
		新建角色写入数据库回调
		"""
		INFO_MSG('新建角色写入数据库回调:(%i) create avatar state: %i, %s, %i' % (self.id, success, avatar.cellData["name"], avatar.databaseID))
		
		# 如果此时账号已经销毁， 角色已经无法被记录则我们清除这个角色
		if self.isDestroyed:
			if avatar:
				avatar.destroy(True)
			return
			
		result = "创建成功"
		if success:
			self.playerName = avatar.cellData["name"]
			self.dbid = avatar.databaseID
			self.writeToDB()
		else:
			result = "创建失败了"

		avatar.destroy()
		
		if self.client:
			self.client.onSetAvatarResult(result)
