# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Feel free to contribute on https://github.com/Arthur-Milchior/anki-tag-empty-cards
# Anki add-on number 536762995 
"""
Add tag empty_n on note whose card name is empty.
"""

import aqt
from aqt import mw
from aqt.qt import *
from anki.collection import _Collection
from anki.utils import ids2str
from anki.notes import Note
import re
def tagCard():
    col = mw.col
    nids =col.db.list(
            "select id from notes ")
    cids = col.genCards(nids)
    cids=ids2str(cids)
    request = "select nid,ord from cards where (id in "+ cids+")"
    print request
    toTagCids=col.db.execute(request)
    for nid, card_ord in toTagCids:
        print "-----------\nConsidering nid:%s, card_ord:%s"%(str(nid),str(card_ord))
        note = Note(col, id=nid)
        model = note._model
        isCloze = model["type"]==1
        print "Model %s: %s."%(str(model["id"]), model["name"])
        if not isCloze:
            print "is cloze."
            templates = model['tmpls']
            template = templates[card_ord]
            try:
                print "Template %s"%(template["name"].encode('utf-8'))
            except UnicodeEncodeError:
                print "Template (unicode error)"
            templateName = template["name"]
            templateName = re.sub(r"\s",r"_",templateName)
        else:
            print "is not cloze."
            templateName= "cloze_%s"%(str(card_ord+1))
        print "template name is %s"% templateName
        tag=("empty_%s"%templateName)
        try:
            print "tagging %s: %s"%(str(nid), tag.encode('utf-8'))
        except UnicodeEncodeError:
            print "tagging %s: %s (unicode error)"%(str(nid),str(card_ord))
        note.addTag(tag)
        note.flush()
    return cids


action = QAction(aqt.mw)
action.setText("Tag Empty Cards")
mw.form.menuTools.addAction(action)
action.triggered.connect(tagCard)
