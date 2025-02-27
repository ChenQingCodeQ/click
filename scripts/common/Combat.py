import random
import KBEngine
import math
from KBEDebug import *

# 单位成长
class UnitGrow:
    def __init__(self, level,healthUp, healthCoe, attackUp, attackCoe, armorUp):
        self.healthUp = healthUp or 0
        self.healthCoe = healthCoe or 0
        self.attackUp = attackUp or 0
        self.attackCoe = attackCoe or 0
        self.armorUp = armorUp or 0
        self.level = level
    @property
    def health(self):
        return (self.level - 1) * self.healthUp + math.pow((self.level - 1) * 2, self.healthCoe)
    @property
    def attack(self):
        return (self.level - 1) * self.attackUp + math.pow((self.level - 1) * 2, self.attackCoe)
    @property
    def armor(self):
        return (self.level - 1) * self.armorUp

class DamageType:
    Physical = 1        # "Physical"
    Flame = 2           # "Flame"
    Ice = 3             # "Ice"
    Poison = 4          # "Poison"


class Param:
    def __init__(self,attacker, victim, damage, damage_type):
        self.attacker = attacker        # 攻击者对象
        self.victim = victim            # 防御者对象
        self.damage = damage            # 初始伤害值
        self.damageType = damage_type   # 伤害类型（例如：物理、火焰等）
        self.isSkill = False            # 是否是技能伤害
        self.isCrit = False             # 是否暴击
        self.isMiss = False             # 是否闪避

# 经验计算公式
expCoefficient = 2.1 # 经验系数
expAmend = 100       # 经验修正值

# 通过经验值计算等级
def computeLevel(exp):
    return int(math.pow(exp / expAmend, 1 / expCoefficient) + 1)

# 通过等级计算经验值
def computeExp(level):
    return math.pow(level - 1, expCoefficient) * expAmend


# 执行伤害
def damage(param:Param):
    # type(victim) = Unit 
    victim = param.victim
    attacker = param.attacker
    damage_type = param.damageType
    # 计算命中率
    hit_rate = attacker.Hit / (attacker.Hit + victim.Dodge)
    param.isMiss = random.random() > hit_rate  # 如果随机数大于命中率，则闪避
    if param.isMiss:
        if attacker.onMissCallback: attacker.onMissCallback(param)
        if victim.onMissCallback: victim.onMissCallback(param)
        victim.allClients.reqDamage(victim.id,-1,0.0, damage_type)
        return
    # 应用攻击者的伤害加成
    param.damage = param.damage * (1 + attacker.DamageBonus)
    # 计算经过护甲减免后的伤害值
    armor_reduction = max(0, min(1, victim.Armor * 0.05))  # 假设每点护甲减少5%伤害
    param.damage = param.damage * (1 - armor_reduction)
    # 根据伤害类型应用额外的伤害加成
    if damage_type == DamageType.Physical:
        # 判断是否发生暴击
        param.isCrit = random.random() < attacker.CritRate
        if param.isCrit:
            param.damage *= attacker.CritDamage
            if attacker.onCritCallback: attacker.onCritCallback(param)
            if victim.onCritCallback: victim.onCritCallback(param)
        param.damage *= 1 + attacker.PhysicalDamage
    elif damage_type == DamageType.Flame:
        param.damage *= 1 + attacker.FlameDamage
    elif damage_type == DamageType.Ice:
        param.damage *= 1 + attacker.IceDamage
    elif damage_type == DamageType.Poison:
        param.damage *= 1 + attacker.PoisonDamage
    # 应用防御者的伤害减免
    param.damage *= 1 - victim.DamageReduction
    # 触发伤害事件
    if attacker.onDamageCallback: attacker.onDamageCallback(param)
    if victim.onDamageCallback: victim.onDamageCallback(param)
    # 如果没有闪避，则从防御者的生命值中减去最终伤害
    victim.CurrentHealth = victim.CurrentHealth - param.damage
    # 触发伤害后事件
    if attacker.onDamageAfterCallback: attacker.onDamageAfterCallback(param)
    if victim.onDamageAfterCallback: victim.onDamageAfterCallback(param)
    # 通知客户端
    victim.allClients.reqDamage(victim.id,-1,param.damage, damage_type)
    # 当前生命值小于等于0，则表示死亡
    if victim.CurrentHealth <= 0:
        victim.kill(attacker)
    
    # 伤害字幕
    # DEBUG_MSG(f"Damage: {param.damage} to {victim.name}, health:{victim.CurrentHealth}")