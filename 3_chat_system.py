class Message:
    def __init__(
            self,
            role:str,
            content:str
        ):
            self.role = role
            self.content = content

class ChatSession:
        def __init__(
                self,
                username:str
            ):
                self.username = username
                self.messages=[]
        
        def add_message(self, role:str, content:str):
               message = Message(role,content)
               self.messages.append(message)

        def show_messages(self):
               for message in self.messages:
                      print(f"{message.role} - {message.content}")

        def count_messages(self):
               count = 0
               for msg in self.messages:
                      if msg.role=="user":
                             count+= 1
               return count


chat = ChatSession("Mateen")
chat.add_message("user","Salam");
chat.add_message("assistant","Wslam")
chat.add_message("user","Coding ma chicha ki bosa?")

chat.show_messages()

print("\nTotal user messages")
print(chat.count_messages())