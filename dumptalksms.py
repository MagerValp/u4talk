#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import argparse
import json
import os.path


def print8(*args):
    print " ".join(unicode(x).encode(u"utf-8") for x in args)


def decode_conv(conv):
    dec = dict()
    
    dec[u"question_trigger"] = [
        None,
        u"ERROR_1",
        u"ERROR_2",
        u"job",
        u"health",
        u"keyword 1",
        u"keyword 2",
        u"ERROR_7",
        u"ERROR_8",
        u"ERROR_9",
        u"ERROR_10",
    ][ord(conv[0])]
    
    dec[u"humility_question"] = [False, True][ord(conv[1])]
    
    dec[u"turns_away_prob"] = int(u"%02x" % ord(conv[2]), 10)
    
    dec[u"pronoun"] = [
        u"He",
        u"She",
        u"It",
        None
    ][ord(conv[3])]
    
    dec[u"name"] = conv[4]
    dec[u"description"] = conv[5]
    dec[u"job"] = conv[6]
    dec[u"health"] = conv[7]
    dec[u"keyword_response_1"] = conv[8]
    dec[u"keyword_response_2"] = conv[9]
    dec[u"question"] = conv[10]
    dec[u"question_yes_answer"] = conv[11]
    dec[u"question_no_answer"] = conv[12]
    dec[u"keyword_1"] = conv[13]
    dec[u"keyword_2"] = conv[14]

    return dec


TOWNE_TLK_OFFSET_EUROPE_BETA = [
    0x6C020,
    0x6CFC9,
    0x6DFA7,
    0x6EF95,
    0x70020,
    0x70F73,
    0x71F2E,
    0x72E7A,
    0x74020,
    0x74F96,
    0x75E56,
    0x76D75,
    0x78020,
    0x78DA5,
    0x79BF8,
    0x7AB5F,
]

TOWNE_TLK_OFFSET_EUROPE = [
    0x6C020,
    0x6CFE6,
    0x6DFE0,
    0x6EFE0,
    0x70020,
    0x70F85,
    0x71F45,
    0x72EA0,
    0x74020,
    0x74FA9,
    0x75E76,
    0x75E76,
    0x78020,
    0x78DB6,
    0x79C1B,
    0x7AB8A,
]

def readString(myfile, char):
    chars = []
    while True:
        c = myfile.read(1)
        if c == chr(char):
            return "".join(chars)
        chars.append(c)
        
def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(u"-v", u"--verbose", action=u"store_true",
                   help=u"Verbose output.")
    p.add_argument(u"source_dir")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    decoded = list()
    

        
    for towne in xrange(16):
        with open(os.path.join(args.source_dir, "UltimaIV.sms"), u"rb") as f:
            f.seek(TOWNE_TLK_OFFSET_EUROPE[towne])
            convs = []
            for character in xrange(16):
                conv = []
                conv.append(f.read(1).decode(u"latin-1"))
                conv.append(f.read(1).decode(u"latin-1"))
                conv.append(f.read(1).decode(u"latin-1"))
                conv.append(f.read(1).decode(u"latin-1"))
                readString(f, 0xFF)
                for text in xrange(11):
                    stuff = readString(f, 0x00)
                    #print(stuff)
                    conv.append(stuff)
                #print(conv)
                decode_conv(conv)
                convs.append(conv)
            #print(convs)
            decoded.extend(decode_conv(c) for c in convs)
    
    print8(json.dumps(decoded, indent=4, sort_keys=True))
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
