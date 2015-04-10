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
    
    dec[u"keyword_1"] = conv[0:4].rstrip()
    dec[u"keyword_2"] = conv[4:8].rstrip()
    
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
    ][ord(conv[8])]
    
    dec[u"humility_question"] = [False, True][ord(conv[9])]
    
    dec[u"turns_away_prob"] = int(u"%02x" % ord(conv[10]), 10)
    
    strings = conv[11:0x120].replace(u"\x8d", u"\n").split(u"\x00")
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
    size = sum(len(x) for x in strings[:10]) + 21
    if size & 1:
        size += 1
    return dec, size


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(u"-v", u"--verbose", action=u"store_true",
                   help=u"Verbose output.")
    p.add_argument(u"source_dir")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    decoded = list()
    
    for towne in xrange(16):
        tlk_file = os.path.join(args.source_dir,
                                u"tlk%s.bin" % unichr(0x61 + towne))
        with open(tlk_file, u"rb") as f:
            tlk = f.read().decode(u"latin-1")
        
        offset = 0x30
        while offset + 20 < len(tlk):
            conv, size = decode_conv(tlk[offset:])
            decoded.append(conv)
            offset += size
    
    print8(json.dumps(decoded, indent=4, sort_keys=True))
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
