# ===================================================
# Contact Tracker class responsible for the logical analysis
# ===================================================
import json
from member import Member


class ContactTracker:
    # class variable
    members = []

    def __init__(self, members, cases_with_contacts):
        # declare instance variable
        self.cases_with_contacts = dict()
        try:

            # The attribute members should be set only once for the entire class of ContactTracker
            if len(ContactTracker.members) == 0:
                ContactTracker.members = members

            # Check that all the sin numbers appearing in cases_with_contacts can be found in the registered community members list
            for key in cases_with_contacts:
                for valid_member in ContactTracker.members:
                    if key == valid_member.sin_number:
                        valid_member.is_sick = True
                        break

            # check true and false
            valid_sin_nums = []
            for member in ContactTracker.members:
                try:
                    if member.is_sick == False:
                        raise ValueError(
                            "A community member with sin number {} either doesn't exist or is not reported as sick.".format(member.sin_number))
                    else:
                        valid_sin_nums.append(member.sin_number)
                except ValueError as e:
                    print("Raise error here", e)

            for value in dict(cases_with_contacts):
                try:
                    if value not in valid_sin_nums:
                        cases_with_contacts.pop(value)
                        raise ValueError(
                            "A community member with sin number {} either doesn't exist or is not reported as sick.".format(value))
                except ValueError as e:
                    print("Raise error here", e)

            # initialize attribute cases_with_contacts
            self.deep_copy(cases_with_contacts)
            print(self.cases_with_contacts)

        except ValueError as e:
            print(e)

    # HELPER METHOD
    # the initializations of the attribute cases_with_contacts should be done by deep copying
    def deep_copy(self, dictionary):
        for key in dictionary:
            self.cases_with_contacts[key[:]] = dictionary[key][:]

    def get_contacts_by_sin_num(self, sin_number):
        # take a sin_number of a sick community member as an input
        # returns the list of Member objects that the sick member has been in contact with

        covid_contacts = []
        for key in self.cases_with_contacts:
            if key == sin_number:
                for position in self.cases_with_contacts[key]:
                    for member in ContactTracker.members:
                        if position == member.sin_number:
                            covid_contacts.append(member)
        return covid_contacts

    def get_all_contacts(self):

        # dictionary for return
        all_contacts = {}

        for key in self.cases_with_contacts:
            in_contact = self.get_contacts_by_sin_num(key)
            all_contacts[key] = in_contact

        return all_contacts

    def patient_zeros(self):
        patient_zero = []

        # all members who were in contact with someone who tested positive
        in_contact_id = []
        for values in self.cases_with_contacts.values():
            for sin_num in values:
                in_contact_id.append(sin_num)

        for key in ContactTracker.members:
            if key.sin_number not in in_contact_id:
                patient_zero.append(key)

        return patient_zero

    def potential_sick_members(self):
        potential_sick = []

        # all members who were in contact with someone who tested positive
        in_contact_id = []
        for value in self.cases_with_contacts.values():
            for sin_num in value:
                in_contact_id.append(sin_num)

        for member in ContactTracker.members:
            if member.is_sick == False:
                if member not in in_contact_id:
                    potential_sick.append(member)

        return potential_sick

    def sick_from_another_member(self):
        sick_member = []

        # all members who were in contact with someone who tested positive
        in_contact_id = []
        for values in self.cases_with_contacts.values():
            for sin_num in values:
                in_contact_id.append(sin_num)

        for member in ContactTracker.members:
            if member.is_sick == True:
                if member.sin_number in in_contact_id:
                    sick_member.append(member)

        return sick_member

    def most_viral_members(self):
        most_viral = []

        count = 0
        highest_count_id = []
        for key in self.cases_with_contacts:
            for value in self.cases_with_contacts.values():
                current_count = len(value)
                if current_count > count:
                    count = current_count
                    highest_count_id.append(key)

        for member in ContactTracker.members:
            if member.sin_number in highest_count_id:
                most_viral.append(member)

        return most_viral

    def most_contacted_member(self):
        most_contacted = []

        count_tracker = []
        for member in ContactTracker.members:
            if member.is_sick == False:
                for value in self.cases_with_contacts.values():
                    if member.sin_number in value:
                        count_tracker.append(member)

        return max(set(count_tracker), key=count_tracker.count)

    def ultra_spreaders(self):
        ultra_spreader = []

        potentially_sick = self.potential_sick_members()

        potential_sick_sin = []
        for i in potentially_sick:
            potential_sick_sin.append(i.sin_number)

        key_list = list(self.cases_with_contacts.keys())
        values_list = list(self.cases_with_contacts.values())

        for value in values_list:

            # remember the key we are at
            key_id_position = values_list.index(value)
            key = key_list[key_id_position]

            # check = any(item in value for item in potential_sick_id)
            if all(y in (potential_sick_sin) for y in value):
                for member in ContactTracker.members:
                    if member.sin_number == key:
                        ultra_spreader.append(member)

        return ultra_spreader

    def non_spreaders(self):

        non_spreader = []
        sick_member = []
        for member in ContactTracker.members:
            if member.is_sick == True:
                sick_member.append(member.sin_number)

        key_list = list(self.cases_with_contacts.keys())
        values_list = list(self.cases_with_contacts.values())

        for value in values_list:
            # print("my value is", value)

            # remember the key we are at
            key_id_position = values_list.index(value)
            key = key_list[key_id_position]

            if all(y in (sick_member) for y in value):
                for member in ContactTracker.members:
                    if member.sin_number == key:
                        non_spreader.append(member)

        return non_spreader

    def min_distance_from_patient_zeros(self, sin_number):

        min_distance = 0

        zero_patients = self.patient_zeros()

        valid_member = False
        my_member = None

        for member in self.members:
            if member.sin_number == sin_number:
                valid_member = True
                my_member = member
                break

        if valid_member is False:
            raise ValueError("The sin number {} is not a valid sin number".format(sin_number))

        if my_member in zero_patients:
            return min_distance

        while my_member not in zero_patients:
            contact_values = []
            for member in zero_patients:
                if member.sin_number in self.get_all_contacts():
                    member_contacts = self.get_contacts_by_sin_num(member.sin_number)

                    for contact in member_contacts:
                        contact_values.append(contact)

            # print("These are all the contacts collected: ", contact_values)
            zero_patients = contact_values
            # print(zero_patients)
            min_distance += 1
            # print("DISTANCE", min_distance)

        return min_distance

    def all_min_distances_from_patient_zeros(self):
        all_min_distances = {}

        for member in self.members:
            min_distance = self.min_distance_from_patient_zeros(member.sin_number)
            # print("MIN DISTANCE: ", min_distance)
            all_min_distances[member.sin_number] = min_distance

        return all_min_distances

