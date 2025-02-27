import Math, math

class Vector:
    def floatToVector3(x, y, z):
        return Math.Vector3(x, y, z)

    def nodeToVector3(node):
        """
        将一个Vector3f转换为Vector3
        """
        if node is None:
            return Math.Vector3(0, 0, 0)
        else:
            return Math.Vector3(node.x, node.y, 0)
    
    def tupleToVector3(vector_tuple):
        return Math.Vector3(vector_tuple[0], vector_tuple[2], vector_tuple[1])


    def add(vector_a, vector_b):
        """
        向量加法
        """
        return Math.Vector3(vector_a.x + vector_b.x, vector_a.y + vector_b.y, vector_a.z + vector_b.z)

    def sub(vector_a, vector_b):
        """
        向量减法
        """
        return Math.Vector3(vector_a.x - vector_b.x, vector_a.y - vector_b.y, vector_a.z - vector_b.z)

    def mul(vector_a, scalar):
        """
        向量乘以标量
        """
        return Math.Vector3(vector_a.x * scalar, vector_a.y * scalar, vector_a.z * scalar)

    def div(vector_a, scalar):
        """
        向量除以标量
        """
        return Math.Vector3(vector_a.x / scalar, vector_a.y / scalar, vector_a.z / scalar)

    def dot(vector_a, vector_b):
        """
        向量点积
        """
        return vector_a.x * vector_b.x + vector_a.y * vector_b.y + vector_a.z * vector_b.z

    def cross(vector_a, vector_b):
        """
        向量叉积
        """
        return Math.Vector3(
            vector_a.y * vector_b.z - vector_a.z * vector_b.y,
            vector_a.z * vector_b.x - vector_a.x * vector_b.z,
            vector_a.x * vector_b.y - vector_a.y * vector_b.x
        )

    def length(vector_a):
        """
        向量长度
        """
        return math.sqrt(vector_a.x * vector_a.x + vector_a.y * vector_a.y + vector_a.z * vector_a.z)

    def normalize(vector_a):
        """
        向量归一化
        """
        vector_length = Vector.length(vector_a)
        if vector_length != 0:
            return Math.Vector3(vector_a.x / vector_length, vector_a.y / vector_length, vector_a.z / vector_length)
        return Math.Vector3()
    
    def distance(vector_a, vector_b):
        """
        向量距离
        """
        return math.sqrt((vector_a.x - vector_b.x) ** 2 + (vector_a.y - vector_b.y) ** 2 + (vector_a.z - vector_b.z) ** 2)

    def lerp(vector_a, vector_b, t):
        """
        线性插值
        """
        return Math.Vector3(
            vector_a.x + (vector_b.x - vector_a.x) * t,
            vector_a.y + (vector_b.y - vector_a.y) * t,
            vector_a.z + (vector_b.z - vector_a.z) * t
        )

    def slerp(vector_a, vector_b, t):
        """
        球面线性插值
        """
        dot = Vector.dot(vector_a, vector_b)
        dot = max(-1, min(1, dot))  # 确保dot在[-1, 1]范围内
        theta = math.acos(dot) * t
        relative_vec = Vector.sub(vector_b, Vector.mul(vector_a, dot))
        relative_vec = Vector.normalize(relative_vec)
        return Vector.add(Vector.mul(vector_a, math.cos(theta)), Vector.mul(relative_vec, math.sin(theta)))

    def angle(vector_a, vector_b):
        """
        向量夹角
        """
        return math.acos(Vector.dot(vector_a, vector_b) / (Vector.length(vector_a) * Vector.length(vector_b)))



    def add2d(vector_a, vector_b):
        """
        二维向量相加，忽略z轴
        """
        return Math.Vector3(vector_a.x + vector_b.x, vector_a.y + vector_b.y, 0)

    def sub2d(vector_a, vector_b):
        """
        二维向量相减，忽略z轴
        """
        return Math.Vector3(vector_a.x - vector_b.x, vector_a.y - vector_b.y, 0)

    def mulf2d(vector_a, scalar):
        """
        二维向量乘以标量，忽略z轴
        """
        return Math.Vector3(vector_a.x * scalar, vector_a.y * scalar, 0)

    def divf2d(vector_a, scalar):
        """
        二维向量除以标量，忽略z轴
        """
        return Math.Vector3(vector_a.x / scalar, vector_a.y / scalar, 0)

    def dot2d(vector_a, vector_b):
        """
        二维向量点积，忽略z轴
        """
        return vector_a.x * vector_b.x + vector_a.y * vector_b.y

    def cross2d(vector_a, vector_b):
        """
        二维向量叉积，忽略z轴
        """
        return vector_a.x * vector_b.y - vector_a.y * vector_b.x

    def distance2d(vector_a, vector_b):
        """
        二维向量距离，忽略z轴
        """
        return math.sqrt((vector_a.x - vector_b.x) ** 2 + (vector_a.y - vector_b.y) ** 2)

    def length2d(vector_a):
        """
        二维向量长度，忽略z轴
        """
        return math.sqrt(vector_a.x * vector_a.x + vector_a.y * vector_a.y)

    def normalize2d(vector_a):
        """
        二维向量归一化，忽略z轴
        """
        vector_length = Vector.length2d(vector_a)
        if vector_length != 0:
            return Math.Vector3(vector_a.x / vector_length, vector_a.y / vector_length, 0)
        return Math.Vector3()

    def lerp2d(vector_a, vector_b, t):
        """
        二维向量线性插值，忽略z轴
        """
        return Math.Vector3(
            vector_a.x + (vector_b.x - vector_a.x) * t,
            vector_a.y + (vector_b.y - vector_a.y) * t,
            0
        )
    
    def slerp2d(vector_a, vector_b, t):
        """
        二维向量球面线性插值，忽略z轴
        """
        dot = Vector.dot(vector_a, vector_b)
        dot = max(-1, min(1, dot))
        theta = math.acos(dot) * t
        relative_vec = Vector.sub(vector_b, Vector.mul(vector_a, dot))
        relative_vec = Vector.normalize2d(relative_vec)
        return Vector.add(Vector.mul(vector_a, math.cos(theta)), Vector.mul(relative_vec, math.sin(theta)))

    def angle2d(vector_a, vector_b):
        """
        二维向量夹角，忽略z轴
        """
        return math.acos(Vector.dot(vector_a, vector_b) / (Vector.length2d(vector_a) * Vector.length2d(vector_b)))

    def rotate2d(vector_a, angle):
        """
        二维向量旋转，忽略z轴
        """
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Math.Vector3(
            vector_a.x * cos - vector_a.y * sin,
            vector_a.x * sin + vector_a.y * cos,
            0
        )