import win32com.client as win32
#import pythoncom
#xl=win32.Dispatch("outlook.application")
# print(xl)
import pythoncom

#pythoncom.CoInitialize()
signature = "Regards"

def build_basic_email(subject, to_list, cc_list):
    outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
    mail = outlook.CreateItem(0)
    mail.To = to_list
    mail.CC = cc_list
    mail.Subject = subject
    return mail

def send_email_done(to, cc, auto=False):
    """
    Sends an email for the 'Done' scenario (email_type = 1).
    """
    subject = "Address Update Completed"
    mail = build_basic_email(subject, to, cc)
    
    body = (
        "Dear Customer,\n\n"
        "We have received all the required details and the address is updated successfully.\n\n"
        f"{signature}"
    )
    
    mail.HtmlBody = body.replace('\n', '<br>')
    
    if auto:
        mail.Send()
        print("Email sent automatically.")
    else:
        mail.Display(True)
        print("Email opened in Outlook for manual review.")

def send_email_need_details(to, cc, missing_values, auto=False):
    """
    Sends an email for the 'Need Details' scenario (email_type = 2).
    `missing_values` should be a list of strings with the missing info.
    """
    subject = "Address Update - Missing Details"
    mail = build_basic_email(subject, to, cc)
    
    body = "Dear Customer,\n\nWe have found some missing values:\n"
    
    for value in missing_values:
        body += f"- {value}\n"

    body = body + "\nPlease provide the above information to update the address\n"
    
    body += f"\n{signature}"
    
    mail.HtmlBody = body.replace('\n', '<br>')
    
    if auto:
        mail.Send()
        print("Email sent automatically.")
    else:
        mail.Display(True)
        print("Email opened in Outlook for manual review.")

def send_exist_email(to, cc, auto=False):
    subject = "Address Details Already Exist"
    mail = build_basic_email(subject, to, cc)
    
    body = (
        "Dear Customer,\n\n"
        "The user details that you have shared with us already exist in our records\n\n"
        f"{signature}"
    )
    
    mail.HtmlBody = body.replace('\n', '<br>')
    
    if auto:
        mail.Send()
        print("Email sent automatically.")
    else:
        mail.Display(True)
        print("Email opened in Outlook for manual review.")    

def send_invalid_email(to, cc, auto=False):
    subject = "Invalid Details Provided"
    mail = build_basic_email(subject, to, cc)
    
    body = (
        "Dear Customer,\n\n"
        "The user details that you have shared with us are not matching with our existing records\n\n"
        f"{signature}"
    )
    
    mail.HtmlBody = body.replace('\n', '<br>')
    
    if auto:
        mail.Send()
        print("Email sent automatically.")
    else:
        mail.Display(True)
        print("Email opened in Outlook for manual review.") 

def email_type_dispatcher(email_type, to, cc, missing_values=None, auto=False):
    """
    Dispatches the correct email based on 'email_type'.
    
    email_type = 1: Done
    email_type = 2: Need Details
    """
    if email_type == 1:
        send_email_done(to, cc, auto)
    elif email_type == 2:
        if missing_values is None:
            missing_values = []
        send_email_need_details(to, cc, missing_values, auto)
    elif email_type == 3:
        send_exist_email(to, cc, auto)
    elif email_type == 4:
        send_invalid_email(to, cc, auto)
    else:
        print(f"Invalid email_type ({email_type}). Choose 1 or 2.")