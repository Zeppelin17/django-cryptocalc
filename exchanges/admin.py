"""/**
 * Admin settings for exchanges app
 *
 * @summary Admin settings for exchanges app
 * @author Zeppelin17 <elzeppelin17@gmail.com>
 *
 * Created at     : 2020-04-01 06:42:09 
 * Last modified  : 2020-04-01 06:42:35
 */"""

from django.contrib import admin
from .models import Exchange

admin.site.register(Exchange)
