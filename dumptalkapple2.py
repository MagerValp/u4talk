#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import argparse
import json
import os.path


def print8(*args):
    print " ".join(unicode(x).encode(u"utf-8") for x in args)


def decode_hex(bytestring, width):
    return [bytestring[offset:offset + width].encode(u"hex") for offset in xrange(0, len(bytestring), width)]

def decode_bytes(bytestring):
    return [ord(x) for x in bytestring]

def decode_towne(towne):
    dec = dict()
    
    dec[u"map_data"] = decode_hex(towne[0:0x0400], 32)
    dec[u"tile_a"] = decode_bytes(towne[0x0400:0x0420])
    dec[u"xpos_a"] = decode_bytes(towne[0x0420:0x0440])
    dec[u"ypos_a"] = decode_bytes(towne[0x0440:0x0460])
    dec[u"tile_b"] = decode_bytes(towne[0x0460:0x0480])
    dec[u"xpos_b"] = decode_bytes(towne[0x0480:0x04a0])
    dec[u"ypos_b"] = decode_bytes(towne[0x04a0:0x04c0])
    dec[u"moves"] = decode_bytes(towne[0x04c0:0x04e0])
    dec[u"talk"] = decode_bytes(towne[0x04e0:0x0500])
    
    return dec


def decode_conv(conv):
    dec = dict()
    
    dec[u"keyword_1"] = conv[0xf0:0xf6].rstrip()
    dec[u"keyword_2"] = conv[0xf6:0xfc].rstrip()
    
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
    ][ord(conv[0xfc])]
    
    dec[u"humility_question"] = [False, True][ord(conv[0xfe])]
    
    dec[u"turns_away_prob"] = int("%02x" % ord(conv[0xff]), 10)
    
    strings = conv[1:0xf0].replace(u"\x8d", u"\n").split(u"\x00")
    (dec[u"name"],
     dec[u"pronoun"],
     dec[u"description"],
     dec[u"job"],
     dec[u"health"],
     dec[u"keyword_response_1"],
     dec[u"keyword_response_2"],
     dec[u"question"],
     dec[u"question_yes_answer"],
     dec[u"question_no_answer"]) = strings[:10]
    
    return dec


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(u"-v", u"--verbose", action=u"store_true",
                   help=u"Verbose output.")
    p.add_argument(u"towne_dsk")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    decoded = list()
    
    with open(args.towne_dsk, u"rb") as f:
        talk = f.read()[:0x10000].decode(u"latin-1")

    for offset in xrange(0, 256 * 256, 256):
        decoded.append(decode_conv(talk[offset:offset + 256]))
    
    print json.dumps(decoded, indent=4, sort_keys=True)
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
