import itertools
from disjoint import DisjointSet
from collections import defaultdict


class DFA:


    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def transition(self, input_symbol):
        if (self.current_state, input_symbol) in self.transition_function:
            self.current_state = self.transition_function[(
                self.current_state, input_symbol)]
        else:
            self.current_state = None

    def in_accept_state(self):
        return self.current_state in self.accept_states

    def reset(self):
        self.current_state = self.start_state

    def is_language_empty(self):
        visited = set()
        def dfs(state):
            if state in visited or state is None:
                return
            visited.add(state)
            for symbol in self.alphabet:
                next_state = self.transition_function.get((state, symbol))
                dfs(next_state)

        found_accept = False
        dfs(self.start_state)
        for state in visited:
            if state in self.accept_states:
                found_accept = True
                break
        return not found_accept

        visited = set()
        rec_stack = set()
        for state in self.states:
            if state not in visited:
                if not dfs(state, visited, rec_stack):
                    return False
        return True

    def generate_strings(self, state, current_string, max_length, list):

        if len(current_string) > max_length:
            return
        if state in self.accept_states:
            list.append(current_string)
        for symbol in self.alphabet:
            next_state = self.transition_function.get((state, symbol))
            self.generate_strings(
                next_state, current_string + symbol, max_length, list)

    def is_finite(self):
        n = len(self.states)
        listN = []
        list2N = []
        self.generate_strings(self.start_state, '', n - 1, listN)
        self.generate_strings(self.start_state, '', (2 * n) - 1, list2N)
        listN = set(listN)
        list2N = set(list2N)
        res = list2N - listN
        if len(res) == 0:
            return True
        else:
            return False

    def shortestWord(self, list):
        return len(min(list))

    def longestWord(self, list):
        return len(max(list))

    def complement(self):
        # create a new set of accept states that includes all states except the current accept states
        new_accept_states = self.states - self.accept_states
        # return a new instance of the DFA class with the new accept states
        return DFA(self.states, self.alphabet, self.transition_function, self.start_state, new_accept_states)

    @staticmethod
    def union(cls, dfa1, dfa2):

        if not isinstance(dfa1, cls):
            raise TypeError("First argument must be an instance of DFA")
        if not isinstance(dfa2, cls):
            raise TypeError("Second argument must be an instance of DFA")
        # Create a new set of states that is the union of the states of dfa1 and dfa2
        new_states = dfa1.states.union(dfa2.states)
        # Create a new set of accept states that is the union of the accept states of dfa1 and dfa2
        new_accept_states = dfa1.accept_states.union(dfa2.accept_states)
        # Create a new start state that is the tuple of the start states of dfa1 and dfa2
        new_start_state = (dfa1.start_state, dfa2.start_state)
        # Create a new transition function that combines the transition functions of dfa1 and dfa2
        new_transition_function = {}
        for state, symbol in itertools.product(new_states, dfa1.alphabet.union(dfa2.alphabet)):
            next_state1 = dfa1.transition_function.get((state, symbol))
            next_state2 = dfa2.transition_function.get((state, symbol))
            if next_state1 is None:
                new_transition_function[(state, symbol)] = next_state2
            elif next_state2 is None:
                new_transition_function[(state, symbol)] = next_state1
            else:
                new_transition_function[(state, symbol)] = (next_state1, next_state2)
        # Return a new instance of the DFA class with the new states, accept states, start state, and transition function
        return cls(new_states, dfa1.alphabet.union(dfa2.alphabet), new_transition_function, new_start_state,
                   new_accept_states)

    def union(self, dfa2):
        # Create a new alphabet that is the union of the two alphabets
        new_alphabet = self.alphabet.union(dfa2.alphabet)

        # Create a new set of states that is the cartesian product of the two sets of states
        new_states = set(itertools.product(self.states, dfa2.states))

        # Create a new start state that is a tuple of the two start states
        new_start_state = (self.start_state, dfa2.start_state)

        # Create a new set of accept states that is the cartesian product of the two sets of accept states
        new_accept_states = set(itertools.product(self.accept_states, dfa2.states)) | set(
            itertools.product(self.states, dfa2.accept_states))

        # Create a new transition function that maps from a pair of states to a new state
        new_transition_function = {}
        for state1 in self.states:
            for symbol in self.alphabet:
                next_state1 = self.transition_function.get((state1, symbol))
                for state2 in dfa2.states:
                    next_state2 = dfa2.transition_function.get((state2, symbol))
                    new_transition_function[((state1, state2), symbol)] = (next_state1, next_state2)

        # Return a new instance of the DFA class with the new states, alphabet, transition function, start state, and accept states
        return DFA(new_states, new_alphabet, new_transition_function, new_start_state, new_accept_states)
    
    @staticmethod
    def intersection(cls, dfa1, dfa2):
        return dfa1.intersection(dfa2)

    def intersection(self, dfa2):
        """
        Compute the intersection of this DFA and dfa2
        """
        # Create a new set of states by taking the Cartesian product of the states of the two DFA's
        new_states = set(itertools.product(self.states, dfa2.states))
        # Create a new alphabet by taking the union of the alphabets of the two DFA's
        new_alphabet = self.alphabet.union(dfa2.alphabet)
        # Create a new transition function by combining the transition functions of the two DFA's
        new_transition_function = {}
        for state1 in self.states:
            for state2 in dfa2.states:
                for symbol in new_alphabet:
                    new_transition_function[((state1, state2), symbol)] = (
                    self.transition_function.get((state1, symbol)), dfa2.transition_function.get((state2, symbol)))
        # Create a new start state by taking the Cartesian product of the start states of the two DFA's
        new_start_state = (self.start_state, dfa2.start_state)
        # Create a new set of accept states by taking the Cartesian product of the accept states of the two DFA's
        new_accept_states = set(itertools.product(self.accept_states, dfa2.accept_states))
        # Create and return the new DFA
        return DFA(new_states, new_alphabet, new_transition_function, new_start_state, new_accept_states)


    @staticmethod
    def difference(cls, dfa1, dfa2):
        return dfa1.difference(dfa2)

    def difference(self, dfa2):
        complement_dfa2 = dfa2.complement()
        difference_dfa = self.intersection(complement_dfa2)
        return difference_dfa

    @staticmethod
    def isSubset(cls, dfa1, dfa2):
        return dfa1.isSubset(dfa2)

    def isSubset(self, dfa2):
        return self.difference(dfa2).is_language_empty()

    @staticmethod
    def isDisjoint(cls, dfa1, dfa2):
        return dfa1.idDisjoint(dfa2)

    def isDisjoint(self, dfa2):
        return self.intersection(dfa2).is_language_empty()

    def _remove_unreachable_states(self):
        graph = defaultdict(list)

        # Build a graph with the transition states as edges
        for (from_state, _), to_state in self.transition_function.items():
            graph[from_state].append(to_state)

        # Perform a depth-first search starting from the start state
        stack = [self.start_state]
        reachable_states = set()

        while stack:
            state = stack.pop()

            if state not in reachable_states:
                stack.extend(graph[state])

            reachable_states.add(state)

        # Filter the states, final states, and transitions based on the reachable states
        self.states = [state for state in self.states if state in reachable_states]
        self.accept_states = [state for state in self.accept_states if state in reachable_states]
        self.transition_function = {key: value for key, value in self.transition_function.items() if key[0] in reachable_states}

    def minimize(self):
        self._remove_unreachable_states()

        def order_tuple(a, b):
            return (frozenset([a]), frozenset([b])) if a < b else (frozenset([b]), frozenset([a]))

        table = {}
        sorted_states = sorted(self.states)

        for i, state1 in enumerate(sorted_states):
            for state2 in sorted_states[i + 1:]:
                table[frozenset([state1, state2])] = (state1 in self.accept_states) != (state2 in self.accept_states)

        flag = True
        while flag:
            flag = False
            for i, state1 in enumerate(sorted_states):
                for state2 in sorted_states[i + 1:]:
                    if table[frozenset([state1, state2])]:
                        continue
                    for w in self.alphabet:
                        t1 = self.transition_function.get((state1, w), None)
                        t2 = self.transition_function.get((state2, w), None)
                        if t1 is not None and t2 is not None and t1 != t2:
                            marked = table[frozenset([t1, t2])]
                            flag = flag or marked
                            table[frozenset([state1, state2])] = marked
                            if marked:
                                break

        d = DisjointSet(self.states)
        for k, v in table.items():
            if not v:
                d.union(*k)

        new_states = {}
        for i, s in enumerate(d.get(), 1):
            for item in s:
                new_states[item] = str(i)

        self.states = [str(x) for x in range(1, len(d.get()) + 1)]
        new_final_states = []
        self.start_state = new_states[self.start_state]

        for s in d.get():
            for item in s:
                if item in self.accept_states:
                    new_final_states.append(new_states[item])
                    break

        self.transition_function = {(new_states[k[0]], k[1]): new_states[v] for k, v in
                                    self.transition_function.items()}
        self.accept_states = new_final_states

        def __str__(self):
            '''
            String representation
            '''
            num_of_state = len(self.states)
            start_state = self.start_state
            num_of_final = len(self.final_states)

            return '{} states. {} final states. start state - {}'.format( \
                num_of_state, num_of_final, start_state)


