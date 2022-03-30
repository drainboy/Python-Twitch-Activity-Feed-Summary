from bs4 import BeautifulSoup
import re
import datetime

TWITCH_NAME = input("Enter Twitch channel name: ")

def main():
    filename = f"{TWITCH_NAME} _ Activity Feed - Twitch.html"
    tag = "div"
    tag_class = "ScTransitionBase-sc-eg1bd7-0 jddxRW tw-transition"
    website = f"https://www.twitch.tv/popout/moderator/{TWITCH_NAME}/activity-feed"

    print("Do download html of site to get updated list")
    print(website)
    soup = get_soup(filename)
    tags = get_tag(soup, tag, tag_class)
    followers = get_followers(tags)
    write_to_file(convert_to_text_list(followers), "followers.txt")


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
        result = re.search(f"(.*)(?: • )?Followed {TWITCH_NAME} • (.*)",tag.get_text())
        if result:
            name = result.group(1)
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
