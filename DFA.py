import itertools

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

    min_dfa = dfa.minimize()
    print(min_dfa.accept_states)
    print(min_dfa.states)
    print(min_dfa.start_state)
    print(min_dfa.transition_function)


