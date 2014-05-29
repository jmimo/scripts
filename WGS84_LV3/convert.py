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
from math import pow, floor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--x_coordinate', help='X Coordinate')
    parser.add_argument('-y', '--y_coordinate', help='Y Coordinate')
    parser.add_argument('-e', '--east', help='LV3 east coordinate')
    parser.add_argument('-n', '--north', help='LV3 north coordinate')
    parser.add_argument('-hi', '--height', required=True, help='Height')
    arguments = parser.parse_args()

    result = None

    if arguments.x_coordinate:
        result = wgs84_to_lv3(arguments.y_coordinate, arguments.x_coordinate, arguments.height)
        print 'WGS84 -> LV3'
        print 'IN latitude: %s longitude: %s height: %s' % (arguments.x_coordinate, arguments.y_coordinate, arguments.height)
        print 'OUT east: %s north: %s height: %s' % (result[1], result[0], result[2])
    if arguments.east:
       result = lv3_to_wgs84(arguments.east, arguments.north, arguments.height)
       print 'LV3 -> WGS84'
       print 'IN east: %s north: %s height: %s' % (arguments.east, arguments.north, arguments.height)
       print 'OUT latitude: %s longitude: %s height: %s' % (result[0], result[1], result[2])

def wgs84_to_lv3(y, x, h):
    y_sex = decimal_to_sexagesimal(y)
    x_sex = decimal_to_sexagesimal(x)
    y_sec = sexagesimal_to_seconds(y_sex)
    x_sec = sexagesimal_to_seconds(x_sex)

    lat_aux = (x_sec - 169028.66) / 10000.0
    lng_aux = (y_sec - 26782.5) / 10000.0

    lat = ((200147.07 + (308807.95 * lat_aux) + (3745.25 * pow(lng_aux, 2)) + (76.63 * pow(lat_aux, 2))) - (194.56 * pow(lng_aux, 2) * lat_aux)) + (119.79 * pow(lat_aux, 3))
    lng = (600072.37 + (211455.93 * lng_aux)) - (10938.51 * lng_aux * lat_aux) - (0.36 * lng_aux * pow(lat_aux, 2)) - (44.54 * pow(lng_aux, 3))

    height = (float(h) - 49.55) + (2.73 * lng_aux) + (6.94 * lat_aux)
    return [lat,lng,height]

def decimal_to_sexagesimal(angle):
    degrees = floor(float(angle))
    minutes = floor((float(angle) - degrees) * 60.0)
    seconds = (((float(angle) - degrees) * 60.0) - minutes) * 60.0
    return degrees + (minutes / 100.0) + (seconds / 10000)

def sexagesimal_to_seconds(angle):
    degrees = floor(float(angle))
    minutes = floor((float(angle) - degrees) * 100.0)
    seconds = (((float(angle) - degrees) * 100.0) - minutes) * 100.0
    return seconds + (minutes * 60) + (degrees * 3600)

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
