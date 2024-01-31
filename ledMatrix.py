# -----------------------------------------------------------------
# OWNERSHIP
# -----------------------------------------------------------------
"""
Altishofer
"""
import sys


# -----------------------------------------------------------------
# SETTINGS
# -----------------------------------------------------------------
class Settings:
    line1 = ""  # "ABCDEFGHI"
    line2 = "COUNTDOWN"  # "JKLMNOPQR"
    line3 = ""  # "STUVWXYZZ"
    EMUL_ONLY = True


# -----------------------------------------------------------------
# IMPORT
# -----------------------------------------------------------------
import os
import time
from datetime import datetime, timedelta
import multiprocessing
import random
from abc import ABC, abstractmethod
import collections
import numpy as np
import segno  # sudo pip3 install segno-pil
import math
if not Settings.EMUL_ONLY:
    import board, neopixel
    import sounddevice as sd  # sudo pip3 install sounddevice


# -----------------------------------------------------------------
# DEFINITION OF LETTERS AND NUMBERS
# -----------------------------------------------------------------
class NrLetters:
    STARTPOSITIONS_NUMBERS = [792, 576, 252, 36]
    STARTPOSITIONS_FIRSTLINE = [865, 757, 649, 541, 433, 325, 217, 109, 1]
    STARTPOSITIONS_SECONDLINE = [871, 763, 655, 547, 439, 331, 223, 115, 7]
    STARTPOSITIONS_THIRDLINE = [877, 769, 661, 553, 445, 337, 229, 121, 13]

    NUMBERS = {
        0: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 127,
                      128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 109, 110,
                      111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 91, 92, 93, 106,
                      107, 108, 73, 74, 75, 88, 89, 90, 55, 56, 57, 70, 71, 72, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
                      47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                      35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "black": [94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
                      87, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        },
        1: {
            "white": [148, 149, 160, 161, 162, 127, 128, 129, 140, 141, 142, 110, 111, 112, 113, 124, 125, 126, 91, 92,
                      93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 73, 74, 75, 76, 77, 78,
                      79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                      67, 68, 69, 70, 71, 72, 52, 53, 54, 19, 20, 21, 16, 17, 18],
            "black": [145, 146, 147, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 130, 131, 132, 133, 134, 135,
                      136, 137, 138, 139, 143, 144, 109, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 37, 38, 39,
                      40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                      34, 35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        },
        2: {
            "white": [145, 146, 147, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 127, 128, 129, 130, 131,
                      132, 133, 134, 135, 136, 137, 142, 143, 144, 109, 110, 111, 116, 117, 118, 119, 120, 121, 122,
                      123, 124, 125, 126, 91, 92, 93, 99, 100, 101, 106, 107, 108, 73, 74, 75, 80, 81, 82, 88, 89, 90,
                      55, 56, 57, 63, 64, 65, 70, 71, 72, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 52, 53, 54, 19, 20,
                      21, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 18],
            "black": [148, 149, 150, 151, 138, 139, 140, 141, 112, 113, 114, 115, 94, 95, 96, 97, 98, 102, 103, 104,
                      105, 76, 77, 78, 79, 83, 84, 85, 86, 87, 58, 59, 60, 61, 62, 66, 67, 68, 69, 47, 48, 49, 50, 51,
                      22, 23, 24, 25, 26, 11, 12, 13, 14, 15],
        },
        3: {
            "white": [145, 146, 147, 152, 153, 154, 160, 161, 162, 127, 128, 129, 135, 136, 137, 142, 143, 144, 109,
                      110, 111, 116, 117, 118, 124, 125, 126, 91, 92, 93, 99, 100, 101, 106, 107, 108, 73, 74, 75, 80,
                      81, 82, 88, 89, 90, 55, 56, 57, 63, 64, 65, 70, 71, 72, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
                      47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                      35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "black": [148, 149, 150, 151, 155, 156, 157, 158, 159, 130, 131, 132, 133, 134, 138, 139, 140, 141, 112,
                      113, 114, 115, 119, 120, 121, 122, 123, 94, 95, 96, 97, 98, 102, 103, 104, 105, 76, 77, 78, 79,
                      83, 84, 85, 86, 87, 58, 59, 60, 61, 62, 66, 67, 68, 69],
        },
        4: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 135, 136, 137, 138, 139, 140, 141, 142, 143,
                      144, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 99, 100, 101, 77, 78, 79, 80, 81, 82, 83,
                      84, 85, 86, 87, 88, 89, 90, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 41, 42, 43,
                      44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 27, 28, 29, 8, 9, 10],
            "black": [155, 156, 157, 158, 159, 160, 161, 162, 127, 128, 129, 130, 131, 132, 133, 134, 119, 120, 121,
                      122, 123, 124, 125, 126, 91, 92, 93, 94, 95, 96, 97, 98, 102, 103, 104, 105, 106, 107, 108, 73,
                      74, 75, 76, 69, 70, 71, 72, 37, 38, 39, 40, 19, 20, 21, 22, 23, 24, 25, 26, 30, 31, 32, 33, 34,
                      35, 36, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18],
        },
        5: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 160, 161, 162, 127, 128, 129, 135, 136, 137,
                      138, 139, 140, 141, 142, 143, 144, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 124, 125,
                      126, 91, 92, 93, 99, 100, 101, 106, 107, 108, 73, 74, 75, 80, 81, 82, 88, 89, 90, 55, 56, 57, 63,
                      64, 65, 70, 71, 72, 37, 38, 39, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23,
                      24, 25, 26, 27, 28, 29, 34, 35, 36, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "black": [155, 156, 157, 158, 159, 130, 131, 132, 133, 134, 119, 120, 121, 122, 123, 94, 95, 96, 97, 98,
                      102, 103, 104, 105, 76, 77, 78, 79, 83, 84, 85, 86, 87, 58, 59, 60, 61, 62, 66, 67, 68, 69, 40,
                      41, 42, 43, 30, 31, 32, 33, 4, 5, 6, 7],
        },
        6: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 127,
                      128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 109, 110,
                      111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 91, 92, 93, 99,
                      100, 101, 106, 107, 108, 73, 74, 75, 80, 81, 82, 88, 89, 90, 55, 56, 57, 63, 64, 65, 70, 71, 72,
                      37, 38, 39, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                      29, 34, 35, 36, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "black": [94, 95, 96, 97, 98, 102, 103, 104, 105, 76, 77, 78, 79, 83, 84, 85, 86, 87, 58, 59, 60, 61, 62,
                      66, 67, 68, 69, 40, 41, 42, 43, 30, 31, 32, 33, 4, 5, 6, 7],
        },
        7: {
            "white": [145, 146, 147, 142, 143, 144, 109, 110, 111, 106, 107, 108, 73, 74, 75, 70, 71, 72, 37, 38, 39,
                      40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                      28, 29, 30, 31, 32, 33, 34, 35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                      18],
            "black": [148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 127, 128, 129, 130,
                      131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 112, 113, 114, 115, 116, 117, 118, 119,
                      120, 121, 122, 123, 124, 125, 126, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
                      105, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 55, 56, 57, 58, 59, 60, 61, 62,
                      63, 64, 65, 66, 67, 68, 69],
        },
        8: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 127,
                      128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 109, 110,
                      111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 91, 92, 93, 99,
                      100, 101, 106, 107, 108, 73, 74, 75, 80, 81, 82, 88, 89, 90, 55, 56, 57, 63, 64, 65, 70, 71, 72,
                      37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 19, 20, 21, 22, 23, 24,
                      25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                      16, 17, 18],
            "black": [94, 95, 96, 97, 98, 102, 103, 104, 105, 76, 77, 78, 79, 83, 84, 85, 86, 87, 58, 59, 60, 61, 62,
                      66, 67, 68, 69],
        },
        9: {
            "white": [145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 160, 161, 162, 127, 128, 129, 135, 136, 137,
                      138, 139, 140, 141, 142, 143, 144, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 124, 125,
                      126, 91, 92, 93, 99, 100, 101, 106, 107, 108, 73, 74, 75, 80, 81, 82, 88, 89, 90, 55, 56, 57, 63,
                      64, 65, 70, 71, 72, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 19,
                      20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18],
            "black": [155, 156, 157, 158, 159, 130, 131, 132, 133, 134, 119, 120, 121, 122, 123, 94, 95, 96, 97, 98,
                      102, 103, 104, 105, 76, 77, 78, 79, 83, 84, 85, 86, 87, 58, 59, 60, 61, 62, 66, 67, 68, 69],
        },
        "middlepoint": [508, 509, 510, 499, 498, 497, 472, 473, 474, 514, 515, 516, 493, 492, 491, 478, 479, 480],
        # "middlepoint":[510, 511, 512, 499, 498, 497, 474, 475, 476, 515, 516, 517, 494, 493, 492, 479, 481, 480],
    }

    LETTERS = {
        "A": {
            "white": [72, 37, 36, 74, 2, 75, 3, 76, 69, 40, 33, 4, 77, 5],
            "black": [73, 1, 71, 38, 35, 70, 39, 34, 68, 41, 32]
        },
        "B": {
            "white": [72, 37, 36, 74, 2, 75, 70, 39, 34, 76, 4, 77, 68, 41, 32, 5],
            "black": [73, 1, 71, 38, 35, 3, 69, 40, 33]
        },
        "C": {
            "white": [72, 37, 36, 1, 74, 75, 76, 68, 41, 32, 5],
            "black": [73, 71, 38, 35, 2, 70, 39, 34, 3, 69, 40, 33, 4, 77]
        },
        "D": {
            "white": [73, 72, 37, 74, 35, 75, 3, 76, 4, 77, 68, 41, 32],
            "black": [36, 1, 71, 38, 2, 70, 39, 34, 69, 40, 33, 5]
        },
        "E": {
            "white": [73, 72, 37, 36, 1, 74, 75, 70, 39, 34, 76, 77, 68, 41, 32, 5],
            "black": [71, 38, 35, 2, 3, 69, 40, 33, 4]
        },
        "F": {
            "white": [73, 72, 37, 36, 1, 74, 75, 70, 39, 34, 76, 77],
            "black": [71, 38, 35, 2, 3, 69, 40, 33, 4, 68, 41, 32, 5]
        },
        "G": {
            "white": [72, 37, 36, 1, 74, 75, 39, 34, 3, 76, 4, 68, 41, 32, 5],
            "black": [73, 71, 38, 35, 2, 70, 69, 40, 33, 77]
        },
        "H": {
            "white": [73, 1, 74, 2, 75, 70, 39, 34, 3, 76, 4, 77, 5],
            "black": [72, 37, 36, 71, 38, 35, 69, 40, 33, 68, 41, 32]
        },
        "I": {
            "white": [73, 72, 37, 36, 1, 38, 39, 40, 77, 68, 41, 32, 5],
            "black": [74, 71, 35, 2, 75, 70, 34, 3, 76, 69, 33, 4]
        },
        "J": {
            "white": [72, 37, 36, 1, 2, 3, 76, 4, 68, 41, 32],
            "black": [73, 74, 71, 38, 35, 75, 70, 39, 34, 69, 40, 33, 77, 5]
        },
        "K": {
            "white": [73, 1, 74, 35, 75, 70, 39, 34, 76, 33, 77, 5],
            "black": [72, 37, 36, 71, 38, 2, 3, 69, 40, 4, 68, 41, 32]
        },
        "L": {
            "white": [73, 74, 75, 76, 77, 68, 41, 32, 5],
            "black": [72, 37, 36, 1, 71, 38, 35, 2, 70, 39, 34, 3, 69, 40, 33, 4]
        },
        "M": {
            "white": [73, 72, 36, 1, 74, 38, 2, 75, 39, 3, 76, 4, 77, 5],
            "black": [37, 71, 35, 70, 34, 69, 40, 33, 68, 41, 32]
        },
        "N": {
            "white": [73, 1, 74, 71, 2, 75, 39, 3, 76, 33, 4, 77, 5],
            "black": [72, 37, 36, 38, 35, 70, 34, 69, 40, 68, 41, 32]
        },
        "O": {
            "white": [72, 37, 36, 74, 2, 75, 3, 76, 4, 68, 41, 32],
            "black": [73, 1, 71, 38, 35, 70, 39, 34, 69, 40, 33, 77, 5]
        },
        "P": {
            "white": [72, 37, 36, 74, 2, 75, 3, 76, 69, 40, 33, 77],
            "black": [73, 1, 71, 38, 35, 70, 39, 34, 4, 68, 41, 32, 5]
        },
        "Q": {
            "white": [72, 37, 36, 74, 2, 75, 3, 76, 33, 68, 41, 5],
            "black": [73, 1, 71, 38, 35, 70, 39, 34, 69, 40, 4, 77, 32]
        },
        "R": {
            "white": [73, 72, 37, 36, 74, 2, 75, 3, 76, 69, 40, 33, 77, 5],
            "black": [1, 71, 38, 35, 70, 39, 34, 4, 68, 41, 32]
        },
        "S": {
            "white": [72, 37, 36, 1, 74, 70, 39, 34, 4, 77, 68, 41, 32],
            "black": [73, 71, 38, 35, 2, 75, 3, 76, 69, 40, 33, 5]
        },
        "T": {
            "white": [73, 72, 37, 36, 1, 38, 39, 40, 41],
            "black": [74, 71, 35, 2, 75, 70, 34, 3, 76, 69, 33, 4, 77, 68, 32, 5]
        },
        "U": {
            "white": [73, 1, 74, 2, 75, 3, 76, 4, 68, 41, 32],
            "black": [72, 37, 36, 71, 38, 35, 70, 39, 34, 69, 40, 33, 77, 5]
        },
        "V": {
            "white": [73, 1, 74, 2, 75, 3, 69, 33, 41],
            "black": [72, 37, 36, 71, 38, 35, 70, 39, 34, 76, 40, 4, 77, 68, 32, 5]
        },
        "W": {
            "white": [73, 1, 74, 2, 75, 39, 3, 76, 40, 4, 68, 32],
            "black": [72, 37, 36, 71, 38, 35, 70, 34, 69, 33, 77, 41, 5]
        },
        "X": {
            "white": [73, 1, 71, 35, 39, 69, 33, 77, 5],
            "black": [72, 37, 36, 74, 38, 2, 75, 70, 34, 3, 76, 40, 4, 68, 41, 32]
        },
        "Y": {
            "white": [73, 1, 74, 2, 70, 34, 40, 41],
            "black": [72, 37, 36, 71, 38, 35, 75, 39, 3, 76, 69, 33, 4, 77, 68, 32, 5]
        },
        "Z": {
            "white": [73, 72, 37, 36, 1, 35, 39, 69, 77, 68, 41, 32, 5],
            "black": [74, 71, 38, 2, 75, 70, 34, 3, 76, 40, 33, 4]
        },
        " ": {
            "white": [],
            "black": [74, 71, 38, 2, 75, 70, 34, 3, 76, 40, 33, 4, 73, 72, 37, 36, 1, 35, 39, 69, 77, 68, 41, 32, 5],
        },
        "corrLines": {
            1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [-6, 6, -6, 6, -6, -6, 6, -6, 6, -6, -6, 6, -6, 6, -6, -6, 6, -6, 6, -6, -6, 6, -6, 6, -6],
            3: [-12, 12, -12, 12, -12, -12, 12, -12, 12, -12, -12, 12, -12, 12, -12, -12, 12, -12, 12, -12, -12, 12,
                -12, 12, -12],
            4: [73, 72, 37, 36, 1, 74, 71, 38, 35, 2, 75, 70, 39, 34, 3, 76, 69, 40, 33, 4, 77, 68, 41, 32, 5]
        }}

    COLORS = [
        (6, 7, 7),
        (31, 7, 7),
        (47, 15, 7),
        (71, 15, 7),
        (87, 23, 7),
        (103, 31, 7),
        (119, 31, 7),
        (143, 39, 7),
        (159, 47, 7),
        (175, 63, 7),
        (191, 71, 7),
        (199, 71, 7),
        (223, 79, 7),
        (223, 87, 7),
        (223, 87, 7),
        (215, 95, 7),
        (215, 95, 7),
        (215, 103, 15),
        (207, 111, 15),
        (207, 119, 15),
        (207, 127, 15),
        (207, 135, 23),
        (199, 135, 23),
        (199, 143, 23),
        (199, 151, 31),
        (191, 159, 31),
        (191, 159, 31),
        (191, 167, 39),
        (191, 167, 39),
        (191, 175, 47),
        (183, 175, 47),
        (183, 183, 47),
        (183, 183, 55),
        (207, 207, 111),
        (223, 223, 159),
        (239, 239, 199),
        (255, 255, 255),
    ]
    COLORS.reverse()


