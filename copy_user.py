import shutil
import os
import platform

def get_existing_users():
    # Fetch a list of existing local users
    if platform.system() == "Windows":
        # Filter out built-in Windows users
        users = [d.name for d in os.scandir('C:\\Users') if d.is_dir() and not d.name.lower().startswith('user')]
    elif platform.system() == "Linux":
        users = [d.name for d in os.scandir('/home') if d.is_dir()]
    else:
        # Add support for other platforms if needed
        raise NotImplementedError("Platform not supported")

    return users

def list_existing_users():
    users = get_existing_users()
    if users:
        print("Existing local users:")
        for user in users:
            print(user)
    else:
        print("No local users found.")

def get_home_directory(username):
    # Get the home directory for a given username
    if platform.system() == "Windows":
        return f'C:\\Users\\{username}'
    elif platform.system() == "Linux":
        return f'/home/{username}'
    else:
        # Add support for other platforms if needed
        raise NotImplementedError("Platform not supported")

def check_user_exists(username):
    return username in get_existing_users()

def transfer_folders():
    list_existing_users()

    # Prompt the user for source username
    source_user = input("Enter the source user name: ")
    while not check_user_exists(source_user):
        print(f"User '{source_user}' does not exist. Please enter a valid source user name.")
        source_user = input("Enter the source user name: ")

    # Prompt the user for destination username
    destination_user = input("Enter the destination user name: ")
    while not check_user_exists(destination_user):
        print(f"User '{destination_user}' does not exist. Please enter a valid destination user name.")
        destination_user = input("Enter the destination user name: ")

    # Replace these values with the actual folders you want to transfer
    folders_to_transfer = ['Desktop', 'Downloads' , 'Documents', 'OpenVPN' , 'Pictures', 'Google']

    for folder in folders_to_transfer:
        source_path = os.path.join(get_home_directory(source_user), folder)
        destination_path = os.path.join(get_home_directory(destination_user), folder)

        # Check if the source folder exists
        if os.path.exists(source_path):
            try:
                # If the destination folder exists, combine them without duplicating files
                if os.path.exists(destination_path):
                    for item in os.listdir(source_path):
                        source_item = os.path.join(source_path, item)
                        destination_item = os.path.join(destination_path, item)

                        if os.path.isdir(source_item):
                            # If it's a directory, recursively copy it
                            shutil.copytree(source_item, destination_item, symlinks=True, ignore=None, copy_function=shutil.copy2)
                        else:
                            # If it's a file, copy it if it doesn't exist in the destination
                            if not os.path.exists(destination_item):
                                shutil.copy2(source_item, destination_item)

                    print(f"Folders '{source_path}' and '{destination_path}' combined successfully.")
                else:
                    # If the destination folder doesn't exist, simply copy the source folder
                    shutil.copytree(source_path, destination_path, symlinks=True, ignore=None, copy_function=shutil.copy2)
                    print(f"Folder '{folder}' transferred successfully.")
            except Exception as e:
                print(f"Error transferring folder '{folder}': {e}")
        else:
            print(f"Source folder '{folder}' does not exist.")

if __name__ == "__main__":
    transfer_folders()
