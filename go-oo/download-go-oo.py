#!/usr/bin/python

# Copyright (C) 2009 by Axel Freyn <axel dash freyn at gmx dot de>

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import sys
import urllib
system = "linux-i586"
version = "3.2"
source = "http://go-oo.mirrorbrain.org/stable/linux-i586/3.2"

language = "en_US"
distribution = "freedesktop"

package_list = {}
# All localizations
localizations = ["af", "ar", "as", "be", "bg", "bn", "bo", "br", "brx", "bs", "by", 
    "ca", "cs", "cy", "da", "de", "dgo", "dz", "el", "en", "eo", "es", "et", 
    "eu", "fa", "fi", "fr", "ga", "gd", "gl", "gu", "he", "hi", "hr", "hu", 
    "is", "it", "ja", "ka", "kid", "kk", "km", "kn", "ko", "kok", "ks", "ku", "ky", "lo", "lt", 
    "lv", "mai", "mk", "ml", "mn", "mni", "mr", "ms", "my", "nb", "ne", "nl",
    "nn", "nr", "ns", "oc", "om", "or", "pa", "pap", "pl", "ps", "pt", "ro", "ru", "rw", "sa", 
    "sat", "sc", "sd", "sh", "si", "sk", "sl", "sr", "ss", "st", "sv", "sw", "ta",
    "te", "tg", "th", "ti", "tn", "tr", "ts", "ug", "uk", "ur", "uz", "ve", "vi", 
    "xh", "zh", "zu"] 
# All dialects
sublocalizations = { "bn": [None, "BD", "IN"], "en": ["GB", "US", "ZA"],
    "pt": [None, "BR"], "sw": [None, "TZ"], "zh": ["CN", "TW"], 
    "gu" : [None, "IN"] }
# analyze parameters
for arg in sys.argv[1:]:
  if arg == "--help" or arg == "help":
    print "Helper script to download Go-oo linux packages\n"

    print "Usage: %s [--localization=<id>] [--distribution=<distro>]" %sys.argv[0]
    print "       [--system=<sys> version=<ver>]"
    print ""
    print "Options:"
    print "	--localization - language to download (default: %s)" %language
    print "	--distribution - distribution for which the menus are dowloaded"
    print "	                 (default: %s)" %distribution
    print "	--system - architecture to dowloaded (default: %s)" %system
    print "	--version - version to download (default: %s)\n" %version

    print "Supported languages:"
    for l in localizations[:-1]:
      if sublocalizations.has_key(l):
	for s in sublocalizations[l]:
	  if s:
	    print "%s_%s,"%(l,s),
	  else:
	    print "%s,"%l,
      else:
	print "%s,"%l,
    print localizations[-1],"\n"

    print "Supported distributions:"
    print "freedesktop, mandriva, redhat, suse\n"

    print "Supported systems:"
    print "linux-i586, linux-x86, linux-x86_64\n"
    sys.exit(0)

  param, value = arg.split("=")
  if param == "--localization":
    language = value
  if param == "--distribution":
    distribution = value
  if param == "--system":
    system = value
  if param == "--version":
    version = value
source = "http://go-oo.mirrorbrain.org/stable/%s/%s" % (system, version)

print "Downloading localization %s, distribution %s, system %s, version %s" % (language, distribution, system, version)

# Read the list of all packages from the web-page
for l in localizations:
  if sublocalizations.has_key(l):
    for s in sublocalizations[l]:
      if s != None:
	package_list[l + "_" + s ] = []
      else:
	package_list[l] = []
  else:
    package_list[l] = []
package_list["general"] = []
package_list["menus"] = {}
for line in urllib.urlopen(source).readlines():
  m = re.search(r"<a href=\"([^\"]*\.rpm)\"", line)
  if m == None:
    continue
  package = m.group(1)
  loc_match = re.match(r"[^-]*-([^-]*)-", package)
  loc = loc_match.group(1)
  try:
    localizations.index(loc)
    if sublocalizations.has_key(loc):
      subloc_match = re.match(r"-([^-]*)-", package[loc_match.end(1):] )
      subloc = subloc_match.group(1)
      try:
	sublocalizations[loc].index(subloc)
	package_list[loc + "_" + subloc].append(package)
      except ValueError:
        package_list[loc].append(package)
    else:
      package_list[loc].append(package) 
  except ValueError:
    m = re.search(r"-([^-]*)-(menus)-",package)
    if m == None:
      package_list["general"].append(package)
    else:
      package_list[m.group(2)][m.group(1)] = package
# create download-list
download = []
for p in package_list["general"]:
  download.append(p)
for p in package_list[language]:
  download.append(p)
download.append( package_list["menus"][distribution] )
for p in download:
  print "downloading %s/%s"%(source,p)
  urllib.urlretrieve( source + "/" + p, p)
