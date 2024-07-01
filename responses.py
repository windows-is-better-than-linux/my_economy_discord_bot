def handle_response(user_message):
   if user_message.lower() == "add_me":
       return "add_me"
   elif user_message.lower() == "help":
       return "help_me"
   elif user_message.lower() == "beg":
       return "beg"
