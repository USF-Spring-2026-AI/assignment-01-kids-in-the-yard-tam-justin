class Person:

    def __init__(
            self,
            year_born,
            year_died,
            first_name,
            last_name,
            direct_descendant,
            partner=None,
            parent=None,
            children=None):
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.partner = partner
        self.parent = parent
        self.children = children
        self.direct_descendant = direct_descendant

    # return the year this person was born
    def get_year_born(self):
        return self.year_born

    # set the year this person was born
    def set_year_born(self, new_year):
        self.year_born = new_year

    # return the year this person died
    def get_year_died(self):
        return self.year_died

    # set the year this person died
    def set_year_died(self, new_year):
        self.year_died = new_year

    # return this person's first name
    def get_first_name(self):
        return self.first_name

    # set this person's first name
    def set_first_name(self, name):
        self.first_name = name

    # return this person's last name
    def get_last_name(self):
        return self.last_name

    # set this person's last name
    def set_last_name(self, name):
        self.last_name = name

    # return this person's partner (object)
    def get_partner(self):
        return self.partner

    # set this person's partner
    def set_partner(self, partner):
        self.partner = partner

    # return an array containing this person's children
    def get_children(self):
        return self.children

    # set this person's children
    def set_children(self, children):
        self.children = children

    # return this person's parent
    def get_parent(self):
        return self.parent

    # set this person's parent
    def set_parent(self, parent):
        self.parent = parent

    # set this person's direct descendant status
    def set_is_direct_descendant(self, bool):
        self.direct_descendant = bool

    # return if this person is a direct descendant
    def is_direct_descendant(self):
        return self.direct_descendant
