import math
from collections import deque

from PersonFactory import PersonFactory


class FamilyTree:
    first_people = []
    people_queue = deque()
    total_people = 0
    total_people_by_decade = {}
    names_count = {}

    def __init__(self):
        self.factory = PersonFactory()

        # generate the first two people
        self.first_people.append(
            self.factory.generate_person(1950, is_direct_descendent=False)
        )
        self.first_people.append(
            self.factory.generate_person(1950, is_direct_descendent=False)
        )
        self.update_family_stats(self.first_people[0])
        self.update_family_stats(self.first_people[1])
        self.first_people[0].set_partner(self.first_people[1])
        self.first_people[1].set_partner(self.first_people[0])
        self.first_people[0].set_is_direct_descendant(True)
        self.first_people[1].set_is_direct_descendant(True)
        self.factory.set_first_people(self.first_people)

        # start tree generation
        self.people_queue.append(self.first_people[0])
        self.generate_tree()

    # updates all relevant statistics for query
    def update_family_stats(self, person):
        if person is None:
            return
        self.total_people += 1
        year_born = person.get_year_born()
        decade = f"{math.floor(year_born / 10 ) * 10}s"
        if decade in self.total_people_by_decade:
            self.total_people_by_decade[decade] += 1
        else:
            self.total_people_by_decade[decade] = 1
        full_name = f"{person.get_first_name()} {person.get_last_name()}"
        if full_name in self.names_count:
            self.names_count[full_name] += 1
        else:
            self.names_count[full_name] = 1

    # generates the tree
    def generate_tree(self):
        # while queue is not empty
        while not len(self.people_queue) == 0:
            # get person out of the queue
            person = self.people_queue.popleft()

            # generate their spouse
            if person.get_partner() is None:
                partner = self.factory.generate_partner(person.get_year_born())
                self.update_family_stats(partner)
                person.set_partner(partner)

            # generate their children
            if not person.get_partner() is None:
                children = self.factory.get_children(
                    year_born=person.get_year_born(),
                    parent1=person,
                    parent2=person.get_partner(),
                    direct_descendant=person.is_direct_descendant(),
                )
                person.set_children(children)
                person.get_partner().set_children(children)
            else:
                children = self.factory.get_children(
                    year_born=person.get_year_born(),
                    parent1=person,
                    parent2=None,
                    direct_descendant=person.is_direct_descendant(),
                )
                person.set_children(children)

            # if there is children, add them to the queue
            if not len(children) == 0:
                for child in children:
                    self.update_family_stats(child)
                    child.set_parent(person)
                    self.people_queue.append(child)

    def get_total_number_of_people(self):
        return self.total_people

    def print_total_number_of_people_by_decade(self):
        for decade, count in self.total_people_by_decade.items():
            print(f"{decade}: {count}")

    def get_duplicate_names(self):
        duplicate_names = []
        for name, count in self.names_count.items():
            if count > 1:
                duplicate_names.append(name)
        return duplicate_names


def main():
    print("generating tree!")
    tree = FamilyTree()
    while True:
        # ask for input
        print("Are you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")
        selection = input()

        # output query information
        if selection == "T":
            print(f"The tree contains {tree.get_total_number_of_people()} people total")
        elif selection == "D":
            tree.print_total_number_of_people_by_decade()
        elif selection == "N":
            duplicate_names = tree.get_duplicate_names()
            print(
                f"There are {len(duplicate_names)} people with duplicate names in the tree:"
            )
            for name in duplicate_names:
                print(name)
        elif selection == "Q":
            break
        else:
            print("None of the above options were selected. Please try again!")


main()
