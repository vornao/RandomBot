import const
import logging
import csv

USER_NOT_VALID = "You are not allowed to access this bot's contents."
USER_NOT_VALID_LOG = "Not allowed user tried to access bot! (User: %s, id: %d)"

logging.basicConfig(
    filename="b0t.log", 
    filemode="a", 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level = logging.INFO)

""" check if user id is allowed to use this bot """
def check_username(username: str, userlist) -> bool:
    if username in userlist:
        return True
    else:
        return False

def load_file_to_list(filename, l):
    try: 
        f = open(filename, "r")
        temp_list = f.read().splitlines()
        for x in temp_list:
            l.append(x)
    except:
        logging.error("error opeining %s", filename)
    finally:
        f.close()

def append_to_file(filename, line):
    with open(filename, "a") as sf:
        sf.write("\n")
        sf.write(line)

def append_to_csv(filename, x, y):
    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerow([x,y])

def parse_csv(filename, d: dict):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for rows in reader:
            d[rows[0]] = rows[1]
