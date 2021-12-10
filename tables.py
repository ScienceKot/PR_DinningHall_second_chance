# Importing all needed libraries.
import random
import threading
import time
import uuid

# Defining the Table class.
class Table:
    def __init__(self, dinning_hall, id : int) -> int:
        '''
            The constructor of the table class.
        :param dinning_hall: DinningHall
            The DinningHall object that contains this table.
        :param id: int
            The id of the table.
        '''
        # Setting up the Table.
        self.state = "WAITING_TO_MAKE_ORDER"
        self.order = None
        self.dinning_hall = dinning_hall
        self.id = id
        self.state_lock = threading.Lock()

    def generate_order(self, waiter_id : int) -> dict:
        '''
            This function generates an random order.
        :param waiter_id: int
            The id of the waiter that took this order.
        :return: dict
            The generated order.
        '''
        # Setting up an unique id.
        order_id = str(uuid.uuid4())

        # Generating a random set of food items.
        num_items = random.randint(1, 10)
        items = random.choices(
            [self.dinning_hall.menu[i]['id'] for i in range(len(self.dinning_hall.menu))],
            k=num_items
        )

        # Computing the maximal waiting time.
        max_wait = 1.3 * max([self.dinning_hall.menu[i-1]['preparation-time'] for i in items])

        # Getting a random priority.
        priority = random.randint(1, 5)

        self.order = {
            "order_id" : order_id,
            "table_id" : self.id,
            "waiter_id" : waiter_id,
            "items" : items,
            "priority" : priority,
            "max_wait" : int(max_wait),
            "pick_up_time": int(time.time())
        }

        return self.order

    def wait_for_visitors(self) -> None:
        '''
            This function resets the state of table.
        '''
        time.sleep(random.randint(2, 4))
        self.state = "WAITING_TO_MAKE_ORDER"

    def validate_order(self, distribution : dict) -> bool:
        '''
            This function validates if a distribution is the distribution generated from the order
            generated from this table.
        :param distribution: dict
            The dictionary with the information about the distribution.
        :return: bool
            True if the ids are the same, else False.
        '''
        if not self.order or self.order['order_id'] != distribution['order_id']:
            return False
        return True

    def free_table(self) -> None:
        '''
            This function resets the table.
        '''
        self.order = None
        self.state = "FREE"

        # Stating the wait_for_visitors function.
        threading.Thread(target=self.wait_for_visitors).start()