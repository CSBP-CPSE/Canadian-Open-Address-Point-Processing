# rask-cask-python

A package that includes two standardizing tools:
- Road Attribute Search Key (RASK), that standardizes road attributes (street name, street type, etc).
- Community Attribute Search Key (CASK), that standardizes municipality names.

The rask-cask Python module is based from the rules defined in the [RASK/CASK specifications](https://gccode.ssc-spc.gc.ca/stats-srgd/rask-cask-python/wikis/RASK/RASK-CASK-Specifications).

## Installation
```bash
# Install for current user.
python setup.py install --user
```

You may need to run the above commands with `sudo`

## Example 1: Simplest operation.
```python
# Simple example.
from rask_cask import RASK
standardized_address = RASK(str_nme='saint laurent boulevard', pr_uid=35)
standardized_address.run()
print(standardized_address)
```

## Example 2: Print all RASK/CASK rules that had an effect in changing the input string.
```python
from rask_cask import RASK
from pprint import pprint

standardized_address = RASK(str_nme='BIG SPRINGS DR SE', pr_uid=35, 
                            logging=True)
standardized_address.run()
pprint(standardized_address.trace)
```

## Example 3: Process a CSV file, standardize all values, and output a standardized CSV file.
```python
# Assuming Python 3 and a CSV file structured as follows (no header value required):
# ngd_str_uid,str_nme,str_typ,str_dir,pr_uid
import csv
from rask_cask import RASK


def standardize_street_address_file(input_filename, output_filename, status_every=10000):
	with open(input_filename, 'r') as file_fp:
		file_fp = csv.reader(file_fp)
		
		standardized_records = []
		for index, record in enumerate(file_fp):
			if index % status_every == 0:
				print(index)
			
			ngd_str_uid = record[0]
			str_nme = record[1]
			str_typ = record[2]
			str_dir = record[3]
			pr_uid = int(record[4])
			
			# Standardize address attributes.
			standardized_record = RASK(str_nme=str_nme,
									   str_typ=str_typ,
									   str_dir=str_dir,
									   pr_uid=pr_uid)
			standardized_record.run()
			
			srch_nme = standardized_record.srch_nme_no_articles
			srch_typ = standardized_record.srch_typ
			srch_dir = standardized_record.srch_dir
			
			# Add standardized attributes to list (which will be exported to a CSV in the end).
			standardized_records.append([ngd_str_uid, srch_nme, srch_typ, srch_dir])
		
		# Export results.    
		with open(output_filename, 'w') as file_out_fp:
			file_out_fp = csv.writer(file_out_fp)
			file_out_fp.writerows(standardized_records)
			
if __name__ == '__main__':
    parameters = {
        'input_filename': '/home/ripdieg/address_file_to_standardize.csv',
        'output_filename': '/home/ripdieg/standardized_address_file.csv'
    }
    standardize_street_address_file(**parameters)
```

## Credit
Full credit for the development of RASK/CASK goes to:
- Daniel Chenier
- Belinda Ha
- Minnie Lee
- Michael Mayda