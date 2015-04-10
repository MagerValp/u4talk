#!/bin/bash


TALK=( \
    talk_Remastered.json \
    talk_DOS1.0.1.json \
    talk_DOS1.0.json \
    talk_Amiga.json \
    talk_C64.json \
    talk_Apple2.json \
    talk_Apple2_old.json \
)


./comparetalk.py ${TALK[@]} > talk.html
