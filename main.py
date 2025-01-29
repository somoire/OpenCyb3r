import sys
import subprocess

def show_menu():
    print("\nWelcome to OpenCyb3r")
    print("=====================")
    print("1. Example Tool (Coming Soon)")
    print("2. Run Bandit Security Scan)")
    print("3. Exit")
    return input("Choose an option: ")

def example_tool():
    print("\nExample Tool: Replace this with your tool's functionality.")
    input("Press Enter to return to the menu.")

def run_bandit_scan():
    print("\nRunning Bandit Security Scan...\n")
    try:
        # Run Bandit on the current directory and capture output
        result = subprocess.run(["bandit", "-r", "."], text=True, capture_output=True)

        # Display the output of the scan
        print(result.stdout)
        
        # Handle errors if Bandit is not installed or fails
        if result.returncode != 0:
            print("\nBandit encountered an issue. Ensure it is installed by running: pip install bandit")
        
    except FileNotFoundError:
        print("\nBandit is not installed. Please install it using: pip install bandit")

    input("\nPress Enter to return to the menu.")
    
def main():
    while True:
        choice = show_menu()
        if choice == "1":
            example_tool()
        elif choice == "2":
            run_bandit_scan()  # Calls Bandit when option 2 is selected
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
