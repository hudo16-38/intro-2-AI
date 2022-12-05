from logic import *


class KB:
    #  Representation of whole knowledge base
    def __init__(self):
        self.clauses = []

    def __str__(self):
        return 'Knowledge base:\n{}\n'.format('\n'.join(['\t'+str(c) for c in self.clauses]))

    def print_facts(self):
        print('Facts:\n{}\n'.format('\n'.join(['\t'+str(c) for c in self.clauses if len(c.premises) == 0])))

    def tell(self, clause):
        # Tell sentence (Implication/Fact) into KB
        if not isinstance(clause, Implication):
            raise TypeError('You can only tell clauses (Implication/Fact)! You passed: {}'
                            .format(type(clause).__name__))
        if clause not in self.clauses:
            self.clauses.append(clause)

    def find_clauses_with_conclusion(self, conclusion):
        # Find all clauses with given conclusion (Literal), sort them Facts first
        return sorted([c for c in self.clauses if c.conclusion == conclusion], key=lambda c: len(c.premises) )

    def ask(self, goal_literal):
        # Backward-chaining
        if not isinstance(goal_literal, Literal):
            raise TypeError('You can only ask Literal! You asked: {}'
                            .format(type(goal_literal).__name__))
        ### Task 1 & 2
        ### YOUR CODE GOES HERE ###
        def prove(goal_literal, memo:set):
            #trivial case
            
            if goal_literal in self.clauses:
                return True

            result = False
            all_clauses = self.find_clauses_with_conclusion(goal_literal)
            memo.add(goal_literal.name) #to prevent cyclic implications

            #we are gonna check each implication
            for clause in all_clauses:
                premises = clause.premises

                #recursive solutions for each premise (they need to be true so that conclusion is true)
                for premise in premises:
                    if premise.name in memo: 
                        break

                    #memo.add(premise.name) #to prevent cyclic implications
                    temp = prove(premise, memo) #if we get False for any premise, implication is False, we try another clause
                    if not temp:
                        break
                    #memo.discard(premise.name)
                else:
                    result = True #all premises were true, so implication counts

                if result:
                    self.tell(Fact(goal_literal)) #we proved an implication, so we store the literal
                    break                         #and break the main for loop
 
            memo.discard(goal_literal.name)
            return result #then we tried all clauses, so final return is here
        
        return prove(goal_literal, set())



if __name__ == "__main__":
    # Task 1 - simple inference
    kb = KB()
    kb.tell(Implication(NOT('P'), L('Q')))            # -P => Q
    kb.tell(Implication(NOT('C'), L('P')))            # -C => P
    kb.tell(Implication(NOT('K'), L('M'), NOT('P')))  # -K ^ M => -P
    kb.tell(Implication(L('B'), NOT('K'), L('M')))    # B ^ -K => M
    kb.tell(Implication(L('A'), L('B'), NOT('K')))    # A ^ B => -K
    kb.tell(Fact(L('A')))
    kb.tell(Fact(L('B')))
    kb.tell(Fact(L('C')))
    print('Simple inference True: ', kb.ask(L('Q')))
    print('Simple inference False:', kb.ask(L('P')))

    # Task 2 - inference with cyclic rules
    kb_cyclic = KB()
    kb_cyclic.tell(Implication([L('A'), NOT('P')], NOT('K')))  # A ^ -P => -K
    for clause in kb.clauses:
        kb_cyclic.tell(clause)
    print('Cyclic rules True: ', kb_cyclic.ask(L('Q')))
    print('Cyclic rules False:', kb_cyclic.ask(L('P')))
