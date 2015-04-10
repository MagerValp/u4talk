#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import argparse
import json
import os.path
import cgi


def print8(*args):
    print " ".join(unicode(x).encode(u"utf-8") for x in args)


def compare(key, first, other, case=False, maxlen=4):
    if key in (u"keyword_1", u"keyword_2"):
        return first[:maxlen].upper() == other[:maxlen].upper()
    else:
        if isinstance(first, basestring) and isinstance(other, basestring):
            if case:
                return other == first
            else:
                return other.upper() == first.upper()
        else:
            return other == first


TOWNES = [
    u"Castle British",
    u"Lycaeum",
    u"Empath Abbey",
    u"Serpent's Hold",
    u"Moonglow",
    u"Britain",
    u"Jhelom",
    u"Yew",
    u"Minoc",
    u"Trinsic",
    u"Skara Brae",
    u"Magincia",
    u"Paws",
    u"Buccaneer's Den",
    u"Vesper",
    u"Cove",
]

KEYS = [
    u"name",
    u"pronoun",
    u"description",
    u"job",
    u"health",
    u"keyword_1",
    u"keyword_response_1",
    u"keyword_2",
    u"keyword_response_2",
    u"question_trigger",
    u"question",
    u"question_yes_answer",
    u"question_no_answer",
    u"humility_question",
    u"turns_away_prob",
]


LABELS = {
    u"name":                u"Name",
    u"pronoun":             u"Pronoun",
    u"description":         u"LOOK",
    u"job":                 u"JOB",
    u"health":              u"HEAL",
    u"keyword_1":           u"Keyword 1",
    u"keyword_response_1":  u"Response 1",
    u"keyword_2":           u"Keyword 2",
    u"keyword_response_2":  u"Response 2",
    u"question_trigger":    u"Trigger",
    u"question":            u"Question",
    u"question_yes_answer": u"Yes",
    u"question_no_answer":  u"No",
    u"humility_question":   u"Humility",
    u"turns_away_prob":     u"Turns away",
}


def json_label(path):
    return os.path.splitext(os.path.basename(path))[0].replace(u"talk_", u"")


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(u"-v", u"--verbose", action=u"store_true",
                   help=u"Verbose output.")
    p.add_argument(u"-l", u"--len", type=int, default=4,
                   help=u"Keyword length")
    p.add_argument(u"json_talks", nargs=u"+")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    compare_case = list()
    talks = list()
    for num, talk in enumerate(args.json_talks):
        with open(talk, u"rb") as f:
            t = json.load(f)
            talks.append(t)
            chars = set()
            if num >= 1:
                for name in [x[u"name"] for x in t]:
                    chars |= set(c for c in name)
                charset = u"".join(sorted(chars))
                compare_case.append(u"abc" in charset)
    
    print8(u"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<title>talk</title>
	<style>

th.name {
	background-color: #eee;
	font-size: 120%;
	padding: 16px 4px 4px 4px;
	font-family: sans-serif;
	border-bottom: none;
}

th.key {
    font-family: sans-serif;
    font-size: 75%;
	line-height: 140%;
}

th.filename {
	text-align: center;
	background-color: #eee;
    font-family: sans-serif;
    font-size: 75%;
    border-top: none;
    border-left: none;
    border-right: none;
}

th:last-of-type.filename {
    border-left: none;
	border-right: 1px solid #888;
}

th:first-of-type.filename {
    border-right: none;
	border-left: 1px solid #888;
}

table.talk .diff {
	color: #f00;
}

table.talk {
	border-collapse: collapse;
}

table.talk td, th {
	border: 1px solid #888;
	margin: 0;
	padding: 2px 4px;
	vertical-align: top;
	white-space: pre;
	text-align: left;
}

	</style>
</head>

<body>

<table class="talk">
<tbody>
""")
    for i in xrange(len(talks[0])):
        convs = [talk[i] for talk in talks]
        print8(u'<tr><th class="name" colspan="%d">%02x - %s - %s</th></tr>' % (len(convs) + 1, i, TOWNES[i >> 4], convs[0][u"name"].replace(u"\n", u" ")))
        print8(u'<tr><th class="filename"></th>%s</tr>' % (u"".join(u'<th class="filename">%s</th>' % json_label(x) for x in args.json_talks)))
        for key in KEYS:
            if args.len != 4:
                if key not in (u"keyword_1", u"keyword_2"):
                    continue
            first = convs[0][key]
            rest = [u"<td>%s</td>" % cgi.escape(unicode(c[key])) \
                        if compare(key, first, c[key], compare_case[num], args.len) else \
                    u'<td class="diff">%s</td>' % cgi.escape(unicode(c[key])) \
                        for num, c in enumerate(convs[1:])]
                
            print8(u'<tr><th class="key">%s</th><td>%s</td>%s</tr>' % (LABELS[key], first, u"".join(rest)))
    print8(u"""</tbody>
</table>

</body>
""")
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
