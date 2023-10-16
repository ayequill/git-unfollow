#!/usr/bin/env python3


if __name__ == "__main__":
    from sys import argv
    from os import path
    from datetime import datetime as date
    from store import make_req, load_data

    if len(argv) < 2 or len(argv) > 2:
        print("Usage: ./unfollow.py <username>")
        exit(1)

    file_path = 'temp.json'
    username = argv[1]
    if path.exists(file_path):
        old_data = load_data(file_path)
        data = load_data(file_path)
    else:
        make_req(username)
        data = load_data(file_path)

    while True:
        try:
            print('=' * len("Specify a command to run by entering a number:"))
            print("Specify a command to run by entering a number:")
            print('=' * len("Specify a command to run by entering a number:"))
            print(f"Last login: {data.get('time_stamp',date.now())}")
            print(f"Followers: {data.get('followers_count')}")
            print(f"Following: {data.get('following_count')}")
            print("\t1. Check who doesnt follow you back")
            print("\t2. Who unfollowed recently?")
            print("\t3. Old data? Reload Data")
            usr_input = input("Enter a command or type 'quit' to close program.\n>>> ")
            if usr_input == 'quit' or usr_input == '0':
                exit(0)
            command = int(usr_input)
            if command == 1:
                if data:
                    dont_follow = data.get('dont_follow_back')
                    print('\n')
                    for user in dont_follow:
                        if user == dont_follow[-1]:
                            print(user)
                            break
                        print(user, end=', ')
                    print('\n')
            if command == 2:
                recently_unfollowed = list(filter(lambda x: x not in data.get('followers'),
                                                  old_data.get('followers', [])))
                # A bug if array is empty
                if recently_unfollowed:
                    print('\n')
                    for user in recently_unfollowed:
                        if user == recently_unfollowed[-1]:
                            print(user)
                            break
                        print(user, end=', ')
                    print('\n')
                else:
                    print("No one unfollowed recently.")
                    print('\n')
            if command == 3:
                make_req(username)
        except Exception as e:
            print(e)
            exit(1)
