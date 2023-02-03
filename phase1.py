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