# Importing all needed libraries.
import time
import random
import threading
import requests
from tables import Table

class Waiter:
    def __init__(self, id : int, dinning_hall) -> None:
        '''
            The constructor of the waiter class.
        :param id: int
            The id of the waiter in the dinning hall.
        :param dinning_hall: DinningHall
            The dinning hall object.
        '''
        self.serving_tables = {}
        self.distributions = []
        self.distributions_mutex = threading.Lock()
        self.dinning_hall = dinning_hall
        self.id = id

    def serve_tables(self, tables : list) -> None:
        '''
            Thin function finds tables waiting to make an order and takes it.
        :param tables: list
            The list of tables in the dinning hall.
        '''
        while True:
            # Searching for free tables.
            for table in tables:
                table.state_lock.acquire()
                if table.state == "WAITING_TO_MAKE_ORDER":
                    table.state = "WAITING_ORDER_TO_BE_SERVED"
                    table.state_lock.release()

                    # Taking an order from the chosen table.
                    self.take_order(table)
                else:
                    table.state_lock.release()
            # Distributing the prepared orders.
            self.serve_distributions()

    def add_distribution(self, distribution : dict) -> None:
        '''
            This function adds a distribution to distributions list.
        :param distribution: dict
            The dictionary with the information about the distribution.
        '''
        self.distributions_mutex.acquire()
        self.distributions.append(distribution)
        self.distributions_mutex.release()

    def serve_distributions(self):
        '''
            THis functions distributes all distributions to their tables.
        '''
        self.distributions_mutex.acquire()

        for distribution in self.distributions:
            if distribution['table_id'] not in self.serving_tables:
                continue
            # Searching a distribution is matching with the served table.
            valid_distribution = self.serving_tables[distribution['table_id']].validate_order(distribution)

            if not valid_distribution:
                continue
            # Freeing the served table.
            self.serving_tables[distribution['table_id']].free_table()
            mark = self.dinning_hall.on_order_served(distribution)

            # Removing the served tables after the order was distributed.
            del self.serving_tables[distribution["table_id"]]

        self.distributions.clear()
        self.distributions_mutex.release()

    def take_order(self, table) -> None:
        '''
            This function is taking an order from a table.
        :param table: Table
            The table from with the order is taken.
        :return:
        '''
        # Generating an order.
        order = table.generate_order(self.id)
        time.sleep(random.randint(2, 4))

        # Getting the pick-up time.
        order['pick_up_time'] = int(time.time())

        # Adding the table to the served.
        self.serving_tables[table.id] = table

        # Sending the order to the kitchen.
        r = requests.post("http://127.0.0.1:4000/order", json=order)