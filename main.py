from session_menu import display_menu

from session_actions import (
    create_session,
    view_sessions,
    update_status,
    add_note,
    start_session,
    end_session,
)


def main():
    while True:
        display_menu()

        choice = input("Select an option: ")

        if choice == "1":
            create_session()

        elif choice == "2":
            view_sessions()

        elif choice == "3":
            update_status()

        elif choice == "4":
            add_note()

        elif choice == "5":
            start_session()

        elif choice == "6":
            end_session()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()