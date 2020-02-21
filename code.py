# A program that shows how the data in the routing tables of routers
# changes when the devices communicate with each other.


class Router:
    """
    The Router Class simulates Routing Protocols
    """

    def __init__(self,router_name):
        """
        The __init__ method accepts an arguement for the name of a Router and
        it is assigned into __router_name. It also adds the router information
        into a combined datastructure(a dict that contains dict that contains
        a list("neighbours") and a dict("routing_table"))

        :param: router_name: str, name of the router
        :return: None

        """

        self.__router_name = router_name
        self.__router_dict = {}
        if self.__router_name not in self.__router_dict.keys():
            self.__router_dict[self.__router_name] = {"neighbours": [],
                                                      "routing_table": {}}

    def print_info(self):
        """
        prints the name of the router and its neighbour routers and the routing
        table. If there is no router with this name, an error message will be
        provided for the user.
        :param:
        :return: None

        """
        routing_table = self.__router_dict[self.__router_name].\
            get("routing_table")

        neighbours = self.__router_dict[self.__router_name].get("neighbours")

        router_name = self.__router_name

        print(" ", router_name)
        print("   ", "N:", ', '.join([item for item in sorted(neighbours)]))

        print("   ", "R:", ', '.join([(network+":"+str(distance))
                                      for network, distance in
                                      sorted(routing_table.items())]))

    def add_neighbour(self, neighbour_router):
        """
        Takes a router object as an arguement and adds the neighbours to the
        router it is called for
        :param: neighbour_router: Router object, object of neighbour router
        :return: None
        """
        neighbour_router_name = neighbour_router.get_router_name()
        neighbours = self.__router_dict[self.__router_name].get("neighbours")
        if neighbour_router_name not in neighbours:
            neighbours.append(neighbour_router_name)

    def get_router_name(self):
        """
        Gets the name of the router it is called for.
        :param:
        :return: router_name: str, name of the router.
        """
        router_name = self.__router_name
        return router_name

    def get_neighbour(self):
        """
        Gets the name of the neighbour routers it is called for.
        :param:
        :return: neighbours: str(list), list of neighbour routers
        """
        neighbours = self.__router_dict[self.__router_name].get("neighbours")
        return neighbours

    def get_routing_table(self):
        """
        Gets the routing table of the router it is called for.

        :param:
        :return: routing_table: dict, routing table of a router (where address
        of the network is the 'key' and distance to the network is the 'value')
        """
        routing_table = self.__router_dict[self.__router_name]\
            .get("routing_table")
        return routing_table

    def add_network(self, address, distance):
        """
        Takes address and distance as arguements and adds them into routing
        table of the router it is called for.

        :param address: str, address of the network
        :param distance: int, distance to the network
        :return: None
        """
        self.__router_dict[self.__router_name]["routing_table"][address]\
            = distance

    def receive_routing_table(self, sender):
        """
        Adds the content of the other router's routing table into its own
        routing table.
        :param sender: Router object, object of the router which routing table
        needs to be sent.
        :return: None
        """
        sender_routing_table = sender.get_routing_table()
        receiver_routing_table = self.get_routing_table()
        for key, value in sender_routing_table.items():
            if key not in receiver_routing_table:
                receiver_routing_table[key] = value + 1

    def has_route(self,network_name):
        """
        Accepts name of the network as an arguement and tells if a certain
        router has a connection to that network.
        :param network_name: str, name of the network
        :return: None
        """
        routing_table = self.get_routing_table()
        if network_name in routing_table:
            distance = routing_table.get(network_name)
            if distance == 0:
                print("Router is an edge router for the network.")
            else:
                print("Network", network_name, "is", distance, "hops away")
        else:
            print("Route to the network is unknown.")


