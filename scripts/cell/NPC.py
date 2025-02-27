import time

import KBEngine
from KBEDebug import *
import d_units

class NPC(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        # DEBUG_MSG(f"初始化 cell [{type(self).__name__}] id:[{self.id}]")
        # unitInfo = d_units.datas[self.roleID]
        # unit = Combat.Unit(unitInfo)

        # unit.killCallback = self.kill
        # self.unitInfo = unitInfo
        # self.unit = unit

    def onGetWitness(self):
        addProximity(self.atkRange, 0, 0)
        

    def onEnterTrap(self, entityEntering, rangeXZ, rangeY, controllerID, userArg):
        """
        当有实体进入陷阱时被调用
        """
        # DEBUG_MSG("NPC:cell onEnterTrap" + str(self.name))
        # if entityEntering.isDestroyed or entityEntering.getScriptName() != "Avatar" or entityEntering.isDead():
        #     return

        # # 判断攻击cd
        # if time.time() - self.attackStartTime < 1 / self.atkSpeed:
        #     return
        # self.attackStartTime = time.time()
        # self.attackTarget = entityEntering
        # self.attack(entityEntering)

        
    def attack(self, target):
        """
        攻击目标
        """
        # if target.isDead() or self.isDead():
        #     return

        # self.allClients.onAttack()
        # param = Combat.Param(self.unit, target.unit, self.unit.Attack, Combat.DamageType.Physical)
        # Combat.Damage(param)


    def kill(self,unit):
        """
        杀死
        """
        # self.allClients.onDead()
        # # 获得当前空间space实体
        # space = KBEngine.entities[self.spaceID]
        # space.onNPCDeath(self)
        # self.destroy()