if __name__ == '__main__':

    states = {'S1', 'S2', 'S3', 'S4', 'S5'}

    # Define the alphabet of the DFA
    alphabet = {'a', 'b'}

    # Define the transition function of the DFA (A DFA that just accepts )
    transition_function = {
        ('S1', 'a'): 'S2',
        ('S1', 'b'): 'S2',
        ('S2', 'a'): 'S3',
        ('S2', 'b'): 'S4',
        ('S3', 'a'): 'S5',
        ('S3', 'b'): 'S5',
        ('S4', 'a'): 'S3',
        ('S4', 'b'): 'S5',
        ('S5', 'b'): 'S5',
        ('S5', 'a'): 'S5',
    }

    # Define the start state of the DFA
    start_state = 'S1'

    # Define the accept states of the DFA
    accept_states = {'S2', 'S3'}

    # Create the DFA. This DFA just accepts 'ba', 'a', 'b', 'aa', 'aba', 'bba' strings.
    dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

    # Test the DFA on some input strings
    input_strings = ['aaa', 'ba', 'a', 'b', 'aa', 'aba', 'bba', 'bbb']

    print("Test the DFA on some strings \n")

    for s in input_strings:
        dfa.reset()
        for c in s:
            dfa.transition(c)
        print(f'{s}: {dfa.in_accept_state()}')

    # Now we check if the language that the DFA accepts is empty or not.

    print('\n')

    if dfa.is_language_empty():
        print("Language accepted by DFA is empty")
    else:
        print("Language accepted by DFA is not empty")

    print('\n')

    # We can see that the language is not empty.

    if dfa.is_finite():
        print("The language accepted by the DFA is finite \n"
              "and it accepts these following strings: \n ")
        accepted_strings = []
        dfa.generate_strings(dfa.start_state, '', len(dfa.states), accepted_strings)
        print(accepted_strings)
        print('\n')
        print('length of the shortest string is : ', dfa.shortestWord(accepted_strings))
        print('\n')
        print('length of the longest string is : ', dfa.longestWord(accepted_strings))
        print('\n')
    else:
        print("Language accepted by DFA is not finite")

    # Now we create the complement of our DFA.
    print('Creating the DFA\'s complement...')
    print('\n')
    complement = dfa.complement()

    # Check if complemnt of our DFA is empty or not.

    if complement.is_language_empty():
        print("Language accepted by the complement of our DFA is empty")
    else:
        print("Language accepted by the complement of our DFA is not empty")

    print('\n')

    if complement.is_finite():
        print("Language accepted by the complement of our DFA is finite")
    else:
        print("Language accepted by the complement of our DFA is not finite")

    # Some strings that the complement of our DFA accepts
    print('\n')
    print('Some strings that the complement of our DFA accepts')
    print('\n')
    complement_accepted_strings = []
    complement.generate_strings(complement.start_state, '', 3, complement_accepted_strings)
    print(complement_accepted_strings)
    print('\n')
    print('length of the shortest string is : ', complement.shortestWord(complement_accepted_strings))
    print('\n')

    # Creating Two DFA's. The dfa1 accepts string without substring 'aa' and dfa2 accepts strings that end with 'ab.

    dfa1 = DFA({'A', 'B', 'C'},
        {'a', 'b'},
        {
            ('A', 'a'): 'B',
            ('A', 'b'): 'A',
            ('B', 'a'): 'C',
            ('B', 'b'): 'A',
            ('C', 'a'): 'C',
            ('C', 'b'): 'C',
        },
        'A',
        {'A', 'B'}
        )
    dfa2 = DFA({'P', 'Q', 'R'},
        {'a', 'b'},
        {
               ('P', 'a'): 'Q',
               ('P', 'b'): 'P',
               ('Q', 'a'): 'Q',
               ('Q', 'b'): 'R',
               ('R', 'a'): 'Q',
               ('R', 'b'): 'P',
        },
        'P',
        {'R'}
        )

    # Creating the union of these two DFA's in both demanded ways and checking some of its properties
    dfa_union = DFA.union(dfa1, dfa2)
    print('states: ',dfa_union.states)
    print('Accepting states: ',dfa_union.accept_states)
    print('Transition Function: ',dfa_union.transition_function)
    print('DFA alphabet: ',dfa_union.alphabet)
    print('Start states: ',dfa_union.start_state)

    union = dfa1.union(dfa2)
    print('states: ', union.states)
    print('Accepting states: ', union.accept_states)
    print('Transition Function: ', union.transition_function)
    print('DFA alphabet: ', union.alphabet)
    print('Start states: ', union.start_state)


    unionStrings = []
    union.generate_strings(union.start_state, '', len(union.states), unionStrings)
    print(unionStrings)

    if union.is_finite():
        print('union is finite')
    else:
        print('union is not finite')

    # Creating the intersection of these two DFA's in both demanded ways and checking some of its properties.

    inter = dfa1.intersection(dfa2)
    print('states: ', inter.states)
    print('Accepting states: ', inter.accept_states)
    print('Transition Function: ', inter.transition_function)
    print('DFA alphabet: ', inter.alphabet)
    print('Start states: ', inter.start_state)

    intersection = DFA.intersection(dfa1, dfa2)
    print('states: ', intersection.states)
    print('Accepting states: ', intersection.accept_states)
    print('Transition Function: ', intersection.transition_function)
    print('DFA alphabet: ', intersection.alphabet)
    print('Start states: ', intersection.start_state)

    intersectionStrings = []
    intersection.generate_strings(intersection.start_state, '', len(intersection.states), intersectionStrings)
    print(intersectionStrings)

    if intersection.is_finite():
      print('Intersection is finite')
    else:
      print('Intersection is not finite')

    # Creating the difference of these two DFA's in both demanded ways.

    diff = dfa1.difference(dfa2)
    print('states: ', diff.states)
    print('Accepting states: ', diff.accept_states)
    print('Transition Function: ', diff.transition_function)
    print('DFA alphabet: ', diff.alphabet)
    print('Start states: ', diff.start_state)


    difference = DFA.difference(dfa1, dfa2)
    print('difference states: ', difference.states)
    print('difference Accepting states: ', difference.accept_states)
    print('difference Transition Function: ', difference.transition_function)
    print('difference DFA alphabet: ', difference.alphabet)
    print('difference Start states: ', difference.start_state)

    differenceStrings = []
    difference.generate_strings(difference.start_state, '', len(difference.states), differenceStrings)
    print(differenceStrings)


    # Checking if these two DFA's are disjoint or not
    print(dfa1.isDisjoint(dfa2))
    # Checking if dfa1 is a subset of dfa1 U dfa2 (it always must be true)
    print(dfa1.isSubset(union))
