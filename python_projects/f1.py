# A simple Python program to print a greeting message

def greet(name):
    return f"Hello, {name}! Welcome to Python programming."

if __name__ == "__main__":
    user_name = input("Enter your name: ")
    print(greet(user_name))