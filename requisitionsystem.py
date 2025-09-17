'''
This program is a requisition system that handles requests from staff in a software company.
Staff can submit purchase requests, which can be approved or disapproved by a manager/supervisor based on certain conditions.
'''


# We apply here the principles of KISS and clean code, by creating a globally available constant with the main menu's message.
# This would prevent the class's start method from being overloaded with a long string, making the the method easier to read.
# It also allows this message to potentially be reused in any other methods.
MENU_MESSAGE = f"""
-- WELCOME TO THE REQUISITION SYSTEM --

1. Add new requisition
2. Update requisition status
3. Display all reqisitions
4. Display requisition statistics
5. Exit

Select action: """


class RequisitionSystem:
    # The __init__ method applies the KISS principle by doing just one simple thing: creating an empty list of requisitions.
    # This list of requisitions would be used as a single 'source of truth' throughout the code, for whatever we need to do - 
    # whether it's a counter based on the number of requsitions, finding and updating requisitions, and so on.
    def __init__(self):
        self.requisitions = []
    

    # The staff_info method applies the KISS principle: it simply creates an empty dict of requisition data,
    # asking the user to input the staff's details and adds them to the dict.
    # It generates a requisition ID based on an automatic counter, which is based on the requisition list's length.
    # It then simply prints the inputted information and the generated requisition ID and returns the dict.
    def staff_info(self):
        info = {}
        counter = len(self.requisitions) + 1
        info["date"] = input("\nEnter date: ")
        info["staff_id"] = input("Enter staff ID: ")
        info["staff_name"] = input("Enter staff name: ")
        info["requisition_id"] = str(10000 + counter)

        print("\nPrinting Staff Information:")
        print(f"Date: {info["date"]}")
        print(f"Staff ID: {info["staff_id"]}")
        print(f"Staff name: {info["staff_name"]}")
        print(f"Requisition ID: {info["requisition_id"]}")

        return info
    

    # The requisitions_details method applies the KISS principle:
    # It simply calls the staff_info method to create a requsition dict, adds an empty list of items to the dict and creates a total price variable,
    # and then uses a simple while loop that prompts the user to add items to the list, validating each item's data and updating the total price.
    # In the end it simply prints the total price, adds it to the dict and returns the dict.
    def requisitions_details(self):
        requisition_data = self.staff_info()
        requisition_data["items"] = []
        total_price = 0

        while True:
            item_count = len(requisition_data["items"]) + 1
            item_name = input(f"\nEnter item #{item_count} name (or 'done' to finish): ")
            if item_name.lower() == "done":
                break
            try:
                item_price = float(input(f"Enter item #{item_count} price: "))
                requisition_data["items"].append({"name": item_name, "price": item_price})
                total_price += item_price
            except ValueError:
                print("Invalid item price - must be a number")
        
        print(f"Total price: ${round(total_price, 2)}")
        requisition_data["total"] = total_price
        
        return requisition_data
    

    # The requisition_approval method applies the KISS principle:
    # it simply calls the requisitions_details method to create a requsition dict, sets the requsition status according to its total price,
    # prints the status and the approval ref, and adds the new dict to the list of requisitions.
    def requisition_approval(self):
        requisition_data = self.requisitions_details()
        requisition_data["status"] = "Pending"

        if requisition_data["total"] < 500:
            requisition_data["status"] = "Approved"
            requisition_data["approval_ref"] = self.generate_approval_ref(requisition_data)

        print(f"\nTotal: ${round(requisition_data["total"], 2)}")
        print(f"Status: {requisition_data["status"]}")

        # This part of four lines could use an improvement in terms of the DRY principle.
        # The words "Approval Reference Number" are repeated twice in different possible strings. 
        # We could instead use one string with a dynamic condition or variable inside of it.
        # In addition, these same four lines of code are repeated in another method (display_requisitons),
        # so we could add a reusable method for this part instead of repeating it.
        if "approval_ref" in requisition_data and requisition_data["status"] == "Approved":
            print(f"Approval Reference Number: {requisition_data["approval_ref"]}")
        else:
            print(f"Approval Reference Number: not available")

        self.requisitions.append(requisition_data)
    

    # The reusable method generate_approval_ref applies the DRY (don't repeat yourself) principle.
    # There are multiple places in the code that need to generate an approval reference ID using the same formula (staff ID + last 3 digits of the requisition ID).
    # Instead of repeating this forumla several times in the code, it's put into a reusable method that can be called whenever an approval reference is needed.

    # It also applies the Single Responisibility principle: the only thing it does is generating an approval ref.
    # This means we only need to change this method if we want to change the formula for generating an approval ref.

    # The KISS principle is also applied: the method is made of just one line that returns a concatenated string using the dict's properties.
    def generate_approval_ref(self, requisition):
        return requisition["staff_id"] + requisition["requisition_id"][-3:]
    

    # The find_requisition_by_id method similarly applies the DRY principle, by providing a reusable function to find a requisition by its ID and return it.
    # It can be used whenever we need to search, display, update or delete a specific requisition throughout the code.
    
    # The KISS principle is also applied here: just loop through each requisition, and returns it if its ID matches the searched ID.
    # If it's done looping and no matching requsition has been found, return None.
    def find_requisition_by_id(self, requisition_id):
        for requisition in self.requisitions:
            if requisition["requisition_id"] == requisition_id:
                return requisition
        return None


    # The respond_requsition applies the KISS principle by following a very simple set of operations:
    # asking the user to enter a requisition ID, search for a matching requisition, asking the user to enter a new status,
    # check if the entered status is valid, and if so, updating the matching requisition's object accordingly.
    def respond_requsition(self):
        requisition_id = input("\nEnter requisition ID: ")
        requisition = self.find_requisition_by_id(requisition_id)
        if requisition is not None:
            new_status = input("Enter new status: ").title()
            if new_status != "Approved" and new_status != "Pending" and new_status != "Not Approved":
                print("Invalid status")
            else:
                requisition["status"] = new_status
                if new_status == "Approved":
                    requisition["approval_ref"] = self.generate_approval_ref(requisition)
                elif "approval_ref" in requisition:
                    del requisition["approval_ref"]
                print(f"Successfully updated status of requisition {requisition_id} to {new_status}")
        else:
            print("Requisition not found")
    

    # The display_requisitons method applies the KISS principle: it does a very basic looping through the list of requisitions,
    # and accesses the dict properties of each requisition item in order to print the requisition's details.

    # The Single Responsibility principle is also applied here, as its only responsibility is printing the list of requisitions.
    # The only reason we might have to change it is if we need to print more details for each requisitions, or change the overall
    # style and format of the list.
    def display_requisitons(self):
        print("\nPrinting requistions:")
        for requisition in self.requisitions:
            print(f"\nDate: {requisition["date"]}")
            print(f"Requisition ID: {requisition["requisition_id"]}")
            print(f"Staff ID: {requisition["staff_id"]}")
            print(f"Staff name: {requisition["staff_name"]}")
            print(f"Total: ${round(requisition["total"], 2)}")
            print(f"Status: {requisition["status"]}")
            if "approval_ref" in requisition and requisition["status"] == "Approved":
                print(f"Approval Reference Number: {requisition["approval_ref"]}")
            else:
                print(f"Approval Reference Number: not available")
    

    # The requisition_statistic method applies the KISS principle: it simply creates three filtered requisition lists for each
    # possible status, and then prints the length of each list, as well as the length of the overall requisition list.

    # It also applies the Single Responsibility principle: the only thing it does is print statistics, so the only reason we might
    # have to change it is if we need to change the style and format of this display, or adding more stats to it.
    def requisition_statistic(self):
        approved_requisitions = [item for item in self.requisitions if item["status"] == "Approved"]
        pending_requisitions = [item for item in self.requisitions if item["status"] == "Pending"]
        not_approved_requisitions = [item for item in self.requisitions if item["status"] == "Not Approved"]

        print("\nRequisition statistics:")
        print(f"The total number of requisitions submitted: {len(self.requisitions)}")
        print(f"The total number of approved requisitions: {len(approved_requisitions)}")
        print(f"The total number of pending requisitions: {len(pending_requisitions)}")
        print(f"The total number of not approved requisitions: {len(not_approved_requisitions)}")
    

    # The start method (which operates the application's main menu) applies the KISS principle:
    # it simply asks the user for their choice, and then uses basic if-elif-else conditions to perform the right action
    # based on the user's choice, or print an error message if the choice is invalid.
    def start(self):
        while True:
            selection = input(MENU_MESSAGE)
            if selection == "1":
                self.requisition_approval()
            elif selection == "2":
                self.respond_requsition()
            elif selection == "3":
                self.display_requisitons()
            elif selection == "4":
                self.requisition_statistic()
            elif selection == "5":
                break
            else:
                print("Invalid selection")


# This part applies the KISS principle by simply creating an instance of the RequisitionSystem class,
# and then just calling the instance's start() method in order to run the system.
requisition_system = RequisitionSystem()
requisition_system.start()