# -*- coding: utf-8 -*-
import random
import KBEngine
import time
import math
import d_units
import Combat
from Mathf import Vector
from KBEDebug import * 
from Combat import Param
from Combat import DamageType

TAG_PLAYER = 1      # 玩家
TAG_MONSTER = 2     # 怪物
TAG_BOSS = 4        # BOSS
TAG_ELITE = 8       # 精英怪


class Unit:
    def __init__(self):
        self.entityName = type(self).__name__
        # 单位标签
        if self.entityName == "Avatar":
            # 设敌人标签
            self.enemyTag = TAG_MONSTER + TAG_BOSS + TAG_ELITE
            self.thisTag = TAG_PLAYER
        elif self.entityName == "Monster":
            # 设敌人标签
            self.enemyTag = TAG_PLAYER
            self.thisTag = TAG_MONSTER

        # 初始化事件回调函数
        self.onMissCallback = None                         # 闪避回调
        self.onCritCallback = None                         # 暴击回调
        self.onDamageCallback = None                       # 受到伤害回调
        self.onDamageAfterCallback = None                  # 受到伤害后回调
        self.onKillCallback = None                         # 击杀回调
        self.onDeadCallback = None                         # 死亡回调
        self.onReviveCallback = None                       # 复活回调

        self.isDead = True                                 # 是否死亡
        self.hateTargetID = -1                             # 仇恨目标ID
        self.hateTargetIDs = []                            # 仇恨ID列表

    def resetAttr(self):
        datas = d_units.datas.get(self.unitID)
        if datas is None:
        	ERROR_MSG("SpawnPoint::spawn:%i not found." % self.creepID)
        	return
        self.name = datas["name"]                         # 名称
        DEBUG_MSG("Unit::resetAttr:%s" % self.name)
        # 添加属性
        self.attack = datas["attack"]                     # 攻击力
        self.health = datas["health"]                     # 生命值
        self.armor = datas["armor"]                       # 护甲值
        self.mana = datas["mana"]                         # 魔法值
        self.attackSpeed = datas["attackSpeed"]           # 攻击速度
        self.movementSpeed = datas["movementSpeed"]       # 移动速度
        self.attackRange = datas["attackRange"]           # 攻击范围
        self.healthRegen = datas["healthRegen"]           # 生命回复
        self.manaRegen = datas["manaRegen"]               # 魔法回复

        self.hit = 100.0                                  # 命中
        self.dodge = 20.0                                 # 闪避
        self.critRate = 0.05                              # 暴击率
        self.critDamage = 1.5                             # 暴击伤害 基础为150%
        self.physicalDamage = 0.0                         # 物理伤害加成 基础为0%
        self.flamedamage = 0.5                            # 火焰伤害加成 基础为50%
        self.iceDamage = 0.5                              # 冰冻伤害加成 基础为50%
        self.poisonDamage = 0.5                           # 中毒伤害加成 基础为50%
        self.damageBonus = 0.0                            # 伤害加成
        self.damageReduction = 0.0                        # 伤害减免
        self.cooldownBoost = 0.0                          # 冷却减少
        self.attackBoost = 0.0                            # 攻击提高
        self.armorBoost = 0.0                             # 护甲提高
        self.healthBoost = 0.0                            # 生命提高
        self.manaBoost = 0.0                              # 魔法提高
        self.attackSpeedBoost = 0.0                       # 攻击速度提高
        self.movementSpeedBoost = 0.0                     # 移动速度提高

        # 等级成长
        grow = Combat.UnitGrow(self.level, datas.get('healthUp'), datas.get('healthCoe'), datas.get('attackUp'), datas.get('healthCoe'), datas.get('armorUp'))
        self.attack += grow.attack                         # 攻击力
        self.health += grow.health                         # 生命值
        self.armor += grow.armor                           # 护甲值
        self.unitGrow = grow
        pass

    def levelUp(self, levelUp):
        self.level += levelUp
        oldGrow = self.unitGrow
        newGrow = Combat.UnitGrow(self.level, oldGrow.healthUp, oldGrow.healthCoe, oldGrow.attackUp, oldGrow.attackCoe, oldGrow.armorUp)

        self.attack = newGrow.attack - oldGrow.attack      # 攻击力
        self.health = newGrow.health - oldGrow.health      # 生命值
        self.armor = newGrow.armor - oldGrow.armor         # 防御力
        self.unitGrow = newGrow
        pass

