from dataclasses import dataclass
from .base import Serializable


@dataclass
class Trade(Serializable):
    '''
    >>> Trade('spot', 100, 100)
    Trade(typology='spot', number=100, nominal=100)

    '''
    typology: str
    number: int
    nominal: int


    def __reduce__(self):
        '''
        >>> t = Trade('spot', 100, 100)
        >>> t.__reduce__()
        (<class 'mx_sim.common.trade.Trade'>, ('spot', 100, 100))

        '''
        return self.__class__, (self.typology, self.number, self.nominal)


    def __eq__(self, other):
        '''
        >>> from mx_sim.common.base import Deserializer
        >>> t = Trade('spot', 100, 100)
        >>> data = t.serialize()
        >>> t2 = Deserializer.deserialize(data)
        >>> t == t2
        True

        '''
        return self.__reduce__() == other.__reduce__()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)