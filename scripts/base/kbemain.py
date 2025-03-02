# -*- coding: utf-8 -*-
import os
import KBEngine
import d_space
from KBEDebug import *


def onBaseAppReady(isBootstrap):
	"""
	KBEngine method.
	baseapp已经准备好了
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	INFO_MSG("baseapp已经准备好了")

	if isBootstrap:
		initSpace()

def initSpace():
	for key, value in d_space.datas.items():
		KBEngine.createEntityLocally("Space", {"mapID": key })


def onReadyForLogin(isBootstrap):
	"""
	KBEngine method.
	如果返回值大于等于1.0则初始化全部完成, 否则返回准备的进度值0.0~1.0。
	在此可以确保脚本层全部初始化完成之后才开放登录。
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	return 1.0

def onReadyForShutDown():
	"""
	KBEngine method.
	进程询问脚本层：我要shutdown了，脚本是否准备好了？
	如果返回True，则进程会进入shutdown的流程，其它值会使得进程在过一段时间后再次询问。
	用户可以在收到消息时进行脚本层的数据清理工作，以让脚本层的工作成果不会因为shutdown而丢失。
	"""
	INFO_MSG('onReadyForShutDown()')
	return True

def onBaseAppShutDown(state):
	"""
	KBEngine method.
	这个baseapp被关闭前的回调函数
	@param state: 0 : 在断开所有客户端之前
				  1 : 在将所有entity写入数据库之前
				  2 : 所有entity被写入数据库之后
	@type state: int
	"""
	INFO_MSG('这个baseapp被关闭前的回调函数: state=%i' % state)
		
def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	@param isReload: 是否是被重写加载脚本后触发的
	@type isReload: bool
	"""
	INFO_MSG('当引擎启动后初始化完所有的脚本后这个接口被调用::isReload:%s' % isReload)

def onFini():
	"""
	KBEngine method.
	引擎正式关闭
	"""
	INFO_MSG('引擎正式关闭()')
	
def onCellAppDeath(addr):
	"""
	KBEngine method.
	某个cellapp死亡
	"""
	WARNING_MSG('某个cellapp死亡: %s' % (str(addr)))
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData有改变
	"""
	DEBUG_MSG('全局数据有改变: %s' % key)
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData有删除
	"""
	DEBUG_MSG('全局数据有删除: %s' % key)
	
def onBaseAppData(key, value):
	"""
	KBEngine method.
	baseAppData有改变
	"""
	DEBUG_MSG('baseAppData有改变: %s' % key)
	
def onBaseAppDataDel(key):
	"""
	KBEngine method.
	baseAppData有删除
	"""
	DEBUG_MSG('baseAppData有删除: %s' % key)

def onLoseChargeCB(ordersID, dbid, success, datas):
	"""
	KBEngine method.
	有一个不明订单被处理， 可能是超时导致记录被billing清除， 而又收到第三方充值的处理回调
	"""
	DEBUG_MSG(f'有一个不明订单被处理: ordersID={ordersID}, dbid={dbid}, success={success}, datas={datas}')


