#!/usr/bin/python
#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

#
# Author: Michael Mimo Moratti
# Copyright 'c' 2014
#

import argparse
from xml.etree import ElementTree
import utm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='Input File')
    arguments = parser.parse_args()
 
    xml = ElementTree.parse(arguments.file)
    root = xml.getroot()
    print '$FormatUTM'  
    for wpt in root.iter('{http://www.topografix.com/GPX/1/1/}wpt'): 
        name = wpt.find('{http://www.topografix.com/GPX/1/1/}name')
        elevation = wpt.find('{http://www.topografix.com/GPX/1/1/}ele')
        if name.text != 'FLY045' and name.text != 'COM000' and elevation.text != '0':
            description = wpt.find('{http://www.topografix.com/GPX/1/1/}desc')
            desc_tokens = description.text.split(' ')
            utmcoords = utm.from_latlon(float(wpt.attrib['lat']), float(wpt.attrib['lon']))
            print '%s   %s%s   %i   %i   %s   %s %s' % (name.text, utmcoords[2], utmcoords[3], utmcoords[0], utmcoords[1], elevation.text, name.text, desc_tokens[2])


if __name__ == "__main__":
    main()
