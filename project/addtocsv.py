#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Compare CSVs, adding any new items in the first CSV to the second CSV.
import os, sys
import doctest
import argparse
import unicodecsv as csv
from cStringIO import StringIO
from shutil import copyfile

def addtocsv(args):
    """ 
        >>> args = build_parser(['--verbose', 'tests/project-longform.csv', 'tests/data.csv'])
        >>> addtocsv(args)
        """
    if len(args.files[0]) > 1:
        new = csv.DictReader(file(args.files[0][0], 'rb'), encoding='utf-8')
        current = csv.DictReader(file(args.files[0][1], 'rb'), encoding='utf-8')

        # Loop through each item in the new csv.
        # If the new item isn't in the current, add it.
        # If the new item is already in the current but has some changes, overwrite the current's item.
        to_add = []
        to_update = []
        ids = []
        current_items = []
        for i, new in enumerate(new):
            for j, existing in enumerate(current):
                current_items.append(existing)
                if new['url'] == existing['url']:
                    if new['url'] not in ids:
                        ids.append(new['url'])
                        to_update.append(new)
                else:
                    if new['url'] not in ids:
                        ids.append(new['url'])
                        to_add.append(new)
            else:
                if new['url'] not in ids:
                    ids.append(new['url'])
                    to_add.append(new)

        # Write the current csv
        # First write all the update & additions, and record the id's.
        # Then loop through the existing records and if we haven't already written them, write 'em.
        with open(args.files[0][1], 'rb') as csvfile:
            h = csv.reader(csvfile)
            fieldnames = h.next()
            del h

        with open(args.files[0][1], 'wb') as csvfile:
            current = csv.DictReader(file(args.files[0][1], 'rb'), encoding='utf-8')
            writefile = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writefile.writeheader()
            ids = []
            for item in to_add + to_update:
                ids.append(item['url'])
                #print item
                writefile.writerow(item)

            for item in current_items:
                if item['url'] not in ids:
                    if args.verbose:
                        print "NEW", item['url']
                    writefile.writerow(item)

def main(args):
    addtocsv(args)

def build_parser(args):
    """ A method to handle argparse.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python addtocsv.py file-new.csv file-existing.csv',
                                     description='''Takes a list of CSVs passed as args.
                                                  Returns the items that are in the first one but not in the subsequent ones.''',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("--test", dest="test", default=False, action="store_true")
    parser.add_argument("files", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv)

    if args.test:
        doctest.testmod(verbose=args.verbose)

    main(args)
