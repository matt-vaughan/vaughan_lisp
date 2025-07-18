
import copy
from vaughanparse import parser

DEBUG = True

class Closure:

    def __init__(self, params, expression, namespace):
        self.namespace = namespace
        for param in params:
            del self.namespace[param]

        self.expression = expression
        self.params = params
        if DEBUG:
            print ("closure contains: ")
            for key, value in namespace.items():
                print(f"{key} -> {value}")
    
    def bind_arguments(self, args):
        if len(args) != len(self.params):
            raise ValueError(f"Expected {len(self.params)} arguments and got {len(args)}")
        
        for i in range(0, len(args)):
            if DEBUG:
                print(f"binding {self.params[i]} to {args[i]}")
            self.namespace[self.params[i]] = args[i] 
    
    def apply(self, args):

        self.bind_arguments(args)
        interp = Interp(self.namespace)
        return interp.exec(self.expression)
    

class Interp:

    def __init__(self, namespace):
        self.namespace = namespace
        self.closures = []

    def exec_string(self, input):
        ast = parser.parse(input)

    # produce the closure for the expression
    def closure(self, params, expression, namespace):
        closure_index = len(self.closures)
        cls = Closure(params, expression, namespace)
        self.closures.append(cls)
        return ('closure', closure_index)

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
                if DEBUG:
                    print(f"looking up {name}")
                if name not in self.namespace:
                    return f"error: {name} not in namespace" 

                return self.namespace[name] # THOUGHT: perhaps conditional exec?? 
                        
            # define case, set values in namespace or produce closure
            case ('define', name, expression):
                self.namespace[name] = self.exec(expression)
                return name
            
            # lambda (build closure)
            case ('lambda', params, expression):
                new_namespace = copy.deepcopy(self.namespace)
                return self.closure(params, expression, new_namespace)

            # function application
            case ('application', name, list):
                if name not in self.namespace:
                    return f"error: {name} is not in namespace"
                
                f = self.namespace[name]
                match f:
                    case ('closure', closure_index):
                        # evaluate the arguments
                        args = []
                        for arg in list:
                            args.append(self.exec(arg))
                        
                        # apply
                        cls = self.closures[closure_index]
                        return cls.apply(args)
                    case _:
                        return f"error: {name} does not refer to a closure"
                    
                return f"apply {name}"
            
            case _:
                return ast

if __name__ == "__main__":

    interp = Interp( dict() )

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
