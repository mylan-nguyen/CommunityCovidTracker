import os
import json
from member import Member
from contactTracker import ContactTracker


def load_file(file_name):
    #check if file is present
    if os.path.isfile(file_name):
        #open text file in read mode
        text_file = open(file_name, "r")

        #read whole file to a string
        data = text_file.read()

        #close file
        text_file.close()

    return data


def JSON_to_members(json_file):
    json_object = json.loads(json_file)
    members = []

    for js in json_object:
        member = Member.from_JSON(js)
        members.append(member)

    return members


def csv_to_dictionary(csv_file):
    csv_dict = {}

    lines = csv_file.split("\n")

    my_values = []
    for line in lines:
        new_line = line.replace(" ", "")
        elem = new_line.split(",")
        #print(elem)
        #print("my key: ", elem[0])
        my_key = elem[0]
        new_elems = elem.remove(my_key)
        csv_dict[my_key] = elem

    return csv_dict

def build_report(contact_tracker):

    report = ""

    report = report + "Contact Records:" + "\n"
    cases_record = contact_tracker.cases_with_contacts
    #report = report + str(contact_tracker.get_all_contacts())

    for member in contact_tracker.members:
        if member.is_sick:
            tmp = str(contact_tracker.get_contacts_by_sin_num(member.sin_number))
            line = str(member) + " had contact with " + tmp.replace('[', '').replace(']', '')
            report += "    " + line + "\n"

    patient_zeros = contact_tracker.patient_zeros()
    report += "\n" + "Patient Zero(s): " + str(patient_zeros).replace('[', '').replace(']', '')

    potentially_sick = contact_tracker.potential_sick_members()
    report += "\n" + "Potential sick members: " + str(potentially_sick).replace('[', '').replace(']', '')

    sick_contact = contact_tracker.sick_from_another_member()
    report += "\n" + "Sick members who got infected from another member: " + str(sick_contact).replace('[', '').replace(']', '')

    most_viral = contact_tracker.most_viral_members()
    report += "\n" + "Most viral members: " + str(most_viral).replace('[', '').replace(']', '')

    most_contact = contact_tracker.most_contacted_member()
    report += "\n" + "Most contacted members: " + str(most_contact).replace('[', '').replace(']', '')

    ultra_spreader = contact_tracker.ultra_spreaders()
    report += "\n" + "Ultra spreaders: " + str(ultra_spreader).replace('[', '').replace(']', '')

    non_spreaders = contact_tracker.non_spreaders()
    report += "\n" + "Non-spreaders: " + str(non_spreaders).replace('[', '').replace(']', '')

    report += "\n\n" + "For bonus:\n" +"Minimum distances of members from patient zeros:\n"


    all_min = contact_tracker.all_min_distances_from_patient_zeros()
    #print(all_min)

    for member in contact_tracker.members:
        for min in all_min:
            #print(min)
            if member.sin_number == min:
                min_distance = "    " + str(member) + ": " + str(all_min[min]) + "\n"
                report += min_distance


    return report

def write_in_file(file_name, text):
    my_file = open(file_name, "w")

    try:
        my_file.write(text)
    except:
        print("there was a problem writing to file with name " + file_name)

    finally:
        my_file.close()


def main():
    try:
        myFile = load_file("cases.csv")
        # print(myFile)

        data = load_file("communitymembers.json")
        members = JSON_to_members(data)
        cases = csv_to_dictionary(myFile)
        #print(csv_to_dictionary(myFile))

        FLAG = True
    except:
        FLAG = False
        print("Sorry, the file " + myFile + " could not be found.")

    if FLAG == True:
        contact_tracker = ContactTracker(members, cases)
        report = build_report(contact_tracker)
        write_in_file("contact_tracing_report.txt", report)


main()
