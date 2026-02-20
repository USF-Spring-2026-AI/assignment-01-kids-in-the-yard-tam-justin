import pandas as pd
import random
import math

from Person import Person


class PersonFactory:
    first_people = []

    def __init__(self):
        # read all files
        self.read_files()
        return

    def set_first_people(self, first_people):
        self.first_people = first_people

    # reads in all data files into their own df
    def read_files(self):
        print("reading files!")
        self.first_names_df = pd.read_csv("first_names.csv")
        self.last_names_df = pd.read_csv("last_names.csv")
        self.birth_marriage_df = pd.read_csv("birth_and_marriage_rates.csv")
        self.life_expectancy_df = pd.read_csv("life_expectancy.csv")
        self.rank_probability_df = pd.read_csv("rank_to_probability.csv", header=None).T

    # returns a year of death based on their birth year
    def get_year_died(self, year_born):
        sel_rows = self.life_expectancy_df[self.life_expectancy_df["Year"] == year_born]
        life_expectancy = int(sel_rows["Period life expectancy at birth"].values[0])
        return random.randint(
            year_born + (life_expectancy - 10), year_born + (life_expectancy + 10)
        )

    # returns a first name based on their birth year
    def get_first_name(self, year_born):
        decade = f"{math.floor(year_born / 10 ) * 10}s"
        sel_rows = self.first_names_df[self.first_names_df["decade"] == decade]
        first_names = sel_rows["name"].tolist()
        frequencies = sel_rows["frequency"].tolist()
        return random.choices(first_names, frequencies)[0]

    # returns one of the two last names if they are direct descendants or one based off of their birth year
    def get_last_name(self, direct_descendant, year_born):
        if direct_descendant:
            return random.choice(
                [
                    self.first_people[0].get_last_name(),
                    self.first_people[1].get_last_name(),
                ]
            )
        else:
            decade = f"{math.floor(year_born / 10 ) * 10}s"
            sel_rows = self.last_names_df[self.last_names_df["Decade"] == decade]
            last_names = sel_rows["LastName"].tolist()
            probability = self.rank_probability_df[0].tolist()
            return random.choices(last_names, probability)[0]

    # calculates if a person has a partner based on their birth year and returns a Person object (partner) or None
    def generate_partner(self, year_born):
        decade = f"{math.floor(year_born / 10 ) * 10}s"
        sel_rows = self.birth_marriage_df[self.birth_marriage_df["decade"] == decade]
        probability = sel_rows["marriage_rate"].values[0]
        if random.choices([True, False], [probability, 1 - probability]):
            partner_year_born = random.randint(year_born - 10, year_born + 10)
            if partner_year_born > 2120:
                return None
            return self.generate_person(
                year_born=partner_year_born, is_direct_descendent=False
            )

    # returns an array with People objects (children) with their birth year based on the eldest parent's birth year (can be an empty array)
    def get_children(self, year_born, parent1, parent2, direct_descendant):
        # calculate and format into a decade
        decade = f"{math.floor(year_born / 10 ) * 10}s"
        # retrieve num of children
        sel_rows = self.birth_marriage_df[self.birth_marriage_df["decade"] == decade]
        birth_rate = float(sel_rows["birth_rate"].values[0])
        num_children = random.randrange(
            round(birth_rate - 1.5), round(birth_rate + 1.5)
        )

        # find eldest parent if there are two parents
        eldest_parent = parent1
        if not parent2 is None:
            if parent2.get_year_born() < parent1.get_year_born():
                eldest_parent = parent2

        # calculate distribution (10 on default i.e 1 child)
        distribution = 10
        if num_children > 1:
            birth_range = [
                eldest_parent.get_year_born() + 25,
                eldest_parent.get_year_born() + 45,
            ]
            distribution = round((birth_range[1] - birth_range[0]) / (num_children - 1))

        # generate children
        children = []
        for i in range(num_children):
            birth_year = (eldest_parent.get_year_born() + 25) + (i * distribution)
            if birth_year > 2120:
                return children
            children.append(
                self.generate_person(birth_year, is_direct_descendent=direct_descendant)
            )
        return children

    # returns a Person object
    def generate_person(self, year_born, is_direct_descendent):
        if year_born > 2120:
            return None
        year_died = self.get_year_died(year_born)
        first_name = self.get_first_name(year_born)
        last_name = self.get_last_name(is_direct_descendent, year_born)
        return Person(
            year_born=year_born,
            year_died=year_died,
            first_name=first_name,
            last_name=last_name,
            direct_descendant=is_direct_descendent
        )
