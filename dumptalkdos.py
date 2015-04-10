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
    
    strings = conv[3:].split(u"\x00")[:12]
    (dec[u"name"],
     dec[u"pronoun"],
     dec[u"description"],
     dec[u"job"],
     dec[u"health"],
     dec[u"keyword_response_1"],
     dec[u"keyword_response_2"],
     dec[u"question"],
     dec[u"question_yes_answer"],
     dec[u"question_no_answer"],
     dec[u"keyword_1"],
     dec[u"keyword_2"]) = [s.rstrip() for s in strings]
    return dec


TOWNE_TLK = [
    u"lcb.tlk",
    u"lycaeum.tlk",
    u"empath.tlk",
    u"serpent.tlk",
    u"moonglow.tlk",
    u"britain.tlk",
    u"jhelom.tlk",
    u"yew.tlk",
    u"minoc.tlk",
    u"trinsic.tlk",
    u"skara.tlk",
    u"magincia.tlk",
    u"paws.tlk",
    u"den.tlk",
    u"vesper.tlk",
    u"cove.tlk",
]

def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(u"-v", u"--verbose", action=u"store_true",
                   help=u"Verbose output.")
    p.add_argument(u"source_dir")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    decoded = list()
    
    for towne in xrange(16):
        with open(os.path.join(args.source_dir, TOWNE_TLK[towne]), u"rb") as f:
            tlk = f.read().decode(u"latin-1")
        
        convs = [tlk[x:x + 0x120] for x in xrange(0, len(tlk), 0x120)]
    
        decoded.extend(decode_conv(c) for c in convs)
    
    print8(json.dumps(decoded, indent=4, sort_keys=True))
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
