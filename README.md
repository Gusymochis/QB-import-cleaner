# QuickBooks Import Cleaner

Simple tool for cleaning and fixing CVS bank import for QuickBooks Online.

## Purpose

Some banks don't provide csv data as csv, instead they may add spurious headers, extra columns and even encode a Microsoft Excel file Binary and output the file as a CSV.

This tool will autodetect the bank where the file was exported and apply a set of rules for automatically convert the file to a supported format by QuickBooks Online. The generated files can then be used for manual import.

## Supported Banks

Right now it suppoorts 2 types of bankk imports from Mexico:
1. Banorte
2. Banregio


# Requirements

* Pandas
* Unidecode
