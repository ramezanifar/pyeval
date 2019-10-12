# pyeval
Evaluates mathematical (arithmetic and logical) expressions in python.   
I needed to evaluate mathematical expressions in python but very fast. There are many python libraries that evaluate a string but they take few miliseconds to calculate the result. For my use case, few miliseconds was detrimental.   
Untill I found this thread:  
https://stackoverflow.com/questions/15884727/recursive-boolean-evaluation  
This inspired me to work on this project. Currently the expression should be in a certain format to be parsed. for example:  
1+2 should be entered as ADD(1,2)  and  
3x(1+2) as MUL(3,ADD(1,2)) and  
3x(1+3)-4x(5/3) as SUB(MUL(3,ADD(1,3),MUL(4,DIV(5,3))) and etc.

This is the list of supported operations at the moment:  
Arithmetic operations:    
(+) : ADD    example : 1+2 as ADD(1,2)    
(-) : SUB    example : 1-2 as SUB(1,2)    
(x) : MUL    example : 1X2 as MUL(1,2)    
(/) : DIV    example : 1/2 as DIV(1,2)    
(^) : POW    example : 1^2 as POW(1,2)    

Comparisions:  
(> )  : GT    example : 1>2  as GT(1,2)  
(>=) : GE    example : 1>=2 as GE(1,2)  
(< ) : LT    example : 1<2  as LT(1,2)  
(<=) : LE    example : 1<=2 as LE(1,2)  
(==) : EQ    example : 1==2 as EQ(1,2)  
(!=) : NE    example : 1!=2 as NE(1,2)  

Boolean operations:  
& : AND    example : b1 & b2 as AND(b1,b2)  
| : OR     example : b1 | b2 as OR(b1,b2)  
! : NOT    example : !b      as NOT(b)  
