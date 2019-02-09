import urllib.request

VERSION_FILE = "https://raw.githubusercontent.com/JPatrickDev/PyHud-Public/master/VERSION"


def compare_version(my_version, latest_version):
    my_version_split = my_version.split(".")
    latest_version_split = latest_version.split(".")
    if my_version_split.__len__() < latest_version_split.__len__():
        for i in range(my_version_split.__len__(), latest_version_split.__len__()):
            my_version_split.append("0")
    else:
        for i in range(latest_version_split.__len__(), my_version_split.__len__()):
            latest_version_split.append("0")
    for i in range(0, my_version_split.__len__()):
        my_version_value = int(my_version_split[i])
        latest_version_value = int(latest_version_split[i])
        if latest_version_value > my_version_value:
            return True
        elif latest_version_value < my_version_value:
            return False
    return False


def check_for_update():
    latest_version = urllib.request.urlopen(VERSION_FILE).read()
    latest_version = latest_version.decode("utf8")
    my_version = open("../../VERSION").read()
    return compare_version(my_version, latest_version)


print(check_for_update())