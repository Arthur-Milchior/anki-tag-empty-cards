# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Feel free to contribute on https://github.com/Arthur-Milchior/anki-tag-empty-cards

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
    request = "select nid,ord from cards where and (id in "+ cids+")"
    print request
    toTagCids=col.db.execute(request)
    for nid, ord in toTagCids:
        note = Note(col, id=nid)
        model = note._model
        template = model['tmpls'][ord]
        templateName = template["name"]
        templateName= re.sub(r"\s",r"_",templateName)
        tag=("empty_%s"%templateName)
        print "tagging %s: %s"%(str(nid), tag)
        note.addTag(tag)
        note.flush()
    return cids


action = QAction(aqt.mw)
action.setText("Tag Empty Cards")
mw.form.menuTools.addAction(action)
action.triggered.connect(tagCard)

