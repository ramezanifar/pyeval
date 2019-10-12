import time
import json



class pyeval:
    '''
    This class evaluates a mathematical expression fast. The expression is a string in a certain format.
    For example the expression ((1+2)-(6x7)>-20) | (3==4) should be translated to 'OR(GT(SUB(ADD(1,2),MUL(6,7)),-20),EQ(3,4))'      
    '''

    def __init__(self):
        self.op=[]
        self.intermediate_results = []
        self.ind = 0

    def find_value(self,parsed):
        ''' 
        This method is used to evaluate a parsed expression. The expression is represented as a nested list
        along with the order of operations
        '''
        if isinstance(parsed, list):
            this_op=self.op[self.ind]
            self.ind=self.ind+1

            if this_op=='+':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc=0
                for e in parsed:
                    acc=acc+self.find_value(e)
                self.intermediate_results[ind_temp - 1] = acc
                return acc

            elif this_op=='*':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc = 1
                for e in parsed:
                    acc=acc*self.find_value(e)
                self.intermediate_results[ind_temp - 1] = acc
                return acc

            elif this_op == '-':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                first = True
                for e in parsed:
                    if first==True: # to avoid negating the first number
                        acc=self.find_value(e)
                        first = False
                    else:
                        acc = acc-self.find_value(e)
                self.intermediate_results[ind_temp - 1] = acc
                return acc

            elif this_op == '/':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                first = True
                for e in parsed:
                    if first==True:
                        acc= self.find_value(e)*1.0 # to make it float
                        first=False
                    else:
                        acc = acc / self.find_value(e)
                self.intermediate_results[ind_temp-1] = acc
                return acc

            elif this_op in ['^','**']:
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                first = True
                acc = 1
                for e in parsed:
                    if first==True:
                        acc= self.find_value(e)
                        first=False
                    else:
                         acc = acc ** self.find_value(e)
                self.intermediate_results[ind_temp-1] = acc
                return acc

            elif this_op =='>':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a > b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == '>=':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a >= b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == '<':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a < b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == '<=':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a <= b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == '==':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a == b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == '!=':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a != b
                self.intermediate_results[ind_temp - 1] = res
                return res


            elif this_op == '&':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc=True
                for e in parsed:
                    acc=acc & self.find_value(e)
                self.intermediate_results[ind_temp-1] = acc
                return acc

            elif this_op == '|':
                ind_temp=self.ind # to store intermediate results in a list corresponding to the operator
                acc=False
                for e in parsed:
                    acc=acc | self.find_value(e)
                self.intermediate_results[ind_temp-1]=acc
                return acc

            elif this_op == '!':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res=not(self.find_value(e))
                self.intermediate_results[ind_temp-1] = res
                return res
        else:
            return parsed

    def parse(self,expr):
        ''' This method parses an expression in the form of nested lists along with a list of ordered operations '''
        # Extract the list of operators'
        i = 0
        op = []
        while i < len(expr):
            if expr[i:i + 3] == 'ADD':
                op.append('+')
                i = i + 4
            elif expr[i:i + 3] == 'SUB':
                op.append('-')
                i = i + 4
            elif expr[i:i + 3] == 'MUL':
                op.append('*')
                i = i + 4
            elif expr[i:i + 3] == 'DIV':
                op.append('/')
                i = i + 4
            elif expr[i:i + 2] == 'GT':
                op.append('>')
                i = i + 3
            elif expr[i:i + 2] == 'GE':
                op.append('>=')
                i = i + 3
            elif expr[i:i + 2] == 'LT':
                op.append('<')
                i = i + 3
            elif expr[i:i + 2] == 'LE':
                op.append('<=')
                i = i + 3
            elif expr[i:i + 2] == 'EQ':
                op.append('==')
                i = i + 3
            elif expr[i:i + 2] == 'NE':
                op.append('!=')
                i = i + 3
            elif expr[i:i + 3] == 'AND':
                op.append('&')
                i = i + 4
            elif expr[i:i + 2] == 'OR':
                op.append('|')
                i = i + 3
            elif expr[i:i + 3] == 'NOT':
                op.append('!')
                i = i + 4
            else:
                i = i + 1
        # Remove the operators from expression
        Operators = ['ADD', 'MUL', 'SUB', 'DIV', 'POW', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'AND', 'OR', 'NOT']
        for this_op in Operators:
            expr = expr.replace(this_op, '')
        # change ( to [
        expr = expr.replace('(', '[')
        expr = expr.replace(')', ']')
        # Extract the list of numbers'
        formatted_expr = json.loads(expr)
        return formatted_expr,op

    def evaluate(self,expr):
        tic = time.time() # To measure the time
        formatted_expr, op=self.parse(expr)
        self.op=op
        self.intermediate_results = [[]] * len(op)
        self.ind=0
        val=self.find_value(formatted_expr) # find the value of the expression
        toc = time.time() - tic
        return val,self.intermediate_results,toc



if __name__ == '__main__':
    myeval=pyeval()
    exprs='OR(GT(SUB(ADD(1,2),MUL(6,7)),-20),EQ(3,4))'  # ((1+2)-(6x7)>-20) | (3==4)
    val,int_res,toc=myeval.evaluate(exprs)
    print '{} = {}'.format(exprs,val)
    print 'Intermediate results:', int_res
    print 'Time it took (us):', toc*1e6
    
