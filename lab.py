#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def updated_formula(formula, guess):
    """
    Takes the formula and updates it by removing a guess, which 
    is a tuple which a value and Boolean value. 
    """
    if formula == None:
        return None 
    #final formula to return
    result = []
    
    #if the formula is an empty list, just return it 
    if formula == []:
        return result
    
    #if there are more values in the list:
    else: 
        #look at each clause
        for clause in formula: 
            #if our guess in not in the clause 
            if guess not in clause:
                #if the guess is in clause, we do not append 
                inner_result = []
                for tup in clause:
                    if tup[0] == guess[0] and tup[1] != guess[1]:
                        #handles the case where same letter but different Boolean
                        
                        
                        if len(clause) == 0:
                            return None 
                        

                        
                        continue 
                    
                    inner_result.append(tup)
                    
                if len(inner_result) != 0:   
                    result.append(inner_result)
                    
                if len(inner_result) == 0: 
                    return None 
                
        
        return result 
        

    
def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """

    
    result = {}

    
    
    if formula is None:
        return None
    
    #check for unit clause
    for clause in formula:
        if len(clause) == 1:
            guess = clause[0]
            formula = updated_formula(formula, guess)
            if formula == None:
                return None 
            #potential issue
            result[guess[0]] = guess[1]
            
            
            
    if formula == []:
        return result
                
    
    for clause in formula:
        if clause == []:
            return None 
    
    
    #print(formula)
    val = formula[0][0][0]
    assigned_val = formula[0][0][1]
    #go through clauses and find try to find length 1 
    #reassign assigned_val based off this clause
    
    
    if val not in result:
        #looks at first value at first clause
        
        
        result[val] = assigned_val 
        #print(val, True)      
        updated = updated_formula(formula, (val, result[val]))
        #print(updated)
        assn =  satisfying_assignment(updated)
        
    
       
    if assn == None: 
        result[val] = not assigned_val 
        #print(val, False)
        updated = updated_formula(formula, (val, result[val])) 
        if updated == None:
            return None 
        #print(updated)
        assn = satisfying_assignment(updated)
            
        if assn == None: 
            return None 
        
                

            
    assn.update(result) 

    return assn 
            
    
    

def group_combinations(students, group):
    """
    Given students, which is a dictionary of the students, and
    the size of their group, returns the combinations of 
    the students of that group size
    """
    
    if group == 1:
        result1 = []
        for student in students: 
            result1.append([student])
        return result1
    
    else:
        result2 = []
        for i in range(len(students)):
            smaller_list = students[i+1:]
            for left_over in group_combinations(smaller_list, group-1):
                result2.append([students[i]]+left_over)
            
        return result2
        #recursuve step?
        



def rule_one(student_preferences, room_capacities):
    """
    Implements the first rule, which, given student_preferences and
    room_capacities, guarantees that each student is given
    a room that they selected as their preferences. 
    """
        
    result = []
    #start with an empty list 
    dict_list = student_preferences.items()
    #gets tups of ID and room choices 
    
    for i in dict_list:
        #for each tuple in dict
        result.append([])
        #intialize empty list
        
        for room in i[1]:
            #loop through rooms
            last_index = len(result)-1
            #get the last index of result to add to later 
            
            result[last_index].append((i[0]+'_'+room, True))
            #add the room combination accordingly 
            
    return result


            
            
def rule_two(student_preferences, room_capacities):
    """
    Implements the second rule, which, given student_preferences and
    room_capacities, guarantees that each student is put into one room
    but no more than 1 student per room. Essentially gets all combinations
    and assigns them with False. 
    """     
    result = []
    dict_list = student_preferences.items()
    
    room_slots = list(room_capacities.keys())
    #names = student_preferences.keys()
    
    for i in dict_list: 
        #find all groups of 2
        groups_of_2 = group_combinations(room_slots, 2)
        
        for rooms in groups_of_2:
        
            inner = []
            
            for room in rooms: 
                
                slot = ((i[0]+'_'+room, False))
                
                inner.append(slot)
            
            result.append(inner)
            
    return result


def rule_three(student_preferences, room_capacities):
    """
    Implements the third rule, which, given student_preferences and
    room_capacities, guarantees that for each room that contains N
    students, there is one student who is not in the room. 
    """ 
    result = []
    dict_list = room_capacities.items()
    students = student_preferences.keys()
    #names = student_preferences.keys()
    
    for i in dict_list: 
        if i[1] < len(students):
            #if greater than number of students, we don't have to worry
            groups = group_combinations(list(students), i[1]+1)
            
            for group in groups:
                inner = []
                
                for person in group: 
                    
                    slot = ((person+'_'+i[0], False))
                    
                    inner.append(slot)
                result.append(inner)
                
    return result 
            
    

def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    rule1 = rule_one(student_preferences, room_capacities)
    rule2 = rule_two(student_preferences, room_capacities)
    rule3 = rule_three(student_preferences, room_capacities)
    
    return rule1+rule2+rule3
    



if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    #a = {'Alice': {'basement', 'penthouse'},
#                            'Bob': {'kitchen'},
#                            'Charles': {'basement', 'kitchen'},
#                            'Dana': {'kitchen', 'penthouse', 'basement'}}
    #b =  {'basement': 1,'kitchen': 2, 'penthouse': 4}
    
    #print([[('Alice_basement', True), ('Alice_penthouse', True)], [('Bob_kitchen', True)],    [('Charles_basement', True), ('Charles_kitchen', True)], [('Dana_kitchen', True),('Dana_penthouse', True), ('Dana_basement', True)]])
    #print('next')
    #print(rule_one(a,b))
    
#    print([[('Alice_basement', False), ('Alice_kitchen', False)], [('Alice_basement', False), ('Alice_penthouse', False)], 
#            [('Alice_kitchen', False), ('Alice_penthouse', False)], [('Bob_basement', False), ('Bob_kitchen', False)], 
#            [('Bob_basement', False), ('Bob_penthouse', False)], [('Bob_kitchen', False), ('Bob_penthouse', False)], 
#            [('Charles_basement', False), ('Charles_kitchen', False)], [('Charles_basement', False), ('Charles_penthouse', False)], 
#            [('Charles_kitchen', False), ('Charles_penthouse', False)], [('Dana_basement', False), ('Dana_kitchen', False)], 
#            [('Dana_basement', False), ('Dana_penthouse', False)], [('Dana_kitchen', False), ('Dana_penthouse', False)]])

#    print([[('Alice_basement', False), ('Alice_kitchen', False)], [('Alice_basement', False), ('Alice_penthouse', False)], 
#            [('Alice_kitchen', False), ('Alice_penthouse', False)], [('Bob_basement', False), ('Bob_kitchen', False)], 
#            [('Bob_basement', False), ('Bob_penthouse', False)], [('Bob_kitchen', False), ('Bob_penthouse', False)], 
#            [('Charles_basement', False), ('Charles_kitchen', False)], [('Charles_basement', False), ('Charles_penthouse', False)], 
#            [('Charles_kitchen', False), ('Charles_penthouse', False)], [('Dana_basement', False), ('Dana_kitchen', False)], 
#            [('Dana_basement', False), ('Dana_penthouse', False)], [('Dana_kitchen', False), ('Dana_penthouse', False)]])

#[[('Alice_basement', False), ('Bob_basement', False)], 
#  [('Alice_basement', False), ('Charles_basement', False)], 
#  [('Alice_basement', False), ('Dana_basement', False)], 
#  [('Bob_basement', False), ('Charles_basement', False)], 
#  [('Bob_basement', False), ('Dana_basement', False)], 
#  [('Charles_basement', False), ('Dana_basement', False)], 
#  [('Alice_kitchen', False), ('Bob_kitchen', False), ('Charles_kitchen', False)],
#  [('Alice_kitchen', False), ('Bob_kitchen', False), ('Dana_kitchen', False)],
#  [('Alice_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)], 
#  [('Bob_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)]]
  

#print(group_combinations(list(a.keys()), 3))
#print('next')
#print(group_combinations(list(a.values()), 2))