# -----------------------------------------------------------------
# HELPER FUNCTIONS FOR TIME CALCULATIONS
# -----------------------------------------------------------------
class Time:

    @staticmethod
    def getCurrentTimeList():
        return [i for i in datetime.now().strftime("%H%M")]

    @staticmethod
    def getTimeDiff():
        dtNow = datetime.now()
        if dtNow.hour < 4:
            dtThen = datetime(dtNow.year, dtNow.month, dtNow.day, 4, 0, 0, 0)
        else:
            tomorrow = dtNow + timedelta(days=1)
            dtThen = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 4, 0, 0, 0)
        dtTable = [int(i) for i in ':'.join(str(dtThen - dtNow).split(':')[:2]).replace(":", "")]
        return dtTable if len(dtTable) == 4 else [0] + dtTable

    @staticmethod
    def secondsPassed(oldTime, seconds: int):
        return True if time.time() - oldTime >= seconds else False


# -----------------------------------------------------------------
# LED EMULATOR FOR LIVE PROCESSING
# -----------------------------------------------------------------
class LedEmu(ABC):

    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.cols = columns
        self.shell = []
        self.fill((0, 0, 0))
        self.bkCol = (0, 0, 0)  # (127, 127, 127)
        os.system("cls")

    @staticmethod
    def colShell(col: tuple, text: str):
        return f"\033[38;2;{col[0]};{col[1]};{col[2]}m {text}\033[0;00m"

    @staticmethod
    def toCoor(n: int):
        x = 54 - n // 18
        return (x, 17 - n % 18) if (n // 18) % 2 != 0 else (x, n % 18)

    @staticmethod
    def toN(x: int, y: int):
        return (54 - x) * 18 + (y % 18 if x % 2 == 0 else 17 - (y % 18))

    def pixel(self, nr: int, colTpl: tuple):
        crdTpl = LedEmu.toCoor(nr)
        self.shell[crdTpl[0]][crdTpl[1]] = colTpl

    def getColCor(self, x: int, y: int):
        return self.shell[x][y]

    def show(self):
        desired_fps = 20
        desired_delay = 1.0 / desired_fps
        # os.system("cls")
        finalOutput = ""
        for y in range(self.cols):
            line = ""
            for x in range(self.rows):
                r, g, b = self.shell[x][y][0], self.shell[x][y][1], self.shell[x][y][2]
                if self.shell[x][y] == (0, 0, 0):
                    line += LedEmu.colShell(self.bkCol, "●")
                else:
                    line += LedEmu.colShell((r, g, b), "●")  # ⏺ better alternative but displayed wrong
            finalOutput += line + "\n"
        sys.stdout.write('\b')
        print(finalOutput[:len(finalOutput)//2], end="")
        print(finalOutput[len(finalOutput)//2:], end="")
        if Settings.EMUL_ONLY:
            time.sleep(desired_delay)

    def fill(self, color: tuple):
        self.shell = [([color] * self.cols) for i in range(self.rows)]

    def getBinaryShell(self):
        return self.shell


# -----------------------------------------------------------------
# SIGNAL PROCESSING FOR LEDs
# -----------------------------------------------------------------
class LedScreen:

    def __init__(self, rows: int, columns: int):
        self.countX = rows
        self.countY = columns
        self.countLeds = rows * columns
        self.autoWrite = False
        self.brightness = 0.05
        self.initHardware()
        self.pixel.fill((0, 0, 0))

    def initHardware(self):
        self.pixel = neopixel.NeoPixel(
            board.D12,
            self.countLeds,
            brightness=self.brightness,
            auto_write=self.autoWrite,
            pixel_order=neopixel.RGB
        )


# -----------------------------------------------------------------
# RUNNER FOR PROCESSING EMULATOR AND HARDWARE IN PARALLEL
# -----------------------------------------------------------------
class Runner:

    def __init__(self, rows: int, columns: int, line1: str, line2: str, line3: str):
        self.emulator = LedEmu(rows, columns)
        self.matrix = LedScreen(rows, columns) if not Settings.EMUL_ONLY else None
        self.stdCol = (255, 255, 255)
        self.midCol = (255, 45, 0)
        self.line1 = line1.upper() if line1.isalpha() and len(line1) <= 9 else ""
        self.line2 = line2.upper() if line2.isalpha() and len(line1) <= 9 else ""
        self.line3 = line3.upper() if line3.isalpha() and len(line1) <= 9 else ""
        self.now = time.time()
        self.midPixActive = False
        self.rows = rows if rows > 0 else 1
        self.columns = columns if columns > 0 else 1

    def assign(self, pixel: int, colTpl: tuple):
        self.emulator.pixel(pixel, colTpl)
        if not Settings.EMUL_ONLY:
            self.matrix.pixel[pixel] = colTpl

    def write(self, num: int, start: int):
        for px in NrLetters.NUMBERS[num]["white"]: self.assign(px + start - 1, self.stdCol)
        for px in NrLetters.NUMBERS[num]["black"]: self.assign(px + start - 1, (0, 0, 0))

    def runClock(self):
        while 1:
            if Time.secondsPassed(self.now, 1):
                for dig, pos in zip(Time.getTimeDiff(), NrLetters.STARTPOSITIONS_NUMBERS): self.write(dig, pos)
                for pos in NrLetters.NUMBERS["middlepoint"]: self.assign(pos, (
                    0, 0, 0)) if self.midPixActive else self.assign(pos, self.midCol)
                self.midPixActive = not self.midPixActive
                self.show()

    def runText(self):
        while True:
            if Time.secondsPassed(self.now, 1):
                for line, idx in zip([self.line1, self.line2, self.line3], range(1, 4)):
                    for letter, start in zip(line, NrLetters.STARTPOSITIONS_FIRSTLINE):
                        # self.shuffle()
                        for idxCorrLineGlob, idxCorrLine in zip(NrLetters.LETTERS["corrLines"][4],
                                                                NrLetters.LETTERS["corrLines"][idx]):
                            for letterPx in NrLetters.LETTERS[letter]["white"]:
                                if idxCorrLineGlob == letterPx:
                                    self.assign(letterPx + start - idxCorrLine - 2, self.stdCol)
                            for letterPx in NrLetters.LETTERS[letter]["black"]:
                                if idxCorrLineGlob == letterPx:
                                    self.assign(letterPx + start - idxCorrLine - 2, (0, 0, 0))
                    self.show()

    def alternate(self):
        # self.handleSupProcess(15, self.ricoKaboom, "rico")
        # self.handleSupProcess(10, self.GPT, "GPT")
        # self.handleSupProcess(10, self.animate_pattern, "animate_pattern")
        # self.handleSupProcess(15, self.pingPong, "pingPong")
        # self.handleSupProcess(10, self.centerImpuls, "centerImpuls")
        # # self.handleSupProcess(10, self.puls, "puls")
        # self.handleSupProcess(15, self.rain, "rain")
        # # self.handleSupProcess(10, self.qrTextSmall, "qrTextSmall")
        self.handleSupProcess(1500, self.snakeBfs, "snakeBfs")
        # self.handleSupProcess(10, self.doom, "DoomFire")
        # self.handleSupProcess(10, self.runText, "runText")
        # self.handleSupProcess(10, self.runClock, "runClock")
        # self.handleSupProcess(10, self.runningStripes, "runStripes")
        # self.handleSupProcess(1500000, self.snakeDumb, "snakeDumb")

        # self.handleSupProcess(10, self.loudVisualizer, "loudVisualizer")

    def handleSupProcess(self, tm: int, process, processName: str):
        self.p = multiprocessing.Process(target=process, name=processName, args=())
        self.p.start()
        while self.p.is_alive() and not Time.secondsPassed(self.now, tm): time.sleep(1)
        self.p.join(0)
        self.terminateSp()
        self.reset()

    def terminateSp(self):
        if self.p.is_alive():
            self.p.terminate()
            self.p.join()

    def show(self):
        self.emulator.show()
        if not Settings.EMUL_ONLY:
            self.matrix.pixel.show()
        self.now = time.time()

    def shuffle(self):
        self.stdCol = (random.randint(130, 255),
                       random.randint(150, 255),
                       random.randint(150, 255)
                       )

    def reset(self):
        if not Settings.EMUL_ONLY:
            self.matrix.pixel.fill((0, 0, 0))
        self.emulator.fill((0, 0, 0))
        self.stdCol = (255, 255, 255)
        self.now = time.time()

    def stressTest(self, iter: int):
        start = time.time()
        for cnt in range(iter):
            for px in range(self.rows * self.columns):
                # self.assign(px, (100,100,100))
                self.shuffle()
                self.assign(px, self.stdCol)
            self.show()
            self.reset()
            self.show()
        self.reset()
        self.show()
        print("StressTest: ", round(iter * 2 / (time.time() - start), 1), "FpS")
        time.sleep(3)

    def doom(self):
        rdm = 2
        while 1:
            for x in range(55):
                self.assign(LedEmu.toN(x, 17), NrLetters.COLORS[1])
                for y in range(rdm):
                    if not random.randint(0, 3): self.assign(LedEmu.toN(x, y), (0, 0, 0))
                for y in range(16, 1, -1):
                    if self.emulator.getColCor(x, y + 1) != (0, 0, 0):
                        prColInd = NrLetters.COLORS.index(self.emulator.getColCor(x, y + 1))
                        if not random.randint(0, y - rdm + 1): self.assign(LedEmu.toN(x, y), (0, 0, 0))
                        if 35 >= (prColInd + rdm) * 1.4 >= 0:
                            col = (prColInd + random.randint(0, rdm)) * 1.4
                            newX = x + random.randint(0, 3)  # 3
                            if newX <= 0 or 54 <= newX: newX = x
                            self.assign(LedEmu.toN(newX, y - random.randint(0, rdm)), NrLetters.COLORS[int(col)])
            self.show()
        self.reset()

    def runningStripes(self):
        x = 0
        while "False":
            for y in range(18):
                self.assign(LedEmu.toN(x % 55, y), NrLetters.COLORS[x % 36])
            x += 1
            self.show()

    def snakeBfs(self):

        def getRmPos(snake=[]):
            avgX = sum([x[0] for x in snake]) // len(snake) if snake else 54//2
            avgY = sum([y[1] for y in snake]) // len(snake) if snake else 17//2
            while "False":
                if avgX >= 55//2:
                    newX = random.randint(0, 54//2)
                else:
                    newX = random.randint(54//2, 54)
                if avgY >= 17//2:
                    newY = random.randint(0, 17//2)
                else:
                    newY = random.randint(17//2, 17)

                if [newX, newY] not in snake: return [newX, newY]

        def bfs(grid: list, start: tuple):
            queue = collections.deque([[start]])
            seen = set([start])
            while queue:
                path = queue.popleft()
                x, y = path[-1]
                if grid[y][x] == goal:
                    return path
                for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= x2 < self.columns and 0 <= y2 < self.rows and grid[y2][x2] != wall and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        def showSnake(col=(255, 255, 255)):
            for idx, el in enumerate(snake):
                newCol = []
                for c in col:
                    newCol.append(c if not idx%2 else c//2)
                self.assign(LedEmu.toN(el[0], el[1]), tuple(newCol))
            self.assign(LedEmu.toN(food[0], food[1]), (255, 0, 0))
            self.show()
            self.reset()

        snake = [getRmPos()]
        food = getRmPos(snake)
        lenSnake = 1
        wall, clear, goal = (255, 255, 255), (0, 0, 0), (255, 0, 0)
        while "False":
            try:
                if snake[0] == food:
                    lenSnake += 1
                    cnt = 100
                    while True and cnt:
                        food = getRmPos(snake)
                        self.reset()
                        for el in snake: self.assign(LedEmu.toN(el[0], el[1]), (255, 255, 255))
                        self.assign(LedEmu.toN(food[0], food[1]), (255, 0, 0))
                        path = bfs(self.emulator.shell, (snake[0][1], snake[0][0]))
                        if path: break
                        cnt -= 1
                else:
                    self.reset()
                    for el in snake: self.assign(LedEmu.toN(el[0], el[1]), (255, 255, 255))
                    self.assign(LedEmu.toN(food[0], food[1]), (255, 0, 0))
                    path = bfs(self.emulator.shell, (snake[0][1], snake[0][0]))
                if not path: raise ValueError('Game Over')
                path.pop(0)
                nextPos = path.pop(0)
                snake.insert(0, [nextPos[1], nextPos[0]])
                snake = snake[:lenSnake]
                showSnake()

            except Exception as eMain:
                print("ERROR:", eMain)
                self.assign(LedEmu.toN(food[0], food[1]), (0, 0, 0))
                for cnt in range(10):
                    showSnake((255, 0, 0))
                    showSnake((255, 255, 255))
                os.system('kill %d' % os.getpid())

    def snakeDumb(self):

        def getRmPos(snake=[]):
            while "False":
                pos = [random.randint(0, 54), random.randint(0, 5)]
                if pos not in snake: return pos

        snake = [getRmPos()]
        food = getRmPos(snake)
        self.assign(LedEmu.toN(food[0], food[1]), (255, 0, 0))

        def up():
            if [snake[0][0], (snake[0][1] + 1) % 18] not in snake:
                snake[0][1] = (snake[0][1] + 1) % 18
            else:
                down()

        def down():
            if [snake[0][0], (snake[0][1] - 1) % 18] not in snake:
                snake[0][1] = (snake[0][1] - 1) % 18
            else:
                right()

        def right():
            if [(snake[0][0] + 1) % 55, snake[0][1]] not in snake:
                snake[0][0] = (snake[0][0] + 1) % 55
            else:
                left()

        def left():
            if [(snake[0][0] - 1) % 55, snake[0][1]] not in snake:
                snake[0][0] = (snake[0][0] - 1) % 55
            else:
                up()

        def next(foodOld: list):
            self.reset()
            snake.insert(0, foodOld)
            foodNew = getRmPos(snake)
            self.assign(LedEmu.toN(foodNew[0], foodNew[1]), (255, 0, 0))
            return foodNew

        def showSnake(col=(255, 255, 255)):
            for el in snake: self.assign(LedEmu.toN(el[0], el[1]), col)
            self.assign(LedEmu.toN(food[0], food[1]), (255, 0, 0))
            self.show()
            self.reset()

        def move():
            if len(snake) > 1:
                for k in range(len(snake) - 1, 0, -1): snake[k] = [snake[k - 1][0], snake[k - 1][1]]
            showSnake()

        while "False":
            if abs(snake[0][0] - food[0]) <= 1 and abs(snake[0][1] - food[1]) <= 1:
                food = next(food)
            # if snake[0] == food: food = next(food)
            try:
                while snake[0][0] > food[0]: left(); move()
                while snake[0][0] < food[0]: right(); move()
                while snake[0][1] > food[1]: down(); move()
                while snake[0][1] < food[1]: up(); move()
            except Exception as eMain:
                print("ERROR:", eMain)
                self.assign(LedEmu.toN(food[0], food[1]), (0, 0, 0))
                for cnt in range(10):
                    showSnake((255, 0, 0))
                    showSnake((255, 255, 255))
                os.system('kill %d' % os.getpid())

    def loudVisualizer(self):
        def audio_callback(indata, frames, time, status):
            volume_norm = int(np.linalg.norm(indata) * 10000 % 18)
            for y in range(volume_norm):
                self.assign(LedEmu.toN(0, y), (255, 255, 255))
            for r in range(17, volume_norm, -1):
                self.assign(LedEmu.toN(0, r), (0, 0, 0))
            for x in range(54, 0, -1):
                for y in range(18):
                    self.assign(LedEmu.toN(x, y), self.emulator.getColCor(x - 1, y))
            self.show()

        stream = sd.InputStream(callback=audio_callback)
        with stream:
            sd.sleep(1000000)

    def qrTextSmall(self):
        text = "blubb"
        toGen = text if len(text) <= 21 else "Text is to large"
        qrcode = segno.make_micro(toGen, version="M4")
        img = qrcode.to_pil()
        img = img.convert('RGB')
        for x in range(17):
            for y in range(17):
                self.assign(LedEmu.toN(x + 20, y), img.getpixel((x, y)))
        self.show()
        time.sleep(1000)

    def rain(self):

        class Drop:
            def __init__(self, outerClass):
                self.speed = 1 / random.randint(1, 4)
                self.xStart = random.randint(0, 54)
                self.currY = -1
                self.outer = outerClass
                self.alive = True

            def next(self):
                self.currY += self.speed
                for clr in range(0, int(self.currY) - 1):
                    self.outer.assign(LedEmu.toN(self.xStart, clr), (0, 0, 0))
                for posY, green, blue in zip(
                        [y for y in range(int(self.currY) - 5 if int(self.currY) - 5 >= 0 else 0, int(self.currY))],
                        reversed([(176, 255, 138), (124, 226, 71), (94, 193, 30), (62, 134, 5), (0, 50, 0)]),
                        reversed([(156, 222, 235), (102, 190, 249), (48, 154, 241), (17, 101, 193), (4, 63, 152)])):

                    if self.currY >= 23:
                        self.selfDestruction()
                    else:
                        if posY <= 17: self.outer.assign(LedEmu.toN(self.xStart, posY), green)  # blue

            def selfDestruction(self):
                self.alive = False

        class Rain:
            def __init__(self, outerClass):
                self.drops = []
                self.outer = outerClass

            def addDropp(self):
                self.drops.append(Drop(self.outer))

            def cleanDeadDrops(self):
                self.drops = [drop for drop in self.drops if drop.alive]

            def next(self):
                for drop in self.drops:
                    drop.next()
                self.outer.show()

        r = Rain(self)
        while True:
            r.addDropp()
            r.next()
            r.cleanDeadDrops()

    def puls(self):
        while True:
            for col in range(0, 255, 20):
                for posX in range(55):
                    for posY in range(18):
                        self.assign(LedEmu.toN(posX, posY), (col, 0, 0))
                self.show()
            for col in range(255, -1, -20):
                for posX in range(55):
                    for posY in range(18):
                        self.assign(LedEmu.toN(posX, posY), (col, 0, 0))
                self.show()

    def centerImpuls(self):
        class Wall:
            def __init__(self, outerClass, max: int):
                self.points = []
                self.outer = outerClass
                self.max = max

            def addPoint(self, radius):
                self.points.append(Point(radius, self.outer))
                if len(self.points) > self.max:
                    self.points = self.points[-self.max:]

            def showPoints(self):
                self.outer.reset()
                for point in self.points:
                    point.color()
                self.outer.show()

        class Point:
            def __init__(self, radius: int, outerClass, x=None, y=None):
                self.radius = radius
                self.pixX = random.randint(0, 54)
                self.pixY = random.randint(0, 17)
                self.outer = outerClass
                self.removeDuplicates()

            def removeDuplicates(self):
                while self.outer.emulator.getColCor(self.pixX, self.pixY) != self.outer.emulator.bkCol:
                    self.pixX = random.randint(0, 54)
                    self.pixY = random.randint(0, 17)

            def color(self):
                for x in range(
                        self.pixX - self.radius,
                        self.pixX + self.radius
                ):
                    for y in range(
                            self.pixY - self.radius,
                            self.pixY + self.radius
                    ):
                        if not (0 <= x <= 54 and 0 <= y <= 17): continue
                        curr = self.outer.emulator.getColCor(x, y)[0]
                        dist = ((self.pixX - x) ** 2 + (self.pixY - y) ** 2) ** 0.5
                        factor = (self.radius - dist) / self.radius
                        new = int(255 * factor) + curr if int(255 * factor) + curr < 255 else 255
                        if dist < self.radius:
                            self.outer.assign(LedEmu.toN(x, y), tuple(new for _ in range(3)))
                        else:
                            self.outer.assign(LedEmu.toN(x, y), tuple(curr for _ in range(3)))

        wall = Wall(outerClass=self, max=5)
        while True:
            wall.addPoint(6)
            wall.showPoints()

    def pingPong(self):
        class Wall:
            def __init__(self, outerClass):
                self.__balls = list()
                self.__outerClass = outerClass
                self.addNew()

            def addNew(self):
                self.__balls.append(Ball(self.__outerClass, self))
                self.__adding = True if len(self.__balls) <= 20 else False

            def iterate(self):
                for ball in self.__balls:
                    ball.iterate()

        class Ball:
            def __init__(self, outerClass, wall):
                self.__x = random.randint(2, 50)
                self.__y = random.randint(2, 15)
                self.__leftRight = [-1, 1][random.randint(0, 1)]
                self.__upDown = [-1, 1][random.randint(0, 1)]
                self.outerClass = outerClass

            def iterate(self):
                self.outerClass.assign(LedEmu.toN(self.__x, self.__y), (0, 0, 0))
                self.__bounce()
                self.__x += self.__leftRight
                self.__y += self.__upDown
                self.outerClass.assign(LedEmu.toN(self.__x, self.__y), (255, 255, 255))

            def __bounce(self):
                if self.__x <= 0:
                    self.__leftRight = 1
                elif self.__x >= 54:
                    self.__leftRight = -1
                if self.__y <= 0:
                    self.__upDown = 1
                elif self.__y >= 17:
                    self.__upDown = -1

        wall = Wall(self)
        now = time.time()
        while True:
            if Time.secondsPassed(now, 1.5):
                wall.addNew()
                now = time.time()
            wall.iterate()
            self.show()

    def animate_pattern(self):
        for i in range(256):
            for y in range(18):
                for x in range(55):
                    if (x - 27) ** 2 + (y - 9) ** 2 <= (10 * math.sin(i / 20)) ** 2:
                        self.assign(LedEmu.toN(x, y),
                                    ((i * 15 + 150) % 256, 0, 0))  # ((i+170) % 256, (i + 170) % 256, (i + 170) % 256))
                    else:
                        self.assign(LedEmu.toN(x, y), (0, 0, 0))
            self.show()

    def GPT(self):

        def draw_circle(x, y, r, color):
            for i in range(55):
                for j in range(18):
                    if (r - 1) ** 2 <= (i - x) ** 2 + (j - y) ** 2 < r ** 2:
                        self.assign(LedEmu.toN(i, j), color)

        def draw_hand(length, angle, color):
            for i in range(-1, 1):
                for j in range(-1, 1):
                    x = 27 + math.cos(angle) * (length + i) + math.cos(angle + math.pi / 2) * j
                    y = 9 + math.sin(angle) * (length + i) + math.sin(angle + math.pi / 2) * j
                    self.assign(LedEmu.toN(int(x), int(y)), color)

        def bres(x1: int, y1: int, x2: int, y2: int, color):
            x, y = x1, y1
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            gradient = dy / float(dx) if dx else 10000
            if gradient > 1:
                dx, dy = dy, dx
                x, y = y, x
                x1, y1 = y1, x1
                x2, y2 = y2, x2
            p = 2 * dy - dx

            for k in range(2, dx + 2):
                if p > 0:
                    y = y + 1 if y < y2 else y - 1
                    p = p + 2 * (dy - dx)
                else:
                    p = p + 2 * dy

                x = x + 1 if x < x2 else x - 1
                if x >= y:
                    self.assign(LedEmu.toN(int(x), int(y)), color)
                else:
                    self.assign(LedEmu.toN(int(y), int(x)), color)

        def draw_hand2(length, angle, color, center):
            x = int(center[0] + math.cos(angle) * (length) + math.cos(angle + math.pi / 2))
            y = int(center[1] + math.sin(angle) * (length) + math.sin(angle + math.pi / 2))
            bres(center[0], center[1], x, y, color)

        def show_time():
            while True:
                self.reset()
                center = [27, 9]
                self.assign(LedEmu.toN(center[0], center[1]), (255, 255, 255))
                t = time.localtime()
                draw_circle(center[0], center[1], 9, (255, 255, 255))
                draw_hand2(5, t.tm_sec * math.pi / 30 - math.pi / 2, (0, 0, 255), center)
                draw_hand2(4, t.tm_min * math.pi / 30 - math.pi / 2, (255, 0, 0), center)
                draw_hand2(3, (t.tm_hour + t.tm_min / 60) * math.pi / 6 - math.pi / 2, (255, 255, 255), center)

                self.show()

        show_time()

    def ricoKaboom(self) -> None:

        class Spark:
            def __init__(self, color: tuple, xStart: int, yStart: int, outerClass: Runner, angle: float):
                self.outer = outerClass
                self.__x = xStart
                self.__y = yStart
                self.__angle = angle  # random.uniform(0, math.pi)
                self.__speed = random.uniform(-0.7, 0.7)
                self.__xV = self.__speed * math.sin(self.__angle)
                self.__yV = self.__speed * math.cos(self.__angle)
                self.__lifeTime = random.randint(15, 25)
                self.__color = color

            def alive(self) -> int:
                return max(self.__lifeTime, 0)

            def tick(self):
                self.__yV += 0.04
                self.__x += self.__xV
                self.__y += self.__yV
                self.__lifeTime -= 1

                if 0 < self.__x < 54 and 0 < self.__y < 17 and self.__lifeTime:
                    self.__color = tuple([int(c - c / (self.__lifeTime) * 0.8) for c in self.__color])
                    self.outer.assign(LedEmu.toN(int(self.__x), int(self.__y)), self.__color)
                else:
                    self.lifeTime = 0

        class Rocket:

            def __init__(self, outerClass: Runner):
                self.__outer = outerClass
                self.__x = random.randint(2, 50)
                self.__y = random.randint(0, 10)
                self.__color = ([(255, 0, 0), (0, 255, 0), (255, 255, 255)][random.randint(0, 2)])
                self.__sparks = [Spark(self.__color, self.__x, self.__y, self.__outer, angle) for angle in
                                 np.linspace(0, math.pi, 100)]
                self.__tail = self.createTail()

            def createTail(self) -> list:
                tail = []
                x = self.__x
                y = self.__y
                xv = random.uniform(-0.7, 0.7)
                yv = 0.7
                # dyv = 0.01
                while 0 < x < 54 and 0 < y < 17:
                    tail.append((round(x), round(y)))
                    x += xv
                    y += yv
                return tail

            def tick(self) -> None:
                if self.__tail:
                    x, y = self.__tail.pop()
                    self.__outer.assign(LedEmu.toN(int(x), int(y)), (max(255, 255 - len(self.__tail) * 10), 180, 0))
                else:
                    for spark in self.__sparks:
                        if spark.alive():
                            spark.tick()

            def alive(self) -> int:
                return len([1 for spark in self.__sparks if spark.alive()])

        class Firework:

            def __init__(self, outerClass: Runner):
                self.__outer = outerClass
                self.__activeRockets = 4
                self.__lastStart = time.time()
                self.__rockets = [Rocket(self.__outer) for _ in range(self.__activeRockets)]

            def tick(self) -> None:
                self.__outer.reset()
                for rocket in self.__rockets:
                    if rocket.alive():
                        rocket.tick()
                aliveRockets = []
                for rocket in self.__rockets:
                    if rocket.alive():
                        aliveRockets.append(rocket)

                if len(aliveRockets) < self.__activeRockets and (time.time() - self.__lastStart) > 0.7:
                    self.__lastStart = time.time()
                    aliveRockets.append(Rocket(self.__outer))

                self.__rockets = aliveRockets
                self.__outer.show()

        f = Firework(self)
        while True:
            f.tick()


# -----------------------------------------------------------------
# ASSERTIONS FOR TESTING
# -----------------------------------------------------------------
assert LedEmu.toCoor(0) == (54, 0)
assert LedEmu.toCoor(1) == (54, 1)
assert LedEmu.toCoor(17) == (54, 17)
assert LedEmu.toCoor(18) == (53, 17)
assert LedEmu.toCoor(35) == (53, 0)
assert LedEmu.toCoor(37) == (52, 1)
assert LedEmu.toCoor(36) == (52, 0)
assert LedEmu.toCoor(52) == (52, 16)
assert LedEmu.toCoor(989) == (0, 17)
assert LedEmu.toCoor(973) == (0, 1)
assert LedEmu.toN(x=54, y=0) == 0
assert LedEmu.toN(x=54, y=1) == 1
assert LedEmu.toN(x=54, y=17) == 17
assert LedEmu.toN(x=53, y=17) == 18
assert LedEmu.toN(x=53, y=0) == 35
assert LedEmu.toN(x=52, y=1) == 37
assert LedEmu.toN(x=52, y=0) == 36
assert LedEmu.toN(x=52, y=16) == 52
assert LedEmu.toN(x=0, y=17) == 989
assert LedEmu.toN(x=0, y=1) == 973
assert LedEmu.toN(x=0, y=0) == 972
# -----------------------------------------------------------------
# MAIN THREAD
# -----------------------------------------------------------------
if __name__ == "__main__":
    runner = Runner(55, 18, line1=Settings.line1, line2=Settings.line2, line3=Settings.line3)
    # runner.stressTest(20)
    while True:
        try:
            runner.alternate()
        except Exception as eMain:
            print("ERROR:", eMain)
            runner.alternate()
        except KeyboardInterrupt:
            runner.terminateSp()
            quit()
