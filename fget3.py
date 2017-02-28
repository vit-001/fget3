# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL

from model.model import Model
from view.base_view import AbstractViewFromModelInterface

view=AbstractViewFromModelInterface()
model=Model(view)

model.goto_url(URL("http://collectionofbestporn.com/most-recent*", test_string='Collection'))

