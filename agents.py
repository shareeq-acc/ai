class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal

    def act(self, percept, graph):
        if percept == self.goal:
            return f"Goal {self.goal} found!"
        return self.SEARCH(graph, percept, self.goal)  # swap algorithm here

class Environment:
    def __init__(self, graph):
        self.graph = graph

    def get_percept(self, node):
        return node

def run_agent(agent, environment, start):
    percept = environment.get_percept(start)
    print(agent.act(percept, environment.graph))