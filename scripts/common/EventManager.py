import uuid

class EventManager:
    def __init__(self):
        self.events = {}  # 存储事件ID与事件信息的映射
        self.handlers = {}  # 存储用户ID与事件处理函数的映射

    def sendEvent(self, userID, eventType, param):
        """
        发送事件，返回事件ID
        :param userID: 用户ID
        :param eventType: 事件类型
        :param param: 事件参数
        :return: 事件ID
        """
        eventID = str(uuid.uuid4())  # 生成唯一的事件ID
        self.events[eventID] = {
            'userID': userID,
            'eventType': eventType,
            'param': param
        }

        # 如果用户注册了该类型的事件处理函数，则调用
        if userID in self.handlers and eventType in self.handlers[userID]:
            self.handlers[userID][eventType](param)

        return eventID

    def registerEvent(self, userID, eventType, func):
        """
        注册事件处理函数
        :param userID: 用户ID
        :param eventType: 事件类型
        :param func: 事件处理函数
        """
        if userID not in self.handlers:
            self.handlers[userID] = {}
        self.handlers[userID][eventType] = func

    def unEvent(self, eventID):
        """
        取消事件
        :param eventID: 事件ID
        """
        if eventID in self.events:
            del self.events[eventID]