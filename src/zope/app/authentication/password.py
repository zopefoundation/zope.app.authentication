##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Backward compatibility imports for password managers."""

# BBB: the password managers were moved into zope.password package.
from zope.password.password import MD5PasswordManager
from zope.password.password import PlainTextPasswordManager
from zope.password.password import SHA1PasswordManager
from zope.password.password import SSHAPasswordManager
from zope.password.password import managers
from zope.password.vocabulary import PasswordManagerNamesVocabulary
