import random
import GlobalConst
import time
from interfaces.Movement import Movement
from Mathf import Vector
from Combat import Param
from Combat import DamageType

import KBEngine
from KBEDebug import *

minWaitTime = GlobalConst.AI_MIN_WAIT_TIME
waitTimeRange = GlobalConst.AI_WAIT_TIME_RANGE


class AI(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.patrolTimer = 0.0                                      # 巡逻计时器
        self.followTimer = 0.0                                      # 跟随计时器

    def onDestroy(self):
        Movement.onDestroy(self)

    def update(self, dt):
        if self.isDead: return
        if self.hateTargetID != -1:
            self._battle()
        else:
            self._patrol(dt)
        
        self.patrolTimer -= dt
        self.followTimer -= dt
        Movement.update(self, dt)

    def _patrol(self,dt):
        # 这里实现AI逻辑
        if self.patrolTimer <= 0.0:
            self.patrolTimer = minWaitTime + random.random() * waitTimeRange
            self.moveRandomPosition()
    
    def _battle(self):
        hateTarget = KBEngine.entities.get(self.hateTargetID)
        # 如果仇恨目标不存在，则清除仇恨
        if hateTarget is None or hateTarget.isDestroyed or hateTarget.isDead:
            self.hateTargetID = -1
            return

        dis = Vector.distance2d(self.uPosition, hateTarget.uPosition)
        if dis <= self.attackRange:
            # 如果距离小于等于攻击范围，则攻击
            self.performAttack(hateTarget)
            self.endNavigation()
        elif self.followTimer <= 0.0:
            self.followTimer = GlobalConst.DATA_FOLLOW_UPDATE_TIME
            self.moveToPosition(hateTarget.uPosition)