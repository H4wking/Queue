from arrays import Array
from ticketcounter.llistqueue import Queue
from ticketcounter.simpeople import TicketAgent, Passenger

import random


class TicketCounterSimulation:
    # Create a simulation object.
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        # Parameters supplied by the user.
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes

        # Simulation components.
        self._passenger_q = Queue()
        self._the_agents = Array(numAgents)
        for i in range(numAgents):
            self._the_agents[i] = TicketAgent(i + 1)

        # Computed during the simulation.
        self._total_wait_time = 0
        self._num_passengers = 0

    # Run the simulation using the parameters supplied earlier.
    def run(self):
        for cur_time in range(self._numMinutes + 1):
            self._handleArrival(cur_time)
            self._handleBeginService(cur_time)
            self._handleEndService(cur_time)

    # Print the simulation results.
    def printResults(self):
        num_served = self._num_passengers - len(self._passenger_q)
        avg_wait = float(self._total_wait_time) / num_served
        print("")
        print("Number of passengers served = ", num_served)
        print("Number of passengers remaining in line = %d" %
              len(self._passenger_q))
        print("The average wait time was %4.2f minutes." % avg_wait)

    def _handleArrival(self, cur_time):
        p = random.random()
        if p < self._arriveProb:
            passenger = Passenger(self._num_passengers, cur_time)
            self._passenger_q.enqueue(passenger)

            print('Time ', cur_time, ': Passenger ', \
                  self._num_passengers, ' arrived.')

            self._num_passengers += 1

    def _handleBeginService(self, cur_time):
        if self._passenger_q.isEmpty() == False:  # handle a customer
            agent_ID = self._find_free_agent()
            if agent_ID >= 0:  # found a free one
                this_passenger = self._passenger_q.dequeue()
                stop_time = cur_time + self._serviceTime
                self._the_agents[agent_ID].start_service(this_passenger, stop_time)

                self._total_wait_time += cur_time - this_passenger._arrival_time

                print('Time ', cur_time, ': Agent ', agent_ID, \
                      ' started serving passenger ', this_passenger.id_num(), '.')

    def _handleEndService(self, cur_time):
        agent_ID = self._find_finish_agent(cur_time)
        if agent_ID >= 0:  # found one who should complete the service
            this_passenger = self._the_agents[agent_ID].stop_service()

            print('Time ', cur_time, ': Agent ', agent_ID, \
                  ' stopped serving passenger ', this_passenger.id_num(), '.')

    def _find_free_agent(self):
        for i in range(len(self._the_agents)):
            if self._the_agents[i].is_free():
                return i  # found a free one
        return -1  # no free agent is found

    def _find_finish_agent(self, cur_time):
        for i in range(len(self._the_agents)):
            if self._the_agents[i].is_finished(cur_time):
                return i  # found a finished one
        return -1  # no finished agent is found

def main():
    num_agents = 2
    total_sim_time = 200
    interarrival_time = 5
    service_time = 6

    bison_airline_agency = TicketCounterSimulation(num_agents, total_sim_time, interarrival_time, service_time)

    print('Number of Agents: ', num_agents)
    print('Total Sim Time: ', total_sim_time)
    print('Interarrival Time: ', interarrival_time)
    print('Service Time: ', service_time)
    bison_airline_agency.run()
    bison_airline_agency.printResults()

main()