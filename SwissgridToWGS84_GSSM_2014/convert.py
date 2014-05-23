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
import os
import argparse
from math import pow
import utm
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='input file')
    parser.add_argument('--output', required=True, help='output file name')
    arguments = parser.parse_args()
    
    input_file = open(arguments.file, 'r')
    output_file = open(arguments.output, 'w')
    output_file.write('$FormatUTM\n')
    lines = input_file.readlines()
    for line in lines:
        striped_line = line.strip()
        coordinates = striped_line[-11:]
        height = striped_line[-19:-15]
        x = ''.join([re.sub('\.', '', coordinates[-5:]),'00'])
        y = ''.join([re.sub('\.', '', coordinates[:5]),'00'])

        print '----------------------------------------'
        print 'SG      x: %s   y: %s height: %s' % (x,y,height)
        wgs_84 = lv3_to_wgs84(y, x, height)
        print 'WGS84 lat: %s lng: %s height: %s' % (wgs_84[0],wgs_84[1], wgs_84[2])
        utmcoords = utm.from_latlon(wgs_84[0], wgs_84[1])
        print 'UTM     z: %s%s e: %s      n: %s' % (utmcoords[2], utmcoords[3], utmcoords[0], utmcoords[1]) 
        tokens = striped_line.split(',')
        print 'DUMP:   %s   %s%s   %s   %s   %i   %s %s' % (striped_line[:6],utmcoords[2],utmcoords[3],utmcoords[0],utmcoords[1],wgs_84[2],striped_line[:6],tokens[1].strip())
        output_file.write('%s   %s%s   %i   %i   %i   %s %s\n' % (striped_line[:6],utmcoords[2],utmcoords[3],utmcoords[0],utmcoords[1],wgs_84[2],striped_line[:6],tokens[1].strip()))    
        

def lv3_to_wgs84(y, x, h):

    y_aux = (float(y) - 600000.0)/1000000.0;
    x_aux = (float(x) - 200000.0)/1000000.0;

    lat = 16.9023892 +  3.238272 * x_aux -  0.270978 * pow(y_aux,2) -  0.002528 * pow(x_aux,2) -  0.0447 * pow(y_aux,2) * x_aux -  0.0140   * pow(x_aux,3)
    lat = lat * 100.0/36.0;

    lng = 2.6779094 + 4.728982 * y_aux + 0.791484 * y_aux * x_aux + 0.1306   * y_aux * pow(x_aux,2) - 0.0436 * pow(y_aux,3)
    lng = lng * 100.0/36.0;

    height = (float(h) + 49.55) - (12.60 * y_aux) - (22.64 * x_aux)

    return [lat, lng, height]

if __name__ == "__main__":
    main()
