
from vaughanparse import parser

class Closure:
    namespace = dict()
    expression = None

    def __init__(self, expression, namespace):
        self.namespace = namespace
        self.expression = expression

class Interp:

    namespace = dict()
    closures = []

    def exec_string(self, input):
        ast = parser.parse(input)

    # get lambda parameters
    def get_params(self, list):
        pass

    # produce the closure for the expression
    def closure(self, params, expression, namespace):
        closure_key = len(self.closures)
        cls = Closure(expression, namespace)
        self.closures.append(cls)
        return ('closure', closure_key)

    # execute statment
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
            
            # define case, set values in namespace or produce closure
            case ('define', name, expression):
                self.namespace[name] = self.exec(expression)
                return name
            
            # lambda (build closure)
            case ('lambda', params, expression):
                cls = self.closure(params, expression, self.namespace)
                return f"make closure"

            # function application
            case ('application', name, list):
                return f"apply {name}"

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
