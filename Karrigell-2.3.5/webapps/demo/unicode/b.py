#!/usr/bin/python
# -*- coding: iso8859_1 -*-

import HIP
H = HIP.HTMLStream()
H + u"Cette phrase est �crite en ISO8859-1 codage mais contient un caract�re qui ne peut �tre repr�sent� en ce codage:  c\u0153ur"


