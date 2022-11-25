from action.action_wrapper import ActionWrapper, SearchBotAction


class ProbabilityAction(ActionWrapper):

    action_wrapper: ActionWrapper
    probability: float

    def __init__(
        self,
        action_wrapper: ActionWrapper,
        probability: float,
    ):
        self.action_wrapper = action_wrapper
        self.probability = probability

    def get_action(self) -> SearchBotAction:
        return self.action_wrapper.action

    def __str__(self) -> str:
        return str(self.action_wrapper) + " (" + round(self.probability*100) + "% chance"