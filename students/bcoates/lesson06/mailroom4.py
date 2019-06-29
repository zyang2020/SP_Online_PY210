#!/usr/bin/env python3

# Starting list of donors and their donation amounts
donor_history = {
    "donor_1": {"name": "Lana Kane", "donations": [2999.99]},
    "donor_2": {"name": "Cheryl Tunt", "donations": [150.20, 98192.10]},
    "donor_3": {"name": "Cyril Figgis", "donations": [819.25, 998.62, 10.50]},
    "donor_4": {"name": "Pam Poovey", "donations": [74926.10, 2675.87, 3289.33]},
    "donor_5": {"name": "Ray Gillette", "donations": [3820.90]}
}

def main_menu(prompt, prompt_actions):
    """ Prompt a user to selection an action to take, 
    and call the appropriate function """

    # Build a prompt message based on prompt and actions
    prompt_message = prompt
    for item in prompt_actions:
        prompt_message += "\n" + item[0] + " - " + prompt_actions[item]['message']
    prompt_message += "\n> "
    
    # Prompt the user and set the selection
    while True:
        selection = input(prompt_message)
        if selection not in prompt_actions:
            print("Please select a valid number...")
        elif prompt_actions[selection]['action']() == 'quit':
            print("Quitting...")
            break

def prompt_for_donor():
    """ Prompt for a donor name, list if needed, add if not found """

    while True:
        # Prompt the user for the full name
        full_name = input("Please enter the full name of a donor (type 'list' for current donor names) > ")

        # If the name is 'list' print the full list of names
        if not full_name:
            print("Unable to proceed with input, please enter a donor name...")
        elif full_name.lower() == "list":
            for donor in donor_history:
                print(donor_history[donor]['name'])
        else:
            donor = add_donor(full_name)
            return donor

def add_donor(full_name):
    """ Prompt for a donor name, list if needed, add if not found """

    for donor in donor_history:
        if full_name == donor_history[donor]['name']:
            return donor
    else:
        new_donor_key = "donor_" + str(len(donor_history)+ 1)
        new_donor = {"name": full_name, "donations": []}
        donor_history[new_donor_key] = new_donor
        return new_donor_key

def prompt_for_donation_amount(donor):
    """ Prompt for a donation amount and add it for the donor """
    
    while True:
        # Prompt for the amount
        donation_amount = input("Please enter the donation amount > ")
        try:
            float_amount = float(donation_amount)
            zero_check = 1 / float_amount
            break
        except ValueError:
            print("Invalid donation amount, please try again...")
        except ZeroDivisionError:
            print("Donation amount can't be zero, please try again...")

    # Add the donation to the donor's list of donations
    add_donation_amount(donor, float_amount)
    return float_amount

def add_donation_amount(donor, float_amount):
    """ Add donation for donor """

    # Add the donation to the donor's list of donations
    donor_history[donor]['donations'].append(float_amount)
            
    # Return the donation amount
    return float_amount

def send_a_thank_you():
    """ Generate a thank you letter for a given donor and amount """

    # Prompt for donor's full name
    donor = prompt_for_donor()

    # Prompt for the donation amount
    donation_amount = prompt_for_donation_amount(donor)

    # Print out a letter customized for the donor and amount
    print(format_thank_you_letter(donor_history[donor]['name'], donation_amount))

def format_thank_you_letter(full_name, donation):
    """ Return a formatted thank you letter """

    letter = f"""
Dear {full_name},

Thank you for your generous donation of ${donation:.2f}!

Sincerely,

The Owners"""
    return(letter)

def create_a_report():
    """ Create a summary report of donors and their donations """

    # Summarize the values into a new list using comprehension
    donor_summary = [[donor_history[donor]['name'], 
                    sum(donor_history[donor]['donations']),
                    len(donor_history[donor]['donations']),
                    sum(donor_history[donor]['donations'])/len(donor_history[donor]['donations'])] for donor in donor_history]

    # Sort the new list descending by total donations and append to list
    donor_summary.sort(key=lambda x: x[1], reverse=True)
    report = []
    for donor in donor_summary:
        report.append(f"{donor[0]:<20} ${donor[1]:>13,.2f} {donor[2]:>11} {donor[3]:>13,.2f}")
    return report

def display_report():
    """ Display a summary report """

    # Print the header row
    header_row = "{0:<20} | {1} | {2} | {3}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
    print(header_row)
    print("-" * len(header_row))

    # Print the summary data
    report = create_a_report()
    for row in report:
        print(row)

def send_thank_you_to_all():
    """ Create letters for all donors for their latest donation and save to disk """

    # Loop through the donor history, create, and save letters
    for donor in donor_history:
        # Set some variables based on the donro information
        full_name = donor_history[donor]['name']
        last_donation = donor_history[donor]['donations'][-1]
        letter = format_thank_you_letter(full_name, last_donation)
        save_file(full_name, letter)

def save_file(full_name, letter):
    """ Save a donor letter to a temp file """

    # Define the temp directory and file name
    temp_dir = "/tmp/"
    file_name = temp_dir + full_name + ".txt"
        
    # Open a file named for the full_name and write the letter
    try:
        with open(file_name, "w") as f:
            f.write(letter)
            print("Saved letter for {} to {}".format(full_name, file_name))
            return file_name
    except IOError:
        print("Unable to save letter for {} to {}, please check the file path...".format(full_name, file_name))

# Define dictionary of menu prompt messages and actions
main_menu_prompt_actions = {
    "1": {"message": "Send a Thank You", "action": send_a_thank_you},
    "2": {"message": "Create a Report", "action": display_report},
    "3": {"message": "Send Thank You to All Donors", "action": send_thank_you_to_all},
    "4": {"message": "Quit", "action": quit}
}

# Define the main menu prompt
main_menu_prompt = """Please enter a number to select the action:"""

# Run the main program
if __name__ == '__main__':
    main_menu(main_menu_prompt, main_menu_prompt_actions)