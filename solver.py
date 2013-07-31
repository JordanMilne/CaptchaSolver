"""
Solver for BestWebSoft's equation captcha plugin for Wordpress.
Silly goose, computers are great at symbolic math.
"""

import re
import sys
import urllib2
from BeautifulSoup import BeautifulSoup
from sympy import Eq, symbols, solve


ENG_DIGIT_REGEX = re.compile("[A-Za-z ]")

SUBTRACT = u"\u2212"
TIMES = u"\xd7"
ADD = u"+"
#doesn't actually exist in the CAPTCHA
DIVIDE = "/"

EXPR_VAL_REGEX = "(?:\s+)?([A-Za-z ]+|[0-9]+)?(?:\s+)?"
EXPR_OP_REGEX = r"(?:\s+)?(" + TIMES + "|\+|" + SUBTRACT + ")(?:\s+)?"

#parse an expression of the form (x? op x? = x?)
EXPR_REGEX = re.compile("^" + EXPR_VAL_REGEX + EXPR_OP_REGEX + EXPR_VAL_REGEX + "=" + EXPR_VAL_REGEX + "$")

#what to do for each operator
OP_TABLE = {
    TIMES: lambda x, y: x * y,
    SUBTRACT: lambda x, y: x - y,
    ADD: lambda x, y: x + y,
    DIVIDE: lambda x, y: x / y
}

#Obviously there's a better way to do this, but let's KISS
NAME2NUM = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,

    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,

    "twenty": 20,
    "thirty": 30,
    #According to my spellchecker, it's not fourty. Who knew.
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90
}


def fix_num(str_num):
    #only deal with numbers up to 99 for now

    if str_num is None:
        return None

    #we're just dealing with an ordinary number
    if re.match("^\s?\d+\s?$", str_num):
        return int(str_num)

    #what we're dealing with should be an english number
    assert(re.match(ENG_DIGIT_REGEX, str_num))

    result = 0

    #split up the number into lowercase parts
    parts = map(lambda x: x.lower(), filter(bool, str_num.split(" ")))

    for part in parts:
        #make sure we have a mapping for it
        assert(part in NAME2NUM)

        #add the numeric value of the part to our result
        result += NAME2NUM[part]

    return result


def solve_expr(expr_text):
    m = re.match(EXPR_REGEX, expr_text)

    #parse the numbers and operation out of the expression
    lh, op, rh, val = m.group(1), m.group(2), m.group(3), m.group(4)

    #try and fix up any english-form numbers
    lh = fix_num(lh)
    rh = fix_num(rh)
    val = fix_num(val)

    #create a special value so we can solve for x
    x = symbols("x", integer=True)

    #the input field will be None
    if lh is None:
        lh = x
    elif rh is None:
        rh = x
    elif val is None:
        val = x
    else:
        #what?
        raise Exception("Bad expr parsing")

    #solve for and return x
    return solve(Eq(OP_TABLE[op](lh, rh), val))[0]

def main(argv):
    #get the captcha and make sure we don't have any ugly HTML entities
    soup = BeautifulSoup(urllib2.urlopen(argv[1]), convertEntities=BeautifulSoup.HTML_ENTITIES)

    cpt_expr = soup.find("input", {"name": "cptch_number"}).parent.text

    print "Expr: " + cpt_expr

    print "Solved: " + str(solve_expr(cpt_expr))

if __name__ == '__main__':
    main(sys.argv)
