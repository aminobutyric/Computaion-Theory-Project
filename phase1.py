class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states


    def transition(self, input_symbol):
        if (self.current_state, input_symbol) in self.transition_function:
            self.current_state = self.transition_function[(self.current_state, input_symbol)]
        else:
            self.current_state = None

    def in_accept_state(self):
        return self.current_state in self.accept_states

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
            self.generate_strings(next_state, current_string + symbol, max_length, list)
        
    
states = {'S1', 'S2', 'S3', 'S4', 'S5'}

# Define the alphabet of the DFA
alphabet = {'a', 'b'}

# Define the transition function of the DFA
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

# Create the DFA
dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

# Test the DFA on some input strings
input_strings = ['ab', 'aaa', 'bb', 'aab', 'a', 'baa']