'''
def main():
    members_list_dict = [{"sin": "470550179", "name": "Bob"},
                         {"sin": "417254688", "name": "Paul"},
                         {"sin": "431911105", "name": "Mark"},
                         {"sin": "427843841", "name": "Carol"},
                         {"sin": "419072662", "name": "Leanne"},
                         {"sin": "425613369", "name": "Will"},
                         {"sin": "468117575", "name": "Farley"},
                         {"sin": "422246158", "name": "Sarai"},
                         {"sin": "464591165", "name": "Larry"},
                         {"sin": "444029897", "name": "Philip"},
                         {"sin": "461509250", "name": "Zach"}]

    members_list = []
    for d in members_list_dict:
        sin = ''
        name = ''
        for k, v in d.items():
            if k == 'sin':
                sin = d[k]
            if k == 'name':
                name = d[k]
        new_member = Member(sin, name, False)
        members_list.append(new_member)

    cases_dict = {'470550179': ['417254688', '431911105', '427843841', '419072662', '425613369'],
                  '427843841': ['431911105', '419072662'],
                  '468117575': ['417254688'],
                  '419072662': ['422246158'],
                  '464591165': ['427843841', '431911105', '419072662', '425613369'],
                  '431911105': ['444029897', '461509250'],
                  '417254688': ['461509250'],
                  '425613369': ['419072662', '431911105'],
                  '461509250': ['444029897'],
                  '260970945': ['260212160']}  # TEST CASE FOR INVALID SICK COMMUNITY MEMBER

    contact_tracker = ContactTracker(members_list, cases_dict)
    print()

    print(contact_tracker.cases_with_contacts)
    print(ContactTracker.members)

    print("part 2")
    members_list2 = contact_tracker.get_contacts_by_sin_num('260996175')
    print(members_list2)

    print("part 3")
    print(contact_tracker.get_all_contacts())

    print()
    print("part 4")
    print(contact_tracker.patient_zeros())

    print()
    print("part 5")
    print(contact_tracker.potential_sick_members())

    print()
    print("part 6")
    print(contact_tracker.sick_from_another_member())

    print()
    print("part 7")
    print(contact_tracker.most_viral_members())

    print()
    print("part 8")
    print(contact_tracker.most_contacted_member())

    print()
    print("part 9")
    print(contact_tracker.ultra_spreaders())

    print()
    print("part 10")
    print(contact_tracker.non_spreaders())

    print("bonus part 1")
    print(contact_tracker.min_distance_from_patient_zeros('461509250'))

    print()
    print("bonus part 2")
    print(contact_tracker.all_min_distances_from_patient_zeros())


main()
'''
