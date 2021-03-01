# modified-rask

This is a modification I (Joseph Kuchar) made to the Python implementation of RASK written by Diego Ripley. RASK is a tool used internally at Statistics Canada to standardise addresses for easier record linking. This version does not use the full set of rules or standardizations used in the original version, as certain choices made for simplifying administrative data are unnecessary for processing address point data.

Most of the following text is as-in Diego's original write-up, with small modifications made where necessary.

## Installation
```bash
# Install for current user.
python setup.py install --user
```

You may need to run the above commands with `sudo`

## Example 1: Simplest operation.
```python
# Simple example.
from modified_cask import RASK
standardized_address = RASK(str_nme='saint laurent boulevard', pr_uid=35)
standardized_address.run()
print(standardized_address)
```

## Example 2: Print all RASK rules that had an effect in changing the input string.
```python
from modified_rask import RASK
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
from modified_rask import RASK


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
