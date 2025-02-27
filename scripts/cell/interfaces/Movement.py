import random, GlobalConst, math
from Mathf import Vector
import KBEngine
from KBEDebug import *


class Movement():
    def __init__(self):
        
        self.spawnPosition = Vector.tupleToVector3(self.spawnPos)   # 出生位置
        self.patrolRadius = 5                                       # 巡逻半径
        self.currentPath = []                                       # 当前路径
        self.currentPathIndex = 0                                   # 当前路径索引

    def onDestroy(self):
        self.endNavigation()
        self.followTarget = None
        self.currentPath = []
        self.currentPathIndex = 0

    def moveRandomPosition(self):
        newPosition = self.getRandomPositionInRadius()
        self.moveToPosition(newPosition)

    def moveToPosition(self, position):
        self._updatePath(self.uPosition.x, self.uPosition.y, position.x, position.y)

    def endNavigation(self):
        self.currentPath = []
        self.currentPathIndex = 0

    def getRandomPositionInRadius(self):
        # 在巡逻半径内随机选择一个点
        angle = random.uniform(0, 2 * math.pi)
        x = self.spawnPosition.x + math.cos(angle) * self.patrolRadius
        y = self.spawnPosition.y + math.sin(angle) * self.patrolRadius
        spawner = KBEngine.globalData[f"Space{self.mapID}"]
        x, y = KBEngine.entities.get(spawner.id).findNearestWalkablePoint(x, y)
        return Vector.floatToVector3(x, y, 0)

    def update(self,dt):
        self._updatePosition(dt)

    def _updatePosition(self,dt):
        if self.currentPathIndex >= len(self.currentPath):
            return
        # DEBUG_MSG(f"索引:[{self.currentPathIndex}] 速度:[{self.MovementSpeed}]  路径 :[{self._pathToString()}]")
        # 获取下一个路径点
        nextPosition = Vector.nodeToVector3(self.currentPath[self.currentPathIndex])
        direction = Vector.sub(nextPosition, self.uPosition)
        distance = Vector.length2d(direction)
        newPosition = None
        if distance <= self.MovementSpeed * dt:
            # 到达下一个路径点
            newPosition = nextPosition
            self.currentPathIndex += 1
        else:
            # 移动到下一个路径点
            moveDir = Vector.mul(Vector.normalize(direction), self.MovementSpeed * dt)
            newPosition = Vector.add(self.uPosition, moveDir)
        newPosition.z = 0.0
        self.uPosition = newPosition

    def _updatePath(self, sx, sy, ex, ey):
        """
        寻找从起点到终点的路径
        """
        spawner = KBEngine.globalData[f"Space{self.mapID}"]
        self.currentPath = KBEngine.entities.get(spawner.id).findPath(sx, sy, ex, ey)
        # 忽视第一个点
        self.currentPathIndex = 1
        # DEBUG_MSG(f"路径更新 :[{self._pathToString()}]")

    def _pathToString(self):
        text = ""
        for node in self.currentPath:
            text += f"{node.x},{node.y};"
        return text