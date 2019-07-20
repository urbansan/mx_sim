import pickle
from abc import abstractmethod, ABC

class Deserializer:
    @staticmethod
    def deserialize(data_bytes):
        return pickle.loads(data_bytes)

deserialize = Deserializer.deserialize

class Serializable(ABC):
    def serialize(self):
        return pickle.dumps(self)

    @abstractmethod
    def __reduce__(self):
        pass