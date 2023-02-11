from DFA import *


class NFA:
    def __init__(self, states_nfa, alphabet_nfa, transition_function_nfa, start_state_nfa, accept_states_nfa):
        self.states = states_nfa
        self.alphabet = alphabet_nfa
        self.transition_function = transition_function_nfa
        self.start_state = start_state_nfa
        self.accept_states = accept_states_nfa

    def is_accepted(self, nfa_string):
        current_states = self.get_epsilon_closure([self.start_state])
        for char in nfa_string:
            current_states = self.get_epsilon_closure(self.move(current_states, char))
            if not current_states:
                return False
        return any(state in self.accept_states for state in current_states)

    def move(self, move_states, char):
        moving_result = set()
        for state in move_states:
            for trans_state in self.transition_function.get((state, char), []):
                moving_result.add(trans_state)
        return moving_result

    def get_epsilon_closure(self, ep_states):
        epsilon_result = set(ep_states)
        stack = list(ep_states)
        while stack:
            state = stack.pop()
            for trans_state in self.transition_function.get((state, None), []):
                if trans_state not in epsilon_result:
                    epsilon_result.add(trans_state)
                    stack.append(trans_state)
        return epsilon_result

    def to_dfa(self):
        dfa_states = []
        dfa_alphabet = self.alphabet
        dfa_transition_function = {}
        dfa_start_state = frozenset(self.get_epsilon_closure([self.start_state]))
        dfa_accept_states = []

        stack = [dfa_start_state]
        while stack:
            current_state = stack.pop()
            if current_state not in dfa_states:
                dfa_states.append(current_state)
            for char in dfa_alphabet:
                next_state = frozenset(self.get_epsilon_closure(self.move(current_state, char)))
                dfa_transition_function[(current_state, char)] = next_state
                if next_state not in dfa_states:
                    stack.append(next_state)
        for state in dfa_states:
            if any(accept_state in state for accept_state in self.accept_states):
                dfa_accept_states.append(state)

        return DFA(dfa_states, dfa_alphabet, dfa_transition_function, dfa_start_state, dfa_accept_states)


nfaStates = {0, 1, 2, 3, 4, 5}

# Define the alphabet used by the NFA
nfaAlphabet = {'a', 'b'}

# Define the transition function of the NFA
nfa_transition_function = {
    (0, 'a'): (1,),
    (0, None): (3,),
    (1, 'a'): (2,),
    (2, 'b'): (0,),
    (3, 'a'): (3, 4),
    (4, 'b'): (5,),
    (5, 'a'): (3,),
}
# Define the start state of the NFA
nfa_start_state = 0

# Define the accept states of the NFA
nfa_accept_states = {3}

# Create an instance of the NFA
nfa = NFA(nfaStates, nfaAlphabet, nfa_transition_function, nfa_start_state, nfa_accept_states)

# Test the NFA on some input strings
nfa_strings = ['a', 'aab', 'aaba', 'aba', 'abab', 'abababab', '']
for string in nfa_strings:
    result = nfa.is_accepted(string)
    print(f"{string}: {result}")

print("covert the NFA to a DFA...")
print("\n")
cDFA = nfa.to_dfa()
print("the number of states:", len(cDFA.states))
print("\n")
print("The Converted NFA States: ", cDFA.states)
print("\n")

print("minimize the converted DFA...")
print("\n")

cDFA.minimize()
print("the minimized number of states:", len(cDFA.states))
print("\n")
print("minimized DFA's states: ", cDFA.states)
print("\n")
print("Minimized DFA's transition function", cDFA.transition_function)
print("\n")