# #region 属性
    def updateAttr(self,key,value): self.__dict__[key] += value

    @property
    def Attack(self): return self.attack * (1 + self.attackBoost)  # 最终攻击

    @property
    def Armor(self): return self.armor * (1 + self.armorBoost)  # 最终护甲

    @property
    def Health(self): return self.health * (1 + self.healthBoost)  # 最终生命

    @property
    def Mana(self): return self.mana * (1 + self.manaBoost)  # 最终魔法

    @property
    def HealthRegen(self): return self.healthRegen  # 最终生命回复

    @property
    def ManaRegen(self): return self.manaRegen  # 最终魔法回复

    @property
    def Hit(self): return self.hit  # 最终命中

    @property
    def Dodge(self): return self.dodge  # 最终闪避

    @property
    def AttackSpeed(self): return self.attackSpeed * (1 + self.attackSpeedBoost)  # 最终攻击速度

    @property
    def MovementSpeed(self): return self.movementSpeed * (1 + self.movementSpeedBoost)  # 最终移动速度

    @property
    def AttackRange(self): return self.attackRange  # 最终攻击范围

    @property
    def CritRate(self): return self.critRate  # 最终暴击率

    @property
    def CritDamage(self): return self.critDamage  # 最终暴击伤害

    @property
    def PhysicalDamage(self): return self.physicalDamage  # 最终物理伤害加成

    @property
    def FlameDamage(self): return self.flamedamage  # 最终火焰伤害加成

    @property
    def IceDamage(self): return self.iceDamage  # 最终冰冻伤害加成

    @property
    def PoisonDamage(self): return self.poisonDamage  # 最终中毒伤害加成

    @property
    def DamageBonus(self): return self.damageBonus  # 最终伤害加成

    @property
    def DamageReduction(self): return self.damageReduction  # 最终伤害减免

    @property
    def CooldownBoost(self): return self.cooldownBoost  # 最终冷却减少
# #endregion

    @property
    def CurrentHealth(self): return self.currentHealth

    @CurrentHealth.setter
    def CurrentHealth(self, health):
        if health < 0.0:
            health = 0.0
        elif health > self.Health:
            health = self.Health
        self.currentHealth = health

    @property
    def CurrentMana(self): return self.currentMane

    @CurrentMana.setter
    def CurrentMana(self, mana):
        if mana < 0.0:
            mana = 0.0
        elif mana > self.Mana:
            mana = self.Mana
        self.currentMane = mana

    def update(self,dt):
        if self.isDead: return
        self.regenTimer += dt
        # 处理生命和魔法回复
        if self.regenTimer >= 1:
            self.regenTimer -= 1
            self.CurrentHealth += self.HealthRegen
            self.CurrentMana += self.ManaRegen

    # 执行攻击
    def performAttack(self, target):
        if target is None or target.isDead or self.isDead: return
        # 判断攻击cd
        if time.time() - self.attackStartTime < 1 / self.attackSpeed: return
        self.attackStartTime = time.time()
        self.allClients.reqAttack(target.id)
        Combat.damage(Param(self, target, self.Attack, DamageType.Physical))

    # 杀死
    def kill(self, attacker):
        DEBUG_MSG(f"{self.name} 被杀死")
        self.allClients.reqDead(attacker.id)
        if attacker.onKillCallback: attacker.onKillCallback(self)
        self.clearTarget()
        self.isDead = True
        if self.onDeadCallback: self.onDeadCallback()

    # 强制杀死 
    def forceKill(self):
        DEBUG_MSG(f"{self.name} 被杀死")
        self.clearTarget()
        self.isDead = True

    def revive(self):
        DEBUG_MSG(f"{self.name} 被复活 lv.{self.level}")
        self.isDead = False                                                     # 是否死亡
        self.resetAttr()                                                        # 重置属性
        self.CurrentHealth = self.Health                                        # 当前生命值
        self.CurrentMana = self.Mana                                            # 当前魔法值
        self.attackStartTime = time.time()                                      # 攻击开始时间
        self.regenTimer = 0                                                     # 回复计时器
        if self.onReviveCallback != None: self.onReviveCallback()               # 复活回调

    def clearTarget(self):
        # 通知仇恨列表中的所有目标
        for id in self.hateTargetIDs:
            hateTarget = KBEngine.entities.get(id)
            if hateTarget is None: continue
            hateTarget.removeTarget(self.id)
        self.hateTargetIDs = []
        self.hateTargetID = -1

    def getDirectTargetID(self):
        if len(self.hateTargetIDs) <= 0: return -1
        minDis = 999.0
        minID = -1
        for id in self.hateTargetIDs:
            hateTarget = KBEngine.entities.get(id)
            if hateTarget is None: continue
            dis = Vector.distance2d(self.uPosition, hateTarget.uPosition)
            if dis < minDis:
                minID = id
                minDis = dis
        return minID

    def addTarget(self, targetID):
        entity = KBEngine.entities.get(targetID)
        # 目标不存在 || 自己已经死亡 || 目标已经死亡 || 目标已经销毁
        if entity == None or self.isDead or entity.isDestroyed or entity.isDead: return
        # 如果目标标签与自己的标签相同 || 目标标签与自己的敌人标签相同
        if entity.thisTag == self.thisTag or entity.thisTag & self.enemyTag == 0: return
        # 如果目标不在仇恨列表中，则添加到列表中
        if targetID not in self.hateTargetIDs: self.hateTargetIDs.append(targetID)
        # 如果没有仇恨目标，则设置当前目标为最近目标
        if self.hateTargetID == -1: self.hateTargetID = self.getDirectTargetID()
        
    def removeTarget(self, targetID):
        if self.isDead: return
        if targetID in self.hateTargetIDs: self.hateTargetIDs.remove(targetID)
        if targetID == self.hateTargetID: self.hateTargetID = self.getDirectTargetID()