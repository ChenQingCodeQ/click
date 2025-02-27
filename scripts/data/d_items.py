"""
装备属性
attack = 10.0                                   # 攻击力
health = 400.0                                  # 生命值
armor = 5.0                                     # 护甲值
mana = 100.0                                    # 魔法值
attackSpeed = 0.7                               # 攻击速度
movementSpeed = 2.0                             # 移动速度
attackRange = 1.0                               # 攻击范围
healthRegen = 2.0                               # 生命回复
manaRegen = 20.0                                # 魔法回复
hit = 100.0                                     # 命中
dodge = 50.0                                    # 闪避
critRate = 0.05                                 # 暴击率
critDamage = 1.5                                # 暴击伤害 基础为150%
physicalDamage = 0                              # 物理伤害加成 基础为0%
flamedamage = 0.5                               # 火焰伤害加成 基础为50%
iceDamage = 0.5                                 # 冰冻伤害加成 基础为50%
poisonDamage = 0.5                              # 中毒伤害加成 基础为50%
damageBonus = 0.0                               # 伤害加成
damageReduction = 0.0                           # 伤害减免
cooldownBoost = 0.0                             # 冷却减少
attackBoost = 0.0                               # 攻击提高
armorBoost = 0.0                                # 护甲提高
healthBoost = 0.0                               # 生命提高
manaBoost = 0.0                                 # 魔法提高
attackSpeedBoost = 0.0                          # 攻击速度提高
movementSpeedBoost = 0.0                            # 移动速度提高
"""

datas={
    1: {
        'id': 1,                            # 物品id
        'type' : 1,                         # 物品类型 1:装备 2:消耗品 3:材料
        'stack': 1,                         # 物品堆叠数量
        'script' : 'itemUse',               # 物品脚本
        'attrKey1': 'attack',               # 攻击力
        'attrValue1': [10.0,20.0],          # 生命值 [min ,max]
        'attrKey2': 'health',               # 生命值
        'attrValue2': [100.0,200.0],        # 生命值 [min ,max]
        'attrKey3': 'armor',                # 护甲值
        'attrValue3': [5.0,10.0],           # 护甲值 [min ,max]
    },
    2: { 'id': 2,'type': 2, 'stack': 99, 'sctipt': 'itemUse'},
    3: { 'id': 3,'type': 3, 'stack': 99 },
}