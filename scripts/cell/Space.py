import KBEngine
from KBEDebug import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import d_space

class Space(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG(f"初始化 cell [{type(self).__name__}] id:[{self.id}]")
        # 创建网格地图（0 表示障碍，1 表示可通行）
        self.spaceInfo = d_space.datas[self.mapID]
        self.grid = Grid(matrix=self.spaceInfo["matrix"])
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        KBEngine.globalData[f"Space{self.mapID}"] = self

    def findPath(self, sx, sy, ex, ey):
        # 定义起点和终点
        sx = round(sx)
        sy = round(sy)
        ex = round(ex)
        ey = round(ey)
        start = self.grid.node(sx, sy)
        end = self.grid.node(ex, ey)

        path, runs = self.finder.find_path(start, end, self.grid)
        # 输出路径 为 json
        # DEBUG_MSG(f"sx: {sx} sy: {sy} ex: {ex} ey: {ey}")
        # for i in range(len(path)):
        #     DEBUG_MSG(f"第 {i} 步: {path[i]}")
        return path

    def findNearestWalkablePoint(self, x, y):
        """
        在网格中找到离 (x, y) 最近的可行走点。
        :param grid: Grid 对象
        :param x: 目标点的 x 坐标
        :param y: 目标点的 y 坐标
        :return: 最近的可行走点的 (x, y) 坐标
        """
        x = round(x)
        y = round(y)
        # x或y小于时设为0
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        # x或y大于地图大小时设为地图大小
        if x >= self.grid.width:
            x = self.grid.width - 1
        if y >= self.grid.height:
            y = self.grid.height - 1

        grid = self.grid
        # 如果目标点本身可行走，直接返回
        if grid.walkable(x, y):
            return (x, y)

        # 获取网格的宽度和高度
        width = grid.width
        height = grid.height

        # 使用广度优先搜索（BFS）向外扩展搜索
        from collections import deque
        queue = deque()
        queue.append((x, y))  # 将初始点加入队列
        visited = set()  # 记录已访问的点
        visited.add((x, y))

        # 定义 4 个方向的移动（上下左右）
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current_x, current_y = queue.popleft()

            # 遍历四个方向
            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy

                # 检查新点是否在网格范围内
                if 0 <= new_x < width and 0 <= new_y < height:
                    # 如果新点未被访问过
                    if (new_x, new_y) not in visited:
                        # 如果新点可行走，返回该点
                        if grid.walkable(new_x, new_y):
                            return (new_x, new_y)
                        # 否则将新点加入队列
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))

        # 如果没有找到可行走点，返回 None
        return None
        
    def onDestroy(self):
    	"""
    	KBEngine method.
    	"""
    	del KBEngine.globalData[f"Space{self.mapID}"]
    	self.destroySpace()
		