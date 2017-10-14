from abc import ABC

class Quantity(ABC):
    def __init__(self, name):
        self.name = name
        self.quantity = "0"
        self.derivative = "0"
        self.quantity_space = None

    def set_derivative(self, new_derivative):
        self.derivative = new_derivative

    def increase_derivative(self):
        # Get position in quantity_space
        print(self.derivative)
        pos = self.quantity_space.index(self.derivative)
        if pos != len(self.quantity_space) - 1:
            self.derivative = self.quantity_space[pos + 1]
        else:
            print("Already max quantity space")
            # TODO: what to do here?

class Q_inflow(Quantity):
    def __init__(self):
        Quantity.__init__(self, "inflow")
        self.quantity_space = ["0", "+"]


class Q_outflow(Quantity):
    def __init__(self):
        Quantity.__init__(self, "outflow")
        self.quantity_space = ["0", "+", "max"]


class Q_volume(Quantity):
    def __init__(self):
        Quantity.__init__(self, "volume")
        self.quantity_space = ["0", "+", "max"]
