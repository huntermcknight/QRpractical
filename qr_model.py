#!/usr/bin/python3

'''
Caitlin Lagrand
Qualitative Reasoning model for bathtubs.

Quantities: inflow, outflow, volume
Quantity spaces: inflow: [0,+], outflow: [0, +, max], volume: [0, +, max]
Dependencies:
I+(Inflow, Volume) - The amount of inflow increases the volume
I-(Outflow, Volume) - The amount of outflow decreases the volume
P+(Volume, Outflow) - Outflow changes are proportional to volume changes
VC(Volume(max), Outflow(max)) - The outflow is at its highest value (max), when the volume is at its highest value (also max).
VC(Volume(0), Outflow(0)) - There is no outflow, when there is no volume.
'''

from quantity import Q_inflow, Q_outflow, Q_volume

class QR_model(object):
    def __init__(self):
        self.create_model()
        self.fill()
        self.update()

    def create_model(self):
        # Quantities
        self.q_inflow = Q_inflow()
        self.q_outflow = Q_outflow()
        self.q_volume = Q_volume()
        # Dependencies
        self.dependencies = [lambda : self.positive_influence(self.q_inflow, self.q_volume),
                             lambda : self.negative_influence(self.q_outflow, self.q_volume),
                             lambda : self.positive_proportional(self.q_volume, self.q_outflow),
                             lambda : self.value_correspondence(self.q_volume, "max", self.q_outflow, "max"),
                             lambda : self.value_correspondence(self.q_volume, "0", self.q_outflow, "0")]

    def update(self):
        for dependency in self.dependencies:
            dependency()

    def fill(self):
        ''' Fill the container by increasing the derivative of the inflow. '''
        self.q_inflow.increase_derivative()

    def empty(self):
        ''' TODO: '''
        return NotImplemented

    def positive_influence(self, quantity_from, quantity_to):
        ''' TODO: '''
        print("positive_influence from", quantity_from.name, "to", quantity_to.name)

    def negative_influence(self, quantity_from, quantity_to):
        ''' TODO: '''
        print("negative_influence from", quantity_from.name, "to", quantity_to.name)

    def positive_proportional(self, quantity_from, quantity_to):
        ''' TODO: '''
        print("positive_proportional from", quantity_from.name, "to", quantity_to.name)

    def negative_proportional(self, quantity_from, quantity_to):
        ''' TODO: '''
        print("negative_proportional from", quantity_from.name, "to", quantity_to.name)

    def value_correspondence(self, quantity_from, value_from, quantity_to, value_to):
        ''' TODO: '''
        print("value_correspondence from", quantity_from.name, "with value", value_from,
              "to", quantity_to.name, "with value", value_to)


def main():
    model = QR_model()

if __name__ == "__main__":
    main()
