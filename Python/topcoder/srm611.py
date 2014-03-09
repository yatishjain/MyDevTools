'''
Div2 I
Problem Statement
        Fox Ciel thinks that the number 41312432 is interesting. This is because of the following property: There is exactly 1 digit between the two 1s, there are exactly 2 digits between the two 2s, and so on.





Formally, Ciel thinks that a number X is interesting if the following property is satisfied: For each D between 0 and 9, inclusive, X either does not contain the digit D at all, or it contains exactly two digits D, and there are precisely D other digits between them.





You are given a String x that contains the digits of a positive integer. Return "Interesting" if that integer is interesting, otherwise return "Not interesting".
 
Definition
        
Class:  InterestingNumber
Method: isInteresting
Parameters: String
Returns:    String
Method signature:   String isInteresting(String x)
(be sure your method is public)
    
 
Constraints
-   x will correspond to an integer between 1 and 1,000,000,000, inclusive.
-   x will not start with a '0'.
 
Examples
0)  
        
"2002"
Returns: "Interesting"
There are 0 digits between the two 0s, and 2 digits between the two 2s, so this is an interesting number.
1)  
        
"1001"
Returns: "Not interesting"
There should be 1 digit between the two 1s, but there are 2 digits between them. Hence, this number is not interesting.
2)  
        
"41312432"
Returns: "Interesting"
This is the number in the statement.
3)  
        
"611"
Returns: "Not interesting"
There is only one digit 6 in this number, so it's not interesting.
4)  
        
"64200246"
Returns: "Interesting"
5)  
        
"631413164"
Returns: "Not interesting"
This number contains the digit 1 three times.
'''
class  InterestingNumber(object):
    def isInteresting(self,num):
        for i in xrange(10):
            i_str = str(i)
            c = num.count(i_str)
            if c not in [0,2]:
                return 'Not interesting'
            if c == 2 and num[num.index(i_str)+1:].index(i_str) != i:
                return 'Not interesting'
        return 'Interesting'
