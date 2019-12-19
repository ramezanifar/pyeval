import time
import json
import math


class pyfeval:
    '''
    pyeval stands for python fast evaluator
    This is an engine to evaluate a mathematical expression fast. The expression is a string in a certain format.
    For example the expression ((1+2)-(6x7)>-20) | (3==4) should be translated to 'OR(GT(SUB(ADD(1,2),MUL(6,7)),-20),EQ(3,4))'
    '''

    def __init__(self):
        self.op=[]
        self.intermediate_results = []
        self.ind = 0
        self.has_error = False # This flag shos if there is any error in evaluation of the expression
        self.err_msg = '' # It will shows the details of the error

    def find_value(self,parsed):
        '''
        This method is used to evaluate a parsed expression. The expression is represented as a nested list
        along with the order of operations
        '''
        if self.has_error == True:
            return 0

        if isinstance(parsed, list):
            this_op=self.op[self.ind]
            self.ind=self.ind+1

            if this_op=='ADD':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc=0
                for e in parsed:
                    acc=acc+self.find_value(e)
                self.intermediate_results[ind_temp - 1] = acc
                return acc

            elif this_op=='MUL':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc = 1
                for e in parsed:
                    acc=acc*self.find_value(e)
                self.intermediate_results[ind_temp - 1] = acc
                return acc

            elif this_op == 'SUB':
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

            elif this_op == 'DIV':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                first = True
                for e in parsed:
                    if first==True:
                        acc= self.find_value(e)*1.0 # to make it float
                        first=False
                    else:
                        den = self.find_value(e) # Denominator
                        if den == 0 :
                            self.has_error = True
                            self.err_msg = "Division by zero"
                            break # Terminate the for loop
                        else:
                            acc = acc / den
                self.intermediate_results[ind_temp-1] = acc
                return acc

            elif this_op in 'POW':
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

            elif this_op =='GT':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a > b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'GE':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a >= b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'LT':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a < b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'LE':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a <= b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'EQ':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a == b
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'NE':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                p1 = parsed[0]
                a = self.find_value(p1)
                p2 = parsed[1]
                b = self.find_value(p2)
                res = a != b
                self.intermediate_results[ind_temp - 1] = res
                return res


            elif this_op == 'AND':
                ind_temp = self.ind # to store intermediate results in a list corresponding to the operator
                acc=True
                for e in parsed:
                    acc=acc & self.find_value(e)
                self.intermediate_results[ind_temp-1] = acc
                return acc

            elif this_op == 'OR':
                ind_temp=self.ind # to store intermediate results in a list corresponding to the operator
                acc=False
                for e in parsed:
                    acc=acc | self.find_value(e)
                self.intermediate_results[ind_temp-1]=acc
                return acc

            elif this_op == 'NOT':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res=not(self.find_value(e))
                self.intermediate_results[ind_temp-1] = res
                return res

            elif this_op == 'SEL':
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                true_pass=self.find_value(parsed[0])
                selector=self.find_value(parsed[1])
                false_pass = self.find_value(parsed[2])
                if selector is True:
                    res=true_pass
                else:
                    res=false_pass
                self.intermediate_results[ind_temp-1] = res
                return res

            elif this_op == 'OUT': # Output is the same as input
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res=self.find_value(e)
                self.intermediate_results[ind_temp-1] = res
                return res

            elif this_op == 'SIN': # Output is Sine of the input. Argument is in radian
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res=math.sin(self.find_value(e))
                self.intermediate_results[ind_temp-1] = res
                return res

            elif this_op == 'SIND': # Output is Sine of the input. Argument is in degrees.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res=math.sin(math.pi/180.0*self.find_value(e))
                self.intermediate_results[ind_temp-1] = res
                return res

            elif this_op == 'COS':  # Output is Cosine of the input. Argument is in radian.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = math.cos(self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'COSD':  # Output is Cosine of the input. Argument is in degrees.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = math.cos(math.pi/180.0 * self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'TAN':  # Output is Tangent of the input. Argument is in radian.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = math.tan(self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'TAND':  # Output is Tangent of the input. Argument is in degrees.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = math.tan(math.pi/180.0 * self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'ABS':  # Output is absolute value of the input.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = abs(self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'SQRT':  # Output is square root value of the input.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    if self.find_value(e) < 0 : # Check if sqrt has non-negative argument
                        self.has_error = True
                        self.err_msg = "Negative argument in SQRT"
                        res = 0
                        break  # Terminate the for loop
                    else:
                        res = math.sqrt(self.find_value(e))
                self.intermediate_results[ind_temp - 1] = res
                return res

            elif this_op == 'NOP':  # Output is the same as input.
                ind_temp = self.ind  # to store intermediate results in a list corresponding to the operator
                for e in parsed:
                    res = self.find_value(e)
                self.intermediate_results[ind_temp - 1] = res
                return res

            else: # Did not identify the operation
                self.has_error = True
                self.err_msg = this_op+' is invalid operation'
                return 0

        else:
            return parsed


    def parse(self,expr):
        '''
        This method parses an expression in the form of nested lists along with a list of ordered operations
        '''

        '''List of supported operators.
        Note: If an operator name includes another one, e.g. SIND and SIN, the longer operator should appear first in the list.
        '''
        Operators = ['ADD', 'MUL', 'SUB', 'DIV', 'POW', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'AND', 'OR', 'NOT', 'SEL',
                     'OUT', 'SIND', 'SIN', 'COSD', 'COS', 'TAND', 'TAN', 'ABS', 'SQRT']


        # Remove blank spaces between open parentheses for example: ADD( (1,2))-->ADD((1,2)
        temp_exp = '' # Holds a temporary string
        found = False  # Initialization.
        for c in expr: # Loop through all characters in the string
            '''If the character is open parenthesis, after that ignore all blank spaces'''
            if c == '(':
                found = True
                temp_exp += c
            elif c == ' ' and found == True:
                pass
            else:
                temp_exp += c
                found = False
        expr = temp_exp
        # Convert the expression to a list of brackets and a list of operators
        open_par = 0 # Number of open parentheses in the expression. It is used to check if the expression is formatted well in terms of parentheses
        i = 0
        op = []
        out_expr = '' # This will be equal to the expression without any of the expressions
        while i< len(expr):
            found = False # Initialization
            for this_op in Operators: # Loop through all supported operations to find a match in the expression
                n = len(this_op) # Length of this operator
                if expr[i:i+n] == this_op: # At the current index of the expression, do we see the above selected operator?
                    op.append(this_op) # Store the found operation
                    found = True
                    break # We found it. Terminate the for loop

            # Adjust the index to search for the next operator
            if found == True:
                i = i + n   # There was a match, so continue the search after the newly characters
            elif i == 0  and expr[i] == '(': # If expression begins with a dummy open parenthesis it is dummy. for example (ADD(1,2))
                op.append('NOP') # No operation
                out_expr += '['
                open_par += 1 # Increment the counter
                i = i + 1  # Continue the search from next index
            elif i > 0 and expr[i] == '(' and expr[i-1] =='(': # If we have two consecutive open parenthesis, it is dummy . Example: ADD((1,2))
                op.append('NOP')
                out_expr += '['
                open_par += 1  # Increment the counter
                i = i + 1  # Continue the search from next index
            elif expr[i] == '(' : # change ( to [
                out_expr += '['
                open_par += 1  # Increment the counter
                i = i + 1  # Continue the search from next index
            elif expr[i] == ')' : # change ) to ]
                out_expr += ']'
                open_par -= 1  # Decrement the counter
                i = i + 1  # Continue the search from next index
            elif expr[i] in ['1','2','3','4','5','6','7','8','9','0','-','+',',','.',' ']: # numeric values
                out_expr += expr[i]  # Update the out_exp
                i = i + 1  # Continue the search from next index
            else: # there was an unsupported operator
                self.has_error = True
                # Find the unsupported operator to report for troubleshooting
                if open_par > 0:
                    temp_exp = expr[i:]
                else:
                    ''' If two expression are concatenated without parentheses that is a problem, e.g. ABSSIN
                    the previously found operator is also invalid because it is a part of a larger invalid string'''
                    temp_exp = op[-1] + expr[i:]


                exp_end = temp_exp.find('(')  # find the next open parentheses
                if exp_end == -1: # If there is none, go all the way to the end
                    exp_end = len(temp_exp)
                self.err_msg = 'Unsupported operator in the expression: ' + temp_exp[0:exp_end]
                break  # Terminate the while loop

        # Check for the number of parentheses. Number of open and close parentheses should be equal
        if self.has_error == False and open_par != 0 :
            self.has_error = True
            self.err_msg = 'Bad parentheses in the expression'


        # Extract the list of numbers
        if self.has_error == False :
            formatted_expr = json.loads(out_expr)
        else:
            formatted_expr = ''

        return formatted_expr,op


    def evaluate(self,expr):
        tic = time.time() # To measure the time
        formatted_expr, op=self.parse(expr)
        if self.has_error is True: # Check if expression did not have any issue
            return self.has_error, self.err_msg, 0, [], 0

        self.op=op
        self.intermediate_results = [[]] * len(op)
        self.ind=0 # Reset the index
        resultant=self.find_value(formatted_expr) # find the value of the expression
        toc = time.time() - tic
        return self.has_error,self.err_msg,resultant,self.intermediate_results,toc



if __name__ == '__main__':
    myeval=pyfeval()    
    exprs='OR(GT(SUB(ADD(1,2),MUL(6,7)),-20),EQ(3,4))'  # ((1+2)-(6x7)>-20) | (3==4)
    has_err,err_msg,val,int_res,toc=myeval.evaluate(exprs)
    if myeval.has_error == False:
        print '{} = {}'.format(exprs,val)
        print 'Intermediate results:', int_res
    else:
        print myeval.err_msg

    print 'It took ', toc * 1e6, 'micro sec to evaluate the expression'







