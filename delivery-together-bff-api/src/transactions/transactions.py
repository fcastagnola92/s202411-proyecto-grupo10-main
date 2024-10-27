class SagaStep:
    def __init__(self, name, action, compensation=None):
        self.name = name
        self.action = action
        self.compensation = compensation
        self.result = None

class Saga:
    def __init__(self):
        self.steps = []

    def add_step(self, name, action, compensation=None):
        step = SagaStep(name, action, compensation)
        self.steps.append(step)
        return step  
    
    def execute(self):
        for step in self.steps:
            try:
                print(f"excecuting step: {step.name}")
                step.result =step.action
            except Exception as e:
                print(f"Error in step {step.name}: {e}")
                self.compensate(step)
                raise SagaError(f"Error in step {step.name}: {e}")

    def compensate(self, failed_step):
        print("Compensating for previous steps...")
        for step in reversed(self.steps):
            if step == failed_step:
                break
            if step.compensation:
                try:
                    print(f"Compensating step: {step.name}")
                    step.compensation()
                except Exception as e:
                    print(f"Error compensating the step {step.name}: {e}")

    def setLastStatusCode(self,status_code):
        self.lastStatusCode=status_code

    def getLastStatusCode(self):
        return self.lastStatusCode

class SagaError(Exception):
    pass


class SagaContext:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)