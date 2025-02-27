# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	"""
	DEBUG_MSG('onInit::isReload:%s' % isReload)
	
def onGlobalData(key, value):
	DEBUG_MSG('globalData改变: %s' % key)
	
def onGlobalDataDel(key):
	DEBUG_MSG('globalData删除: %s' % key)

def onCellAppData(key, value):
	DEBUG_MSG('cellAppData改变 : %s' % key)
	
def onCellAppDataDel(key):
	DEBUG_MSG('cellAppData删除 : %s' % key)
	
def onSpaceData( spaceID, key, value ):
	"""
	KBEngine method.
	spaceData改变
	"""
	pass
	
def onAllSpaceGeometryLoaded( spaceID, isBootstrap, mapping ):
	"""
	KBEngine method.
	space 某部分或所有chunk等数据加载完毕
	具体哪部分需要由cell负责的范围决定
	"""
	pass