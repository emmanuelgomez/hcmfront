# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hcmfront.forms import PostForm

from django.shortcuts import render

# Create your views here.
def post_new(request):
    form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
