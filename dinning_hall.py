# Importing all needed functions.
import time
import threading

from tables import Table
from waiter import Waiter

# Defining the Dinning Hall class.
def get_mark_for_order(order_prep_time : float, max_wait : int) -> int:
    '''
        This function gives a mark to an order.
    :param order_prep_time: float
        The order preparation time.
    :param max_wait: int
        The maximal time that can a order to be waited for
    :return: int
        The mark given to the order preparation.
    '''
    if order_prep_time < max_wait:
        return 5
    elif order_prep_time < max_wait * 1.1:
        return 4
    elif order_prep_time < max_wait * 1.2:
        return 3
    elif order_prep_time < max_wait * 1.3:
        return 2
    elif order_prep_time < max_wait * 1.4:
        return 1
    else:
        return 0


class DinningHall:
    def __init__(self, settings : dict) -> None:
        '''
            The constructor of the Dinning Hall.
        :param settings: dict
            The dictionary with the settings of the Dinning hall.
        '''
        # Creating the list of tables.
        self.tables = [Table(dinning_hall = self, id=i) for i in range(settings['n_tables'])]

        # Creating the list of waiters.
        self.waiters = {i:Waiter(i, self) for i in range(settings['n_waiters'])}

        # Setting up the menu.
        self.menu = settings['menu']

        # Defining the order preparation variables.
        self.prepared_orders = {}
        self.prepared_orders_semaphore = threading.BoundedSemaphore(value=1)
        self.marks = []

    def run(self) -> None:
        '''
            The main running function.
        '''
        # Staring all waiters in the dinning hall.
        for waiter_id, waiter in self.waiters.items():
            threading.Thread(target=waiter.serve_tables, args=(self.tables, )).start()

    def notify_order_recieve(self, distribution : dict) -> None:
        '''
            This function adds to the waiter a distribution that it must sent to the table.
        :param distribution: dict
            The dictionary with the information about the distribution.
        '''
        # Getting the waiter who served the order from which this distribution of generated.
        waiter = self.waiters[distribution['waiter_id']]

        # Adding the distribution to the waiters distributions.
        waiter.add_distribution(distribution)

    def on_order_served(self, distribution : dict) -> int:
        '''
            This function count the time taken for an order to be prepared and gives a mark.
        :param distribution: dict
            The dictionary with the information about the distribution.
        :return: int
            The mark given to the order preparation.
        '''
        # Computing the total preparation time for the order.
        order_total_preparing_time = int(time.time()) - distribution['pick_up_time']

        # Calculating the the mark of the order.
        mark = get_mark_for_order(order_total_preparing_time, distribution['max_wait'])
        print(f"order_id = {distribution['order_id']}, mark - {mark}")
        # Adding the mark to the previous marks.
        self.marks.append(mark)

        return mark
