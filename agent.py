# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """
    A simple reflex agent.
    It uses only current IF-THEN conditions and stores no history.
    """

    def sense_and_act(self, percept: dict) -> str:
        if percept["food_here"]:
            return "Up"

        if percept["wall_ahead"]:
            return "Left"

        return "Up"


class ModalBasedAgent:
    """
    A model-based reflex agent that stores recent percepts and actions.
    It uses memory to avoid selecting the same unsuccessful action repeatedly.
    """

    def __init__(self):
        self.last_action = None
        self.last_percept = None
        self.failed_actions = set()


    def sense_and_act(self, percept: dict) -> str:
        possible_actions = ["Up", "Right", "Down", "Left"]

        # Update internal state using the previous action and current sensor result
        if (
            self.last_action is not None
            and percept["wall_ahead"]
        ):
            self.failed_actions.add(self.last_action)


        # Food is collected automatically by the environment.
        # The agent still needs to select a movement action.
        if percept["food_here"]:
            action = self._choose_untried_action(possible_actions)

        elif percept["wall_ahead"]:
            action = self._choose_untried_action(possible_actions)

        else:
            # Continue the previous direction when it appears safe
            if (
                self.last_action is not None
                and self.last_action not in self.failed_actions
            ):
                action = self.last_action
            else:
                action = self._choose_untried_action(possible_actions)

        # Store information for the next decision
        self.last_percept = dict(percept)
        self.last_action = action

        return action

    def _choose_untried_action(self, actions: list[str]) -> str:
        for action in actions:
            if action not in self.failed_actions:
                return action

        # All actions were previously marked as failed
        self.failed_actions.clear()
        return actions[0]
