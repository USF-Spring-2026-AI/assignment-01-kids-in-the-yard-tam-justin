import random
import math
import pandas as pd
from collections import defaultdict

class Person:
    """
    Acts as a node in the family tree, keeping details of each simulated person.
    """
    def __init__(self, first_name, last_name, year_born, year_died, is_direct_descendant=False):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.year_died = year_died
        self.is_direct_descendant = is_direct_descendant
        self.partner = None
        self.children = []

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_partner(self, partner):
        self.partner = partner

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        partner_name = self.partner.get_full_name() if self.partner else "None"
        return f"{self.get_full_name()} ({self.year_born}-{self.year_died}) | Partner: {partner_name} | Children: {len(self.children)}"


class PersonFactory:
    """
    Responsible for reading the exact CSV data files and generating new instances of the Person class.
    """
    def __init__(self):
        self.read_files()

    def read_files(self):
        # 1. Rank to Probability
        df_rp = pd.read_csv('rank_to_probability.csv', header=None)
        self.rank_probs = df_rp.values[0].tolist()

        # 2. Last Names
        df_ln = pd.read_csv('last_names.csv')
        self.last_names = {}
        for decade, group in df_ln.groupby('Decade'):
            self.last_names[decade] = group.sort_values('Rank')['LastName'].tolist()

        # 3. Life Expectancy
        df_le = pd.read_csv('life_expectancy.csv')
        self.life_expectancy = dict(zip(df_le['Year'], df_le['Period life expectancy at birth']))
        self.min_le_year = df_le['Year'].min()
        self.max_le_year = df_le['Year'].max()

        # 4. Gender Name Probability
        df_gp = pd.read_csv('gender_name_probability.csv')
        self.gender_prob = {}
        for _, row in df_gp.iterrows():
            if row['decade'] not in self.gender_prob:
                self.gender_prob[row['decade']] = {}
            self.gender_prob[row['decade']][row['gender']] = row['probability']

        # 5. First Names
        df_fn = pd.read_csv('first_names.csv')
        self.first_names = {}
        for (decade, gender), group in df_fn.groupby(['decade', 'gender']):
            self.first_names[(decade, gender)] = list(zip(group['name'], group['frequency']))

        # 6. Birth and Marriage Rates
        df_bm = pd.read_csv('birth_and_marriage_rates.csv')
        self.bm_rates = {}
        for _, row in df_bm.iterrows():
            self.bm_rates[row['decade']] = {
                'birth': row['birth_rate'],
                'marriage': row['marriage_rate']
            }

    def get_decade_str(self, year):
        decade = (year // 10) * 10
        decade = max(1950, min(2120, decade))  
        return f"{decade}s"

    def generate_life_expectancy(self, year_born):
        lookup_year = max(self.min_le_year, min(self.max_le_year, year_born))
        base_expectancy = self.life_expectancy[lookup_year]
        variance = random.randint(-10, 10)
        return year_born + int(round(base_expectancy)) + variance

    def get_person(self, year_born, is_direct_descendant=False, root_last_names=None):
        decade = self.get_decade_str(year_born)

        # Combine both male and female names for the decade into one pool
        names_info_male = self.first_names.get((decade, 'male'), [])
        names_info_female = self.first_names.get((decade, 'female'), [])
        all_names_info = names_info_male + names_info_female
        
        first_names = [x[0] for x in all_names_info]
        # random.choices will automatically handle weights that don't sum to 1.0
        probs = [x[1] for x in all_names_info] 
        
        first_name = random.choices(first_names, weights=probs, k=1)[0]
        # ------------------------------------------

        # Last Name Logic
        if is_direct_descendant and root_last_names:
            # Direct descendants keep the last name of either of the first two people
            chosen_last_name = random.choice(root_last_names)
        else:
            # Partners (non-direct) get a ranked probability last name
            names = self.last_names[decade]
            chosen_last_name = random.choices(names, weights=self.rank_probs, k=1)[0]

        year_died = self.generate_life_expectancy(year_born)
        
        return Person(first_name, chosen_last_name, year_born, year_died, is_direct_descendant)

    def get_partner(self, person):
        year_born = person.year_born + random.randint(-10, 10)
        return self.get_person(year_born, is_direct_descendant=False)


class FamilyTree:
    """
    The driver class responsible for keeping references to the root Person instances.
    Data is traversed as a tree rather than held in a flat list.
    """
    def __init__(self):
        self.roots = []
        self.factory = PersonFactory()
        self.max_year = 2120

    def generate_tree(self):
        """
        Generates the family tree starting with two people born in 1950[cite: 22].
        Traverses generation by generation using a queue.
        """
        print("Reading files... [cite: 44]")
        print("Generating family tree... [cite: 45]")

        # Initialize the first two people born in 1950 using the standard probability logic [cite: 22, 32]
        # is_direct_descendant=False ensures they pull last names from last_names.csv based on rank probabilities 
        person1 = self.factory.get_person(1950, is_direct_descendant=False)
        person2 = self.factory.get_person(1950, is_direct_descendant=False)

        # Dynamically set the root last names based on what was generated for the original couple
        self.root_last_names = [person1.last_name, person2.last_name]
        
        # Link the root couple
        person1.set_partner(person2)
        person2.set_partner(person1)

        self.roots = [person1, person2]

        # Use a queue for Breadth-First Search (BFS) generation
        queue = [person1]
        processed_families = set()

        while queue:
            current_person = queue.pop(0)

            # Skip if we already processed this person (or their partner)
            if current_person in processed_families:
                continue

            # Mark this person and their existing partner as processed
            processed_families.add(current_person)
            if current_person.partner:
                processed_families.add(current_person.partner)

            # --- Check for Marriage (Assign a Partner) ---
            decade = self.factory.get_decade_str(current_person.year_born)
            marriage_rate = self.factory.bm_rates[decade]['marriage']
            
            # A person has a probability of having a spouse or partner as defined in the "marriage_rate" column 
            if not current_person.partner and random.random() < marriage_rate:
                partner = self.factory.get_partner(current_person)
                current_person.set_partner(partner)
                partner.set_partner(current_person)
                
                # Immediately mark the newly generated partner as processed
                processed_families.add(partner)

            # --- Calculate Children Logic ---
            # The number of potential children depends on the decade of the person's birth, +/- 1.5 children [cite: 32, 33]
            birth_rate = self.factory.bm_rates[decade]['birth']
            min_children = round(birth_rate - 1.5)
            max_children = round(birth_rate + 1.5)
            
            num_children = random.randint(min_children, max_children)

            # Determine the elder parent's birth year for child distribution [cite: 34]
            elder_year = current_person.year_born
            if current_person.partner:
                elder_year = min(current_person.year_born, current_person.partner.year_born)

            # Generate the calculated number of children, distributing their birth years evenly [cite: 34]
            for i in range(num_children):
                
                # The Year Born field for the children will be distributed evenly from the elder parent's Year Born + 25 years through parent's Year Born + 45 years [cite: 34, 35]
                if num_children == 1:
                    child_birth_year = elder_year + 35  # Place single child in the middle of the 25-45 span
                else:
                    # Distribute from elder_year + 25 through elder_year + 45
                    step = 20 / (num_children - 1)
                    child_birth_year = elder_year + 25 + int(round(i * step))

                # Stop generation branch if the child's birth year exceeds the 2120 limit [cite: 22]
                if child_birth_year <= self.max_year:
                    child = self.factory.get_person(
                        child_birth_year, 
                        is_direct_descendant=True, 
                        root_last_names=self.root_last_names
                    )
                    
                    # Add child to the current person
                    current_person.add_child(child)
                    
                    # Add child to the partner as well, if they exist
                    if current_person.partner:
                        current_person.partner.add_child(child)

                    # Only add the child to the queue to continue the generation tree
                    queue.append(child)

    def get_all_people(self):
        """
        Traverses the tree starting from the roots to collect all unique individuals.
        """
        visited = set()
        queue = list(self.roots)
        people = []

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            
            visited.add(curr)
            people.append(curr)

            # Add partner to queue if not visited
            if curr.partner and curr.partner not in visited:
                queue.append(curr.partner)

            # Add children to queue
            for child in curr.children:
                if child not in visited:
                    queue.append(child)
                    
        return people

    def get_duplicates(self):
        name_counts = defaultdict(int)
        for p in self.get_all_people():
            name_counts[p.get_full_name()] += 1
        return [name for name, count in name_counts.items() if count > 1]

    def interact(self):
        while True:
            print("\nAre you interested in:")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("(S)earch for a person by name") 
            print("(Q)uit")

            choice = input("> ").strip().upper()
            all_people = self.get_all_people()

            if choice == 'T':
                print(f"The tree contains {len(all_people)} people total.")
            elif choice == 'D':
                decades = defaultdict(int)
                for p in all_people:
                    decade = (p.year_born // 10) * 10
                    decades[decade] += 1
                for decade in sorted(decades.keys()):
                    print(f"{decade}s: {decades[decade]}")
            elif choice == 'N':
                duplicates = self.get_duplicates()
                print(f"There are {len(duplicates)} duplicate names in the tree:")
                for name in duplicates:
                    print(f"* {name}")
            elif choice == 'S':
                search_name = input("Enter the full name to search for: ").strip().lower()
                results = [p for p in all_people if p.get_full_name().lower() == search_name]
                if results:
                    print(f"Found {len(results)} match(es):")
                    for p in results:
                        print(f"- {p}")
                else:
                    print("No matches found.")
            elif choice == 'Q':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tree = FamilyTree()
    tree.generate_tree()
    tree.interact()