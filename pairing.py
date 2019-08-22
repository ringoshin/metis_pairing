#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:32:52 2019

@author: ringoshin
"""

import sys
from datetime import datetime
import re
from bs4 import BeautifulSoup

#--------------------------------------------------------------------------#
# Things to do before you can use this app:                                #
#    1. Update 'who_am_i' to your own name                                 #
#    2. Update 'readme_md_doc' to where your copy is                       #
#    3. If 'Pairing_list_everyday.txt' is not in same folder as this app,  #
#       update 'Pairing_List' to include full path to the file             #
#--------------------------------------------------------------------------#

# Update who_am_i to your own name as listed in Slack's Pairing List
who_am_i = 'Fan Yeng Loon'

# Update readme_md_loc to where your local SGP19_DSO's readme.md is located
readme_md_loc = '/home/ringoshin/Projects/z - learning/0 - Kaplan/SGP19_DS0/readme.md'

# Location of local copy of 'Pairing_list_everyday.txt' from Slack channel
Pairing_List = 'Pairing_list_everyday.txt'


# First and last day of our Metis/Kaplan bootcamp
first_day = datetime.strptime('8 Jul 2019', '%d %b %Y')   # W1D1
last_day = datetime.strptime('27 Sep 2019', '%d %b %Y')   # W12D5



def Str_to_TupleList(pair_names_str):
    """ Convert list of paired names into list of tuples
    """
    pattern = r"\'([a-zA-Z ]+)\'"
    temp_list_iter = iter(re.findall(pattern, pair_names_str))
    return [(name, next(temp_list_iter)) for name in temp_list_iter]


def Load_Pairing_List(fileName):
    """ Load local copy of daily pairing list from Slack
    """
    with open(fileName) as f:
        content = f.readlines()
    content_iter = iter(content)
    return {key.strip(' \n') : Str_to_TupleList(next(content_iter).strip(' \n')) \
                    for key in content_iter}
    
    
def Get_Week_and_Day_Number(check_date):
    """ Find out which week and day number where W1D1 repsents 1st week and day
    Returns week number and day number
    """
    global first_day, last_day
    if check_date < first_day or check_date > last_day:
        raise ValueError('Date is not within course schedule.')
        
    days_diff = check_date - first_day
    week_num = days_diff.days // 7 + 1
    day_num = days_diff.days % 7 + 1
    return week_num, day_num


def Get_Task_per_Date(wnum, dnum):
    """ Locate pair assignment for Week <wnum> Day <dnum> from local Git
    copy of https://github.com/thisismetis/SGP19_DS0/blob/master/readme.md
    """
    #url = 'https://github.com/thisismetis/SGP19_DS0/blob/master/readme.md'
    global readme_md_loc   # Location of local readme.md, defined at top of app
    #response = requests.get(url)
    #print(response.status_code)

    #page = response.text
    page = open(readme_md_loc)
    soup = BeautifulSoup(page.read(), 'lxml')

    table_rows = soup.find_all('tr')
    if wnum < len(table_rows):
        table_cells = table_rows[wnum].find_all('td')
        if dnum <= len(table_cells):
            if 'pairs' in table_cells[dnum-1].find('a')['href']:
                pair_text = table_cells[dnum-1].find('a').text
                return True, pair_text.replace('•','').replace("Pair:",'').strip()
    return False, None


def Get_Paired_and_Dummy(week, day, pairing_list):
    """ Find out who is pairing with <who_am_i> from <pairing list> on this day:
        W<week> D<day>
        Also find out who is the assigned dummy
    """
    global who_am_i
    
    weekday = 'W{}D{}'.format(week,day)
    week_day_pairs = pairing_list[weekday]
    dummy=''

    # Locate the dummy
    for name1, name2 in week_day_pairs:
        if name2=='dummy':
            dummy = name1
            break
        elif name1=='dummy':
            dummy = name2
            break
    
    if dummy==who_am_i:
        return who_am_i, dummy
    
    for name1, name2 in week_day_pairs:
        if name1==who_am_i:
            return name2, dummy
        elif name2==who_am_i:
            return name1, dummy
        
    print()
    raise ValueError(f'{who_am_i} cannot be found!')


def main(argv=None):
    global who_am_i, Pairing_List
    
    if len(argv)>1:
        #print(argv)
        who_am_i = ' '.join(argv[1:])
        
    weeknum, daynum = Get_Week_and_Day_Number(datetime.today())
    pairing_list = Load_Pairing_List(Pairing_List)
    
    if daynum <= 5:
        found, assignment = Get_Task_per_Date(weeknum, daynum)
        if not found:
            print("No pair assignment found for W%dD%d." %(weeknum, daynum))
            print("Please ensure local Git copy has been updated.")
            print()
        else:            
            paired_assignee, dummy = Get_Paired_and_Dummy(weeknum, daynum, pairing_list)
            print("The agony for today (W%dD%d) is %s." %(weeknum, daynum, assignment))
            if dummy==who_am_i:
                print("Oops, you are the dummy!")
            else:
                print("You are sharing your pain with %s. Sadly, nobody wants %s." %(paired_assignee, dummy))
            print()
   
    if not (weeknum==12 and daynum==5):
        daynum += 1
        if daynum > 5:
            weeknum += 1
            daynum = 1
        found, assignment = Get_Task_per_Date(weeknum, daynum)
        if not found:
            print("No pair assignment found for W%dD%d." %(weeknum, daynum))
            print("Please ensure local Git copy has been updated.")
        else:
            paired_assignee, dummy = Get_Paired_and_Dummy(weeknum, daynum, pairing_list)
            print("The next agony on W%dD%d will be %s." %(weeknum, daynum, assignment))
            if dummy==who_am_i:
                print("You are the next dummy!")
            else:
                print("You are destined to suffer with %s. %s is doomed to cry alone." %(paired_assignee, dummy))


if __name__ == '__main__':
    main(sys.argv) 
    #print(Get_Task_per_Date(7,3))
    pass