Summary
=======

I was reading an article posted on Reddit and saw that the comments were protected with a simple algebraic expression. I wanted to see how quickly I could break it, and came up with this in an hour and a half.

Usage
=====

    ./solver.py "http://urlofpage/withcaptcha"

solver.py will print the expression and the number that should go in the cptch_number field.

Example
=======

    $ ./solver.py http://localhost/captchatest.php
    Expr: 8 ×=  fifty six
    Solved: 7

Recommendations
===============

Use ReCaptcha or similar image-based captcha plugins. Computers are great at DOM manipulation and algebra, but they're not so great at deciphering distorted text.