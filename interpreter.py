
from vaughanparse import parser

class Interp:

    stack = []
    namespace = dict()

    def exec_string(self, input):
        ast = parser.parse(input)

    def exec(self, ast):
        match ast:
            # literal cases: ints, floats, strings
            case ('string_literal', str):
                return str
            
            case ('int_literal', number):
                return number

            case ('float_literal', number):
                return number
            
            # list cases: list, head, tail
            case ('list', cons):
                return self.exec(cons)

            case ('head', expression, list):
                exp_value = self.exec(expression)
                list_value = self.exec(list)
                return [exp_value] + list_value

            case ('tail', expression):
                return [self.exec(expression)]

            # name lookup case
            case ('name', name):
                if name not in self.namespace:
                    return f"error: {name} not in namespace" 

                return self.exec(self.namespace[name])
            
            # define case, set values in namespace
            case ('define', name, expression):
                self.namespace[name] = expression
                return name

            # function application
            case ('application', name, list):
                return f"applied {name}"


if __name__ == "__main__":

    interp = Interp()

    while True:
        try:
            s = input('vaughan > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)
        
        exec_result = interp.exec(result)
        print(exec_result)
