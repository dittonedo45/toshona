import typing

class GetNumber(typing.Dict):
    def __init__(self, *args, **kwargs):
        dict.__init__ (self, *args, **kwargs)
        self.last_element=4

    def set_last_element(self, last=None):
        self.last_element=last

    def _get(self, item):
        res=dict.get (self, item, None)

        if not res:
            return self.get(self.last_element)
        else:
            return res

class Shona(object):
    """
    The Shona class for translating numbers to shona strings::
    >>> v = Shona (9000)
    <[900]: mazana mapfumpamwe>
    >>> str(Shona (9500))
    <[9500]: zviuru zvipfumpamwe, nemazana mashanu>

    """
    def __init__(self, numb, end=""):
        self.func_handler=GetNumber(zip(range (1,5),
            (self._humwe, self._hukumi, self._huzana, self._huru)))
        self.res=None
        self.numb=numb
        self.end=end
    
    def __str__(self):
        if not self.res:
            self.res="".join (self.shona (self.numb))
        return self.res

    def __repr__(self):
        if not self.res:
            self.res="".join (self.shona (self.numb))
        return f"<[{self.numb}]: {self.res}>"

    def shona(self, number=None):
        if number is None:
            number=self.numb
        if not number:
            return iter(lambda *x: None, None)
        str_n=str (number)
        length=len(str_n)

        func=self.func_handler._get (length)
        if not func:
            return
        yield from func(str_n)
    def the_end (self):
        if len(self.end):
            yield self.end
    def not_singular (self, num):
        return "1"!=num

    def _humwe (self, number, m_s=0, has_end=True):
        units=["zanda", "imwe", "piri", "tatu", "ina", "shanu", "tanhatu", "nomwe", "sere", "pfumpamwe"]
        m_humwe=["zanda", "", "maviri", "matatu", "mana", "mashanu", "matanhatu", "manomwe", "masere", "mapfumpamwe"]
        z_humwe=["zanda", "", "zviviri", "zvitatu", "zvina", "zvishanu", "zvitanhatu", "zvinomwe", "zvisere", "zvipfumpamwe"]
        if m_s==0:
            yield units[int(number)]
        elif m_s==1:
            yield m_humwe[int(number)]
        else:
            yield z_humwe[int(number)]

        if has_end:
            yield from self.the_end()

    def _hukumi(self, number):
        yield self.plural (1, number[0])
        if self.not_singular(number[0]):
            yield " "
            yield from self._humwe(number[0], 1, False)

        if int(number[1:]):
            yield ", ne"
            yield from self.shona(int(number[1:]))
        else:
            yield from self.the_end()

    def _huzana(self, number):
        yield self.plural (2, number[0])
        if self.not_singular(number[0]):
            yield " "
            yield from self._humwe(number[0], 1, False)

        if int(number[1:]):
            yield ", ne"
            yield from self.shona(int(number[1:]))
        else:
            yield from self.the_end()

    def _huru(self, number):
        count=len(number[:-3])
        if count>1:
            yield self.plural (3, "3")
            yield " "
            yield "("
            yield from self.shona(int(number[:-3]))
            yield ")"

            if int(number[count:]):
                yield ", ne"
                yield from self.shona(int(number[count:]))
            else:
                yield from self.the_end()
        else:
            yield self.plural (3, number[:1])
            if self.not_singular(number[0]):
                yield " "
                yield from self._humwe(number[:1], 3, False)

            if int(number[1:]):
                yield ", ne"
                yield from self.shona(int(number[1:]))
            else:
                yield from self.the_end()

    def plural(self, degree, num):
        if degree==1:
            if int(num)==1:
                return "gumi"
            else:
                return "makumi"
        elif degree==2:
            if int(num)==1:
                return "zana"
            else:
                return "mazana"
        elif degree==3:
            if int(num)==1:
                return "churu"
            else:
                return "zviuru"
