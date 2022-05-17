from defines import *
from regex_dict import RegexDict
import content_parser


def invitation_handler(content):
    f = open('templates/Invitation/hello.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def heroes_handler(content):
    f = open('templates/1/Task.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def heroes_task_handler(content):
    r = content_parser.match_odin(content)
    if r:
        f = open('templates/1/Success.html', 'r', encoding="utf-8")
    else:
        f = open('templates/1/Fail.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def places_handler(content):
    f = open('templates/2/Task.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def places_task_handler(content):
    r = content_parser.match_cthulhu(content)
    if r:
        f = open('templates/2/Success.html', 'r', encoding="utf-8")
    else:
        f = open('templates/2/Fail.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def planes_handler(content):
    f = open('templates/3/Task.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def planes_task_handler(content):
    r = content_parser.match_planes_task(content)
    if r:
        f = open('templates/3/Success.html', 'r', encoding="utf-8")
    else:
        f = open('templates/3/Fail.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def alchemy_handler(content):
    f = open('templates/4/Task.html', 'r', encoding="utf-8")
    html = f.read()
    return html


def alchemy_task_handler(content):
    r = content_parser.match_alchemists(content)
    if r:
        f = open('templates/4/Success.html', 'r', encoding="utf-8")
    else:
        f = open('templates/4/Fail.html', 'r', encoding="utf-8")
    html = f.read()
    return html


handlers = RegexDict()
handlers['IN.02.BW SILVER BIRD'] = invitation_handler
handlers['LIB.21.MTH HEAVEN WHEEL'] = heroes_handler
handlers['LIB.21.MTH WHEEL TURNED'] = heroes_task_handler
handlers['VOD.34.DP LUCID DREAM'] = places_handler
handlers['VOD.34.DP WAKE UP'] = places_task_handler
handlers['MP.AV.42 FLEETING PEGASUS'] = planes_handler
handlers['MP.AV.42 ICARUS RISING'] = planes_task_handler
handlers['PHY.ST.15 BLACK ROSE'] = alchemy_handler
handlers['PHY.ST.15 FLOWER BLOOM'] = alchemy_task_handler


