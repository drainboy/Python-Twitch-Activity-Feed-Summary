from bs4 import BeautifulSoup
import re
import datetime
import argparse

TWITCH_NAME = ""

def main():
    args = arg_parser()
    TWITCH_NAME = args.twitch_user

    if not TWITCH_NAME:
        TWITCH_NAME = input("Enter Twitch channel name: ")

    filename = f"{TWITCH_NAME} | Activity Feed - Twitch.html" #need to use glob to find file
    tag = "div"
    tag_class = "tw-transition"
    website = f"https://www.twitch.tv/popout/moderator/{TWITCH_NAME}/activity-feed"

    print("Do download html of site to get updated list")
    print(website)
    soup = get_soup(filename)
    tags = get_tag(soup, tag, tag_class)
    followers = get_followers(tags)
    write_to_file(convert_to_text_list(followers), "followers.txt")


def arg_parser():
    parser = argparse.ArgumentParser(description="Twitch Activity Feed HTML converter.")
    parser.add_argument("twitch_user", nargs="?")
    args = parser.parse_args()
    return args

def convert_to_text_list(dictionary):
    output = []
    for key, value in dictionary.items():
        formatted_date = value.strftime("\n%d %b %Y")
        if formatted_date not in output:
            output.append(formatted_date)
            output.append(key)
        else:
            output.append(key)
    return output


def get_soup(filename):
    file = open(filename)
    soup = BeautifulSoup(file, "html.parser")
    return soup


def get_tag(soup, tag, tag_class):
    tags = soup.find_all(tag, class_= tag_class)
    if not tags:
        raise Exception(f"No '{tag}' found in given ")
    return tags


def get_followers(tags):
    usernames = {}
    for tag in tags:
        # Debug code to find out what the tag has
        # print(tag.get_text())
        result = re.search(f"(.*)Followed .* • (.*)",tag.get_text())
        if not result:
            result = re.search(f"(.*Raided).* • (.*)", tag.get_text())
        # print(result)
        if result:
            name = result.group(1)
            if "raided" in name.lower():
                name = name[:-6] + "*"
            date = get_date(result.group(2))
            usernames[name] = date
    return usernames


def get_date(text):
    output = datetime.datetime.now()
    if "yesterday" in text.lower():
        output -= datetime.timedelta(days=1)
    elif "ago" in text.lower():
        since, timing, ago = text.split()
        since = int(since)
        if "day" in timing:
            output -= datetime.timedelta(days=since)
        elif "hour" in timing:
            output -= datetime.timedelta(hours=since)
    return output


def write_to_file(a_list, filename):
    file_content = "\n".join(a_list)
    with open(filename,"w") as file:
        print(str(file_content))
        file.write(str(file_content))


if __name__ == "__main__":
    main()
