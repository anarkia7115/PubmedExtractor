#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

def main():
  with open("./error_txt_folder/error_txt") as f:
    for line in f:

      filtered_string = ''.join(s for s in line if s in string.printable)
      print filtered_string

if __name__ == "__main__":
  main()