def filecheck(file_obj):
    """
    Accepts a file object as a parameter and checks if it has any errornamous
    line or not. If no error found then it stores the router names and their
    correspondig objects into a dict (router_dict) which is initially empty and
    calls the give_command function. Otherwise it will return 0.

    :param file_obj: File object,
    :return: None (if file does not contain any error errornamous)
          or 0 (if the file has errornamous line)

    """

    router_dict = {}

    for line in file_obj:

        # "count" variable will store number of '!' sign
        # a valid line will always contain 2 '!' signs
        count = 0

        row = line.rstrip().split()
        for ch in row[0]:
            if ch == "!":
                count += 1

        if count == 2:
            row = line.rstrip().split("!")

            if len(row) == 3:

                router_name = row[0]

                neighbour = row[1].split(";")
                neighbour = [x for x in neighbour if x != ""]

                network = row[2].split(":")
                network = [x for x in network if x != ""]

                router_obj = Router(router_name)
                router_dict[router_name] = router_obj

                if len(neighbour) > 0:
                    for items in neighbour:
                        router_obj.add_neighbour(Router(items))

                if len(network) == 2:
                    try:
                        distance = int(network[1])
                        address = network[0]
                        router_obj.add_network(address, distance)
                    except ValueError:
                        return 0

        else:
            return 0

    give_command(router_dict)


def give_command(router_dict):
    """
    Perform tasks regarding the contents of the command line interpreter. At
    first, it waits for a command from the user. If the user enters an unknown
    command the program will print an error message. For a valid command, it
    will call certain methods of class Router using certain objects from the
    router dict which it takes as a parameter. It also updates the router dict
    if a new router is added.

    :param router_dict: dict, Dict of the router which has router name as key
    and their corresponding objects as value.
    :return: None
    """

    while True:
        command = input("> ")
        command = command.upper()

        if command == "P":
            router_name = input("Enter router name: ")
            if router_name in router_dict:
                router_obj = router_dict.get(router_name)
                router_obj.print_info()
            else:
                print("Router was not found.")

        elif command == "PA":
            for router_objects in router_dict.values():
                router_objects.print_info()

        elif command == "S":
            sending_router = input("Sending router: ")
            sending_router_obj = router_dict.get(sending_router)
            receiving_routers = sending_router_obj.get_neighbour()
            for items in receiving_routers:
                receiving_router_obj = router_dict.get(items)
                receiving_router_obj.receive_routing_table(sending_router_obj)

        elif command == "C":
            router_1 = input("Enter 1st router: ")
            router_2 = input("Enter 2nd router: ")
            if router_1 in router_dict.keys() and \
                    router_2 in router_dict.keys():
                router1_obj = router_dict.get(router_1)
                router2_obj = router_dict.get(router_2)

                router1_obj.add_neighbour(router2_obj)
                router2_obj.add_neighbour(router1_obj)
            else:
                print("Router was not found.")

        elif command == "RR":
            router_name = input("Enter router name: ")
            network_name = input("Enter network name: ")
            if router_name in router_dict:
                router_obj = router_dict.get(router_name)
                router_obj.has_route(network_name)
            else:
                print("Router was not found.")

        elif command == "NR":
            router_name = input("Enter a new name: ")
            if router_name not in router_dict:
                router_dict[router_name] = Router(router_name)
            else:
                print("Name is taken.")

        elif command == "NN":
            router_name = input("Enter router name: ")
            if router_name in router_dict.keys():
                network = input("Enter network: ")
                distance = int(input("Enter distance: "))
                router_obj = router_dict.get(router_name)
                router_obj.add_network(network, distance)
            else:
                print("Router was not found.")

        elif command == "Q":
            print("Simulator closes.")
            return

        else:
            print("Erroneous command!")
            print("Enter one of these commands:")
            print("NR (new router)")
            print("P (print)")
            print("C (connect)")
            print("NN (new network)")
            print("PA (print all)")
            print("S (send routing tables)")
            print("RR (route request)")
            print("Q (quit)")


def main():
    """
    First, it asks for a file name. If the user enters a file name, then it is
    checked by filecheck funtion. If any error is found, it will print an error
    messege and the program will be terminated. If the user does not enter a
    file name, the program calls the give_command funtion with a router dict
    which is empty.
    :return: None
    """
    routerfile = input("Network file: ")
    if routerfile != "":
        try:
            file_obj = open(routerfile,"r")
            error_check = filecheck(file_obj)
            file_obj.close()

            if error_check == 0:
                print("Error: the file could not be read or "
                      "there is something wrong with it.")

        except IOError:
            print("Error: the file could not be read or "
                  "there is something wrong with it.")
        except OSError:
            print("Error: the file could not be read or "
                  "there is something wrong with it.")
    else:
        router_dict = {}
        give_command(router_dict)


main()
