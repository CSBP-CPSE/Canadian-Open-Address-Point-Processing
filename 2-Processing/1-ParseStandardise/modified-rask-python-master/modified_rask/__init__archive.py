# -*- coding: utf-8 -*-
"""
This is a stripped down version of the RASK implementation written by Diego Ripley. 
Specifications more fitting for adminstrative data than address point data have been removed.
The street types have been edited to conform to Canada Post standard abbreviations.
"""
from collections import OrderedDict
from modified_rask.helpers import tracer
import re
import sys
from unicodedata import normalize

python_version = sys.version_info.major


class RASK(object):
    # Inputs
    def __init__(self, str_nme='', str_typ='', str_dir='',
                 pr_uid='', logging=False):
        str_nme = str_nme if str_nme else ''
        str_typ = str_typ if str_typ else ''
        str_dir = str_dir if str_dir else ''

        self.srch_nme = str_nme
        self.srch_typ = str_typ
        self.srch_dir = str_dir
        self.pr_uid = str(pr_uid)
        self.logging = logging

        if logging:
            self.trace = OrderedDict()
            self.times = []

    valid_str_typs = ('abbey',
'acres',
'allee',
'alley',
'aut',
'ave',
'av',
'bay',
'beach',
'bend',
'blvd',
'boul',
'bypass',
'byway',
'campus',
'cape',
'car',
'carref',
'ctr',
'c',
'cercle',
'chase',
'ch',
'cir',
'circt',
'close',
'common',
'conc',
'crnrs',
'cote',
'cour',
'cours',
'crt',
'cove',
'cres',
'crois',
'cross',
'cds',
'dale',
'dell',
'divers',
'downs',
'dr',
'ech',
'end',
'espl',
'estate',
'expy',
'exten',
'farm',
'field',
'forest',
'fwy',
'front',
'gdns',
'gate',
'glade',
'glen',
'green',
'grnds',
'grove',
'harbr',
'heath',
'hts',
'hghlds',
'hwy',
'hill',
'hollow',
'île',
'imp',
'inlet',
'island',
'key',
'knoll',
'landng',
'lane',
'lmts',
'line',
'link',
'lkout',
'loop',
'mall',
'manor',
'maze',
'meadow',
'mews',
'montee',
'moor',
'mount',
'mtn',
'orch',
'parade',
'parc',
'pk',
'pky',
'pass',
'path',
'ptway',
'pines',
'pl',
'place',
'plat',
'plaza',
'pt',
'pointe',
'port',
'pvt',
'prom',
'quai',
'quay',
'ramp',
'rang',
'rg',
'ridge',
'rise',
'rd',
'rdpt',
'rte',
'row',
'rue',
'rle',
'run',
'sent',
'siderd',
'sq',
'st',
'subdiv',
'terr',
'tsse',
'thick',
'towers',
'tline',
'trail',
'trnabt',
'vale',
'via',
'view',
'villge',
'villas',
'vista',
'voie',
'walk',
'way',
'wharf',
'wood',
'wynd')

    @tracer
    def spec_1(self):
        def spec_1_normalize(current_field_value):
            """
            Normalizes accented characters to their ASCII equivalent
            """
            character_list = []
            for character in current_field_value:
                character_code_point = ord(character)

                if character_code_point == 198:
                    character_list.append('a')
                elif character_code_point == 189:
                    character_list.append('half')
                else:
                    character_list.append(character)

            value = ''.join(character_list)

            value = str(normalize('NFKD', value)
                            .encode('ascii',
                                    'ignore').lower(), 'utf-8')


            return value

        fields = ('srch_nme', 'srch_typ', 'srch_dir')

        for field in fields:
            current_field_value = getattr(self, field)
            if current_field_value:
                value = spec_1_normalize(current_field_value)
                setattr(self, field, value)

            
                
    @tracer
    def spec_3(self):
        """
        Remove any non-alphanumeric characters from srch_typ and
        srch_dir
        """
        for field in ('srch_typ', 'srch_dir'):
            current_field_value = getattr(self, field)
            if current_field_value:
                regular_expression = re.compile(r'[^a-z\d]')
                value = regular_expression.sub('', current_field_value)
                if current_field_value != value:
                    setattr(self, field, value)
    @tracer
    def spec_3b_mod(self):
        """
        Remove "no." when it precedes a number. This is so that later on, it doesn't get misinterpreted as a direction.
        This is not in default RASK.
        """
        current_field_value = self.srch_nme
        pattern = re.compile("no\. (?=\d)")
        if pattern.search(current_field_value):
            value = current_field_value.replace("no. ","") 
        else:
            value = current_field_value
                
        if current_field_value != value:
            self.srch_nme = value
            
    @tracer
    def spec_3c_mod(self):
        """
        Replace hyphens with spaces rather than empty strings as in spec6 - especially important for Quebec City addresses like Cinq-Mars and Pape-Paul-VI.
        This is not in default RASK.
        """
        current_field_value = self.srch_nme
        #if (self.pr_uid == 24) or self.pr_uid == '24':
       
        temp = current_field_value.replace("-"," ") 
        value = re.sub(' +', ' ', temp)
        #else:
        #    value = current_field_value
        if current_field_value != value:
            self.srch_nme = value

    @tracer
    def spec_4(self):
        """
        Replace, with a single space, everything from srch_nme inside
        of brackets, as long as it does not remove everything from
        srch_nme.

        Examples:
        (this will (get) removed) yep
        (this will not get removed
        (this will not get removed)
        """
        current_field_value = self.srch_nme
        if current_field_value:
            if '(' and ')' in current_field_value:
                regular_expression = re.compile(r'\((.*)\)')
                value = regular_expression.sub('', current_field_value)
                if value.replace(' ', ''):
                    if current_field_value != value:
                        self.srch_nme = value

    @tracer
    def spec_6(self):
        """
        Remove any non-alphanumeric characters from srch_name
        """
        current_field_value = self.srch_nme
        character_list = []
        apostrophes = (34, 96, 124, 180, 145, 146, 147, 148, 166)
        for character in current_field_value:
            character_code_point = ord(character)

            if character_code_point in apostrophes:
                character_list.append("'")
            else:
                character_list.append(character)

        regular_expression = re.compile(r"[^a-z\d ']")
        value = regular_expression.sub('', ''.join(character_list))

        if current_field_value != value:
            self.srch_nme = value

    @tracer
    def spec_7_1(self):
        """
        Replace multiple single quotes with one single quote
        """
        current_field_value = self.srch_nme
        if "'" in current_field_value:
            regular_expression = re.compile(r"('{2,})'")
            value = regular_expression.sub("'", current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_7_2(self):
        """
        If srch_nme contains a single quote at the end of a word, and
        the next word is s, remove all spaces between the single quote and the
        s
        """
        current_field_value = self.srch_nme
        if "'" in current_field_value:
            regular_expression = re.compile(r"(?<=\w| )*' *(?=s(?![a-z\d']))")
            value = regular_expression.sub("'", current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_7_3(self):
        """
        If any word in srch_nme begins with a single quote, and the
        previous word is d, l, or o, then remove the space between the two
        """
        current_field_value = self.srch_nme
        if not current_field_value:
            return
        if "'" in current_field_value:
            regular_expression = re.compile(
                r"(?<=(?<![a-z\d'])(d|l|o)(?![a-z\d'])) *'")
            value = regular_expression.sub("'", current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_8(self):
        """
        Remove all interior blanks from srch_dir
        """
        current_field_value = self.srch_dir
        if current_field_value:
            value = current_field_value.replace(' ', '')
            if current_field_value != value:
                self.srch_dir = value

    @tracer
    def spec_9(self):
        """
        Remove all interior blanks from srch_typ
        """
        current_field_value = self.srch_typ
        if current_field_value:
            value = current_field_value.replace(' ', '')
            if current_field_value != value:
                self.srch_typ = value

    @tracer
    def spec_10(self):
        """
        From srch_nme, replace the following words
        """
        current_field_value = self.srch_nme

        regular_expression = re.compile(
            r"(?<![a-z\d'])(et|and|the|of|to|an)(?![a-z\d'])")
        value = regular_expression.sub('', current_field_value)
        if value:
            if current_field_value != value:
                self.srch_nme = value

    def find_me(self, string, max_words=4):
        length = len(string)  # The number of words in our string
        combinations = []

        for word_set_size in range(max_words, 0, -1):
            if word_set_size == 1:
                for word in string:
                    if word not in combinations:
                        combinations.append(word)
            else:
                for index, y in enumerate(range(word_set_size, length + 1)):
                    value = ' '.join(string[index:y])
                    if value not in combinations:
                        combinations.append(value)

        return tuple(combinations)

    def replace_domains_function(self, field, domain_values, max_words=2,
                                 exceptions=()):
        """
        An example for the replacements that this function would do
            "NORTHERN","NORD","NORTH"	=> "N"
            "EASTERN","EST","EAST"	=> "E"
            "SOUTHERN","SUD","SOUTH"	=> "S"
            "WESTERN","OUEST","WEST","O"	=> "W"
            "NORDOUEST","NORTHWESTERN","NORTHWEST","NO","NORDO",
            "NORTHW"	=> "NW"
            "NORDEST","NORTHEASTERN","NORTHEAST","NORDE","NORTHE"	=> "NE"
            "SUDEST","SOUTHEASTERN","SOUTHEAST","SUDE","SOUTHE"	=> "SE"
            "SUDOUEST","SOUTHWESTERN",SOUTHWEST","SO","SUDO","SOUTHW"	=> "SW"
        """
        current_field_value = getattr(self, field)
        if not current_field_value:
            return
        """
        Find all possible sequential combinations for a given value. This is
        dependent on the given domain values.

        For example, given specification 32.2 (number replacement):
         - The maximum words in a domain is four words:
           (QUATRE VINGT DIX NEUVIEME)
         - Given the string "THERE ARE FOUR QUATRE VINGT", the find_me
         function will return the following:
            1. THERE ARE FOUR QUATRE
            2. ARE FOUR QUATRE VINGT
            3. THERE ARE FOUR
            4. ARE FOUR QUATRE
            5. FOUR QUATRE VINGT
            6. THERE ARE
            7. ARE FOUR
            8. FOUR QUATRE
            9. QUATRE VINGT
            10. ALL 1 word combinations
        - We then iterate through the valid domain values, and see if any of
        the combinations match. If they do, they are replaced in the order
        listed above
        """
        current_field_value_split = current_field_value.split()
        current_field_value_split = self.find_me(current_field_value_split,
                                                 max_words=max_words)

        all_domain_values = []
        check = []
        for index, word_combinations in enumerate(current_field_value_split):
            for domain_value in domain_values:
                if index == 0:
                    all_domain_values.extend(domain_value[1])
                """
                If a word combination is inside of a domain value, then append
                to check to replace later. Given the example previously
                mentioned, QUATRE VINGT would intersect the domain value
                QUATRE VINGT, and will then be turned into 80
                """
                if (word_combinations in domain_value[1] and
                        word_combinations not in exceptions):
                    check.append((domain_value[0], word_combinations))

        if check:
            check = sorted(check, key=lambda x: all_domain_values.index(x[1]))

        if check:
            replacements_history = []
            value = current_field_value
            for domain_value in check:
                domain_value_shortform = domain_value[0]
                domain_value_longform = domain_value[1]

                # TODO: Refactor
                if replacements_history:
                    regular_expression_string = r"(?<![a-z\d'])%s(?![a-z\d'])"
                    for replacement in replacements_history:
                        regular_expression = re.compile(
                            regular_expression_string % replacement[1])
                        domain_value_longform = regular_expression.sub(
                            replacement[0], domain_value_longform)
                """
                Perform a simple check on the current field value so we do not
                waste unnecessary resources.

                Given the example mentioned, the first replacement would be
                QUATRE VINGT DIX NEUVIEME, which would get turned to 99.

                We still have the one word combinations eg. QUATRE, VINGT, DIX,
                NEUVIEME. So, we do a simple check and see if any of these
                combinations are on the current value. They won't be since
                QUATRE VINGT DIX NEUVIEME would have been replaced to 99
                """
                if domain_value_longform in value:
                    regular_expression_string = r"(?<![a-z\d'])%s(?![a-z\d'])"
                    regular_expression = re.compile(
                        regular_expression_string % domain_value_longform)
                    value_replaced = regular_expression.sub(
                        domain_value_shortform,
                        value)
                    if value_replaced != value:
                        replacements_history.append(domain_value)
                        value = value_replaced

            if current_field_value != value:
                setattr(self, field, value)

    @tracer
    def spec_11(self):
        """
        If the following words on the right are found anywhere in
        srch_nme, replace with the words on the left
        """
        spec_11_domain_values = \
            (('o', ("'o'",)), ('l', ("'l'",)), ('d', ("'d'",)),
             ('valley', ('vly',)),
             ('upper', ('upr',)), ('dr s', ('sdr',)), ('river', ('riv',)),
             ('prince', ('pr',)), ('portage', ('portg',)), ('dr n', ('ndr',)),
             ('lower', ('lwr',)), ('lake', ('lk',)), ('golden', ('gldn',)),
             ('creek', ('ck',)), ('div', ('division', 'divisional', 'divn')),
             ('stn', ('station', 'sta')), ('cty', ('county', 'cnty', 'comte')),
             ('twp', ('township', 'twnshp', 'twsp')),
             ('reg', ('regional', 'rgnl', 'region')),
             ('mun', ('municipal', 'munic', 'municipality', 'municipalite')),
             ('old', ('0ld',)),
             ('saint', ('sainte', 'ste', 'saintes', 'saints', 'stes', 'sts',
                        'saitn')),
             ('ft', ('fort',)))
        self.replace_domains_function(field='srch_nme',
                                      domain_values=spec_11_domain_values,
                                      max_words=1)


    # TODO: Find out if the definition of word means number as well
    @tracer
    def spec_15_1(self):
        """
        If any word in srch_nme starts with a single quote, then
        remove the quote
        """
        current_field_value = self.srch_nme
        if "'" in current_field_value:
            regular_expression = re.compile(r"(?<![a-z\d'])'(?=[a-z\d ]*)")
            value = regular_expression.sub('', current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_15_2(self):
        """
        While any word in srch_nme ends in 's, remove the 's
        """
        current_field_value = self.srch_nme
        if "'s" in current_field_value:
            regular_expression = re.compile(r"('s)(?![a-z\d'])(?<=\w)")
            value = []
            # Split words by space
            words = self.srch_nme.split()
            # Iterate through every word, check if they end with 'S
            for word in words:
                if word.endswith("'s"):
                    # Do it recursively until there is no more at the end
                    while word.endswith("'s"):
                        word = regular_expression.sub("", word)
                    value.append(word)
                else:
                    value.append(word)

            value = ' '.join(value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_15_3(self):
        """
        Remove all single quotes from srch_nme, unless it is preceded
        by l, d, or o
        """
        current_field_value = self.srch_nme
        if "'" in current_field_value:
            regular_expression = re.compile(r"(?<!d|l|o)'")
            value = regular_expression.sub('', current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    # TODO: refactor
    @tracer
    def spec_18(self):
        """
        If any of l', o', or d' begin a word in srch_nme, if the
        next character is not a space, add a space
        """
        current_field_value = self.srch_nme
        if "'" in current_field_value:
            regular_expression = re.compile(
                r"(?! )(?<=(?!<[a-z\d'])(l'|o'|d'))")
            value = regular_expression.sub(' ', current_field_value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_20(self):
        """
        Patterns like 13 th, 2 nd are compressed into 1 word
        """
        current_field_value = self.srch_nme
        value = current_field_value

        # Check to see if there are any numbers
        regular_expression = re.compile(r'[\d]')

        if regular_expression.search(current_field_value):
            regular_expression = re.compile(
                r"(?<=[\d]) (?=(iere|ieme|ere|eme|ier|ime|e|re|er)(?![a-z\d']))")
            value = regular_expression.sub('', value)

            # Ends with 11, 12, or 13 and next word is th
            regular_expression = re.compile(
                r"(?<=11|12|13) (?=th(?![a-z\d']))")
            value = regular_expression.sub('', value)

            # Number ends with a 2 and next word is nd
            regular_expression = re.compile(r"(?<=2) (?=nd(?![a-z\d']))")
            value = regular_expression.sub('', value)

            # Number ends with 4, 5, 6, 7, 8, 9, 0 and next word is th
            regular_expression = re.compile(
                r"(?<=4|5|6|7|8|9|0) (?=th(?![a-z\d']))")
            value = regular_expression.sub('', value)

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_21(self):
        """
        For all words in srch_nme that start with a number followed
        by a sequence of characters, remove the following characters:

        ('iere', 'ieme', 'ere', 'eme', 'ier', 'er', 're', 'e', 'th', 'st',
        'nd', 'rd', 'ime')

        """
        current_field_value = self.srch_nme

        # Check to see if there are any numbers
        regular_expression = re.compile(r'[\d]')

        if regular_expression.search(current_field_value):
            to_replace = ('iere', 'ieme', 'ere', 'eme', 'ier', 'er', 're',
                          'e', 'th', 'st',
                          'nd', 'rd', 'ime')

            regular_expression_string = '|'.join(to_replace)
            regular_expression = re.compile(r"(?<=[\d])(%s)(?![a-z\d'])" %
                                            regular_expression_string)
            value = regular_expression.sub('', current_field_value)
            if current_field_value != value:
                self.srch_nme = value



    # TODO: Refactor
    @tracer
    def spec_25(self):
        """
        Drop the final s, when not final double ss
        """
        current_field_value = self.srch_nme
        if 'S' in current_field_value:
            value = current_field_value

            regular_expression = re.compile(
                r"(?<=[^\d' ][^\d' ][^s\d' ])(s)(?![a-z\d'])")
            value = regular_expression.sub('', value)

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_26(self):
        """
        Replace spelled out numbers (right) to with their corresponding
        numbers (left)
        """
        spec_26_domain_values = (
                                 ('9000', ('neuf mille', 'nine thousand')),
                                 ('8000', ('huit mille', 'eight thousand')),
                                 ('7000', ('sept mille', 'seven thousand')),
                                 ('6000', ('six mille', 'six thousand')),
                                 ('5000', ('cinq mille', 'five thousand')),
                                 ('4000', ('quatre mille', 'four thousand')), (
                                     '3000', ('trois mille', 'three thousand',
                                              'troi mille')),
                                 ('2000', ('deux mille', 'two thousand')), (
                                     '1000', (
                                         'un mille', 'one thousand',
                                         'one thousandth',
                                         'thousandth', 'thousand', 'mille')),
                                ('1100', (
                                     'eleven hundred', )),
                                 ('900', (
                                     'neuf cents', 'neuf cent',
                                     'nine hundred')), ('800', (
            'huit cents', 'huit cent', 'eight hundred')), ('700', (
            'sept cents', 'sept cent', 'seven hundred')), ('600', (
            'six cents', 'six cent', 'six hundred')), ('500', (
            'cinq cents', 'cinq cent', 'five hundred')), ('400', (
            'quatre cents', 'quatre cent', 'four hundred')), ('300', (
            'trois cents', 'troi cents', 'trois cent', 'troi cent',
            'three hundred')), ('200',
                                ('deux cents', 'deux cent', 'two hundred')),
                                 ('100', (
                                     'un centieme', 'un cent', 'one hundred',
                                     'one hundredth', 'hundredth', 'hundred',
                                     'centieme', 'cent')), ('99', (
            'quatre vingt dix neuvieme', 'quatre vingt dix neuf',
            'ninety ninth',
            'ninety nineth', 'ninety nine')), ('98', (
            'quatre vingt dix huitieme', 'quatre vingt dix huit',
            'ninety eighth',
            'ninety eight')), ('97', (
            'quatre vingt dix septieme', 'quatre vingt dix sept',
            'ninety seventh',
            'ninety seven')), ('96', (
            'quatre vingt seizieme', 'quatre vingt seize', 'ninety sixth',
            'ninety six')), ('95', (
            'quatre vingt quinzieme', 'quatre vingt quinze', 'ninety fifth',
            'ninety five')), ('94', (
            'quatre vingt quatorzieme', 'quatre vingt quatorze',
            'ninety fourth',
            'ninety four')), ('93', (
            'quatre vingt treizieme', 'quatre vingt treize', 'ninety third',
            'ninety three')), ('92', (
            'quatre vingt douzieme', 'quatre vingt douze', 'ninety second',
            'ninety two')), ('91', (
            'quatre vingt onzieme', 'quatre vingt onze', 'ninety first',
            'ninety one')), ('90', (
            'quatre vingt dixieme', 'quatre vingt dix', 'ninetieth',
            'ninety')), (
                                     '89', (
                                         'quatre vingt neuvieme',
                                         'quatre vingt neuf',
                                         'eighty ninth', 'eighty nineth',
                                         'eighty nine')), ('88', (
            'quatre vingt huitieme', 'quatre vingt huit', 'eighty eighth',
            'eighty eight')), ('87', (
            'quatre vingt septieme', 'quatre vingt sept', 'eighty seventh',
            'eighty seven')), ('86', (
            'quatre vingt sixieme', 'quatre vingt six', 'eighty six',
            'eighty sixth')), ('85', (
            'quatre vingt cinq', 'quatre vingt cinquieme', 'eighty fifth',
            'eighty five')), ('84', (
            'quatre vingt quatre', 'quatre vingt quatrieme', 'eighty fourth',
            'eighty four')), ('83', (
            'quatre vingt troisieme', 'quatre vingt troizieme',
            'quatre vingt trois', 'quatre vingt troi', 'eighty three',
            'eighty third')), ('82', (
            'quatre vingt deuxieme', 'quatre vingt deux', 'eighty two',
            'eighty second')), ('81', (
            'quatre vingt une', 'quatre vingt unieme', 'quatre vingt un',
            'eighty first', 'eighty one')), ('80', (
            'quatre vingtieme', 'quatre vingt', 'eighty', 'eightieth')),
                                 ('79', (
                                     'soixante dix neuvieme',
                                     'soixante dix neuf', 'seventy ninth',
                                     'seventy nineth', 'seventy nine')),
                                 ('78', (
                                     'soixante dix huitieme',
                                     'soixante dix huit', 'seventy eight',
                                     'seventy eighth')), ('77', (
            'soixante dix septieme', 'soixante dix sept', 'seventy seven',
            'seventy seventh')), ('76', (
            'soixante seize', 'soixante seizieme', 'seventy six',
            'seventy sixth')), ('75', (
            'soixante quinzieme', 'soixante quinze', 'seventy fifth',
            'seventy five')), ('74', (
            'soixante quatorzieme', 'soixante quatorze', 'seventy fourth',
            'seventy fouth')), ('73', (
            'soixante treizieme', 'soixante treize', 'seventy third',
            'seventy three')), ('72', (
            'soixante douzieme', 'soixante douze', 'seventy second',
            'seventy two')), ('71', (
            'soixante onzieme', 'soixante onze', 'seventy first',
            'seventy one')),
                                 ('70', (
                                     'soixante dixieme', 'seventieth',
                                     'seventy',
                                     'soixante dix')), ('69', (
            'soixante neuvieme', 'soixante neuf', 'sixty ninth',
            'sixty nineth',
            'sixty nine')), ('68', (
            'soixante huitieme', 'soixante huit', 'sixty eighth',
            'sixty eight')),
                                 ('67', ('soixante sept', 'soixante septieme',
                                         'sixty seventh', 'sixty seven')), (
                                     '66', ('soixante sixieme', 'soixante six',
                                            'sixty sixth', 'sixty six')),
                                 ('65', (
                                     'soixante cinquieme', 'soixante cinq',
                                     'sixty five', 'sixty fifth')), (
                                     '64', (
                                         'soixante quatrieme',
                                         'soixante quatre',
                                         'sixty fourth', 'sixty four')),
                                 ('63', (
                                     'soixante troizieme',
                                     'soixante troisieme', 'soixante trois',
                                     'soixante troi', 'sixty third',
                                     'sixty three')), ('62', (
            'soixante deuxieme', 'soixante deux', 'sixty two',
            'sixty second')), (
                                     '61', ('soixante unieme', 'soixante une',
                                            'soixante un', 'sixty one',
                                            'sixty first')), ('60', (
            'soixantieme', 'soixante', 'sixtieth', 'sixty')), ('59', (
            'cinquante neuvieme', 'cinquante neuf', 'fifty ninth',
            'fifty nineth',
            'fifty nine')), ('58', (
            'cinquante huit', 'cinquante huitieme', 'fifty eight',
            'fifty eighth')), ('57', (
            'cinquante septieme', 'cinquante sept', 'fifty seven',
            'fifty seventh')), ('56', (
            'cinquante six', 'cinquante sixieme', 'fifty six', 'fifty sixth')),
                                 (
                                     '55', (
                                         'cinquante cinq',
                                         'cinquante cinquieme',
                                         'fifty five', 'fifty fifth')),
                                 ('54', (
                                     'cinquante quatrieme', 'cinquante quatre',
                                     'fifty four',
                                     'fifty fourth')), ('53', (
            'cinquante troisieme', 'cinquante troizieme', 'cinquante trois',
            'cinquante troi', 'fifty three', 'fifty third')), ('52', (
            'cinquante deuxieme', 'cinquante deux', 'fifty two',
            'fifty second')),
                                 ('51', ('cinquante une', 'cinquante unieme',
                                         'cinquante un', 'fifty one',
                                         'fifty first')), ('50', (
            'cinquantiem', 'cinquante', 'fifty', 'fiftieth')), ('49', (
            'quarante neuvieme', 'quarante neuf', 'forty ninth',
            'forty nineth',
            'forty nine')), ('48', (
            'quarante huit', 'quarante huitieme', 'forty eight',
            'forty eighth')),
                                 ('47', ('quarante sept', 'quarante septieme',
                                         'forty seven', 'forty seventh')), (
                                     '46', ('quarante six', 'quarante sixieme',
                                            'forty six', 'forty sixth')),
                                 ('45', (
                                     'quarante cinq', 'quarante cinquieme',
                                     'forty five', 'forty fifth')), (
                                     '44', (
                                         'quarante quatre',
                                         'quarante quatrieme',
                                         'forty four', 'forty fourth')),
                                 ('43', (
                                     'quarante troizieme', 'quarante troi',
                                     'quarante troisieme',
                                     'quarante trois', 'forty three',
                                     'forty third')), ('42', (
            'quarante deuxieme', 'quarante deux', 'forty two',
            'forty second')), (
                                     '41', ('quarante une', 'quarante un',
                                            'quarante unieme', 'forty one',
                                            'forty first')), ('40', (
            'quarantieme', 'quarante', 'forty', 'fortieth')), ('39', (
            'trente neuvieme', 'trente neuf', 'thirty ninth', 'thirty nineth',
            'thirty nine')), ('38', (
            'trente huitieme', 'trente huit', 'thirty eight',
            'thirty eighth')), (
                                     '37', ('trente septieme', 'trente sept',
                                            'thirty seven', 'thirty seventh')),
                                 (
                                     '36', (
                                         'trente sixieme', 'trente six',
                                         'thirty six',
                                         'thirty sixth')), ('35', (
            'trente cinquieme', 'trente cinq', 'thirty five', 'thirty fifth')),
                                 (
                                     '34',
                                     ('trente quatrieme', 'trente quatre',
                                      'thirty four', 'thirty fourth')), (
                                     '33', ('trente troizieme', 'trente troi',
                                            'trente troisieme', 'trente trois',
                                            'thirty three', 'thirty third')), (
                                     '32', ('trente deuxieme', 'trente deux',
                                            'thirty two', 'thirty second')),
                                 ('31',
                                  (
                                      'trente une',
                                      'trente un',
                                      'trente unieme',
                                      'thirty one',
                                      'thirty first')),
                                 ('30', (
                                     'xxx', 'trentieme', 'trente', 'thirtieth',
                                     'thirty')), ('29', (
            'vingt neuvieme', 'vingt neuf', 'twenty ninth', 'twenty nineth',
            'twenty nine', 'xxiv')), ('28', (
            'vingt huitieme', 'vingt huit', 'twenty eighth', 'twenty eight',
            'xxviii')), ('27', (
            'vingt septieme', 'vingt sept', 'twenty seventh', 'twenty seven',
            'xxvii')), ('26', (
            'vingt sixieme', 'vingt six', 'twenty sixth', 'twenty six',
            'xxvi')), (
                                     '25', ('vingt cinquieme', 'vingt cinq',
                                            'twenty fifth', 'twenty five',
                                            'xxv')),
                                 ('24', ('vingt quatrieme', 'vingt quatre',
                                         'twenty fourth', 'twenty four',
                                         'xxiv')), ('23', (
            'vingt trois', 'vingt troi', 'vingt troisieme', 'vingt troizieme',
            'twenty third', 'twenty three', 'xxiii')), ('22', (
            'vingt deuxieme', 'vingt deux', 'twenty second', 'twenty two',
            'xxii')), ('21', (
            'vingt unieme', 'vingt un', 'vingt une', 'twenty first',
            'twenty one',
            'xxi')), ('20',
                      ('xx', 'twenty', 'twentieth', 'vingtieme', 'vingt')), (
                                     '19', (
                                         'dix neuf', 'dix neuvieme', 'xix',
                                         'nineteen',
                                         'nineteenth')), ('18', (
            'dix huitieme', 'dix huit', 'xviii', 'eighteen', 'eighteenth')),
                                 ('17',
                                  (
                                      'dix septieme',
                                      'dix sept',
                                      'xvii',
                                      'seventeen',
                                      'seventeenth')),
                                 ('16', (
                                     'xvi', 'sixteen', 'sixteenth', 'seizieme',
                                     'seize')), ('15', (
            'xv', 'fifteenth', 'fifteen', 'quinzieme', 'quinze')), ('14', (
            'xiv', 'fourteenth', 'fourteen', 'quatorzieme', 'quatorze')),
                                 ('13', (
                                     'xiii', 'thirteenth', 'thirteen',
                                     'treizieme', 'treize')), ('12', (
            'xii', 'twelfth', 'twelve', 'douzieme', 'douze')), ('11', (
            'xi', 'eleventh', 'eleven', 'onzieme', 'onze')),
                                 ('10', ('tenth', 'ten', 'dixieme', 'dix')), (
                                     '9', (
                                         'ix', 'ninth', 'nineth', 'nine',
                                         'neuvieme',
                                         'neuf')), ('8', (
            'viii', 'eighth', 'eight', 'huitieme', 'huit')), ('7', (
            'vii', 'seventh', 'seven', 'septieme', 'sept')),
                                 ('6', ('vi', 'sixth', 'six', 'sixieme')),
                                 ('5', ('fifth', 'five', 'cinquieme', 'cinq')),
                                 ('4', (
                                     'iv', 'iiii', 'fourth', 'four',
                                     'quatrieme',
                                     'quatre')), ('3', (
            'iii', 'three', 'third', 'trois', 'troi', 'troisieme',
            'troizieme')), (
                                     '2',
                                     ('ii', 'second', 'two', 'deuxieme',
                                      'deux')),
                                 (
                                     '1',
                                     ('one', 'first', 'unieme', 'un', 'une')))
        self.replace_domains_function(field='srch_nme',
                                      domain_values=spec_26_domain_values,
                                      max_words=4)

        spec_26_domain_values_extra = (
            ('1', ('premiere', 'premier')),
        )
        if self.pr_uid in ('13', '24'):
            self.replace_domains_function(field='srch_nme',
                                          domain_values=spec_26_domain_values_extra,
                                          max_words=1)



    @tracer
    def spec_28(self):
        """
        If first word in srch_nme is st and srch_nme contains
        more than one word, replace first word with saint
        """
        current_field_value = self.srch_nme

        if current_field_value.startswith('st'):
            if len(current_field_value.split()) > 1:
                regular_expression = re.compile(r"^(st)(?![a-z\d'])")
                value = regular_expression.sub('saint', current_field_value)

                if current_field_value != value:
                    self.srch_nme = value

    @tracer
    def spec_29(self):
        """
        For srch_nme and srch_typ, the following words on the
        right will be replaced with the ones on the left.

        Note: srch_nme has various exceptions where they should not
        be replaced. There is also a province dependent replacement (in QC)
        
        for purpose of ODA, this was stripped down to only standardise some standard street types
        """
        if self.pr_uid == '24':
            rang = ('rang',('rng'))
            avenue = ('av', ('ave', 'avenue', 'aveneue'))
            boulevard = ('boul', ('boul', 'boule', 'boulev', 'boulevard','boulv', 'bv', 'blv', 'bvd'))
            centre =  ('c', ('ctr', 'center', 'centre', ))
            
            place = ('place', ('pl', 'plc'))
            point = ('pointe', ('pnt', 'poin', 'point','pt'))

        else:
            rang = ('rg',('rng','range'))

            avenue = ('ave', ('ave', 'avenue', 'aveneue'))
            boulevard =  ('blvd', ('boul', 'boule', 'boulev', 'boulevard','boulv', 'bv', 'blv', 'bvd'))
            centre = ('ctr', ('c', 'center', 'centre'))
            place = ('pl', ('place', 'plc'))
            point = ('pt', ('pnt', 'poin', 'point', 'pointe'))

        spec_29_domain_values = \
            ( avenue, boulevard, centre, point, place,
            ('abbey', ('abby',)),                         
            #('acres', ('ac', 'acer', 'acers', ')),
            ('alley', ('ally',)),
            ('aut', ('autoroute',)),
         
            #('bay', ('ba', )),
            ('beach', ('bch',)), 
            #('bend', ('bn', 'bnd')),
           
            ('bypass', ('bp', 'byps', 'byp')), 
            ('byway', ('bwy', 'by way')),
            #('campus', ('campu',)), 
            ('car', ('carre',)),
             ('carref', ('carrefour', 'carefour')),
            ('cercle', ('ce', 'cer', 'cerc', 'cercl', 'cercle',  'crcl', 'crcle',)), 
          
            ('ch', ('chemin','chem')),
            ('cir', ( 'ci', 'circ', 'circl','circle', 'cirl', 'cirle', 'cirs', 'crcl', 'crcle', 'cri', 'cricl')),
            ('circt', ('circuit', 'crct')),
            ('close', ('cl', 'clove', 'cls', 'cs')),
            ('common', (('cm', 'cmmn', 'cmn', 'com', 'comm', 'commn', 'commo')),
            ('conc', ('cn', 'con', 'concesion', 'concess', 'concession',
                                   'concessions')),
            ('crnrs', ('corner', 'corners', 'crnr')),
            ('crt', ('court', 'crts', 'ct')),
            ('cove', ('cv',)),
            ('cres', ('cr', 'cre', 'crees', 'cresc', 'crescent', 'crest',
                             'cresant', 'crescant', 'cresent','crese',
                            'cresl', 'crs', 'crscnt',)),
            ('crois',('croi', 'crois', 'croissant',)),
            ('cross', ('crossing', 'crss', 'cx')),
            ('cds', ('cd', 'cul de sac', 'cul sac', 'culsac')),
            ('divers', ('diver', 'diversion')),
            ('downs', ('down', 'ds', 'dwn', 'dwns')),
            ('dr', ('dirve', 'driev','drive', )),
            ('ech', ('echangeur','échangeur',)),
            ('espl', ('esplanade',)),
            ('estate', ('estat', 'estates', 'ests')),
            ('expy', ('expr way', 'express', 'expr', 'express way', 'expressway',
                            'expresway', 'expw', 'xy')),
            ('exten', ('ext', 'extention', 'extension', 'extn')),
            ('fwy', ('free way', 'freeway', 'frwy')),
            ('front', ('frnt',)),
            ('gdns', ('garde', 'garden', 'gardens', 'gdn', 'gn', 'grdn', 'grdns',
                            'gs')),
            ('gate', ('gt',)),
            ('glen', ('gln',)),
            ('green', ('gr', 'grn')),
            ('grnds', ('gnd', 'gnds', 'grnd', 'ground', 'grounds')),
            ('grove', ('gv')),
            ('harbr', ('har', 'harbor', 'harbour', 'harbur', 'hb', 'hbr', 'hrbr')),
            ('hts', ('heigh', 'height', 'heights', 'hght', 'hghts', 'hgt', 'hgts',
                            'high', 'higt', 'higts', 'ht', 'htg', 'htgs', )), 
            ('hghlds', ('hghld', 'high land', 'high lands', 'highland',
                                 'highlands',
                                 'highlnd', 'highlnds')),
            ('hwy', ('hgwy', 'highwa', 'highway',
                            'hi way', 'hiway', 'hy', 'hyw',)),
            ('hill', ('hills', 'hl')),
             ('hollow', ('holow', 'hw')),
            ('imp', ('impasse',)),
            ('island', ('isl', 'islands', 'isld', 'islds', )),
            ('knoll', ('knl',)),
            ('landng', ('landg', 'landi', 'landing', 'ld', 'ldg', 'ldn', 'ldng', 'lg',
                            'lndg', 'lndng')),
            ('lane', ('lanet', 'llane', 'ln', )),
            ('lmts', ('limit', 'limits', 'lmt')),
            ('line', ('li',)),
            ('link', ('lk', 'lnk')),
            ('lkout', ('look out', 'lookout')),
            ('loop', ('lp',)),
            ('manor', ('man', 'mnr', 'mor', 'mr')),
            ('meadow', ('mdw', 'mdws')),
            ('mews', ('me', 'mew')),
            ('montee', ('mo', 'mte', 'mtee',)),
            ('mtn', ( 'montagne', 'montain', 'montaine', 'mountain',)),
            ('mount',('mt',)),
            ('orch', ('orchard',)),
            ('pk',('park',)),
            ('pkwy', ('prk way', 'park way', 'parkw', 'parkway', 'paw', 'pkw',
                            'pkway',
                            'pky', 'prkw', 'prkwa', 'prkway', 'prkwy', 'prky', 'py')),
            ('pass',('pass', 'passage', 'ps', 'psg')),
            ('path', ('pth',)),
            ('ptway', ('path way', 'pathway', 'pathwy', 'pthway', 'pthwy')),
            ('pines', ('pine',)),

            'plat', ('plateau',)),
            ('plaza', ('plz', 'plza', 'pz')),
            ('pvt', ('priv', 'private', 'prive', 'prt', 'prvt', 'prvte')),
            ('prom', ('promenade',)),
            ('rg', ('range',)),
            ('ridge', ( 'rdg', 'rdge', 'ri', 'ridg', 'rigde')),
            ('rise', ('rs',)),
            ('rd',('road',)),
            ('rdpt', ('rd pt', 'rond point', 'rond pt', 'rondpoint', 'rondpt')),
            ('rte',('route',)),
            ('rle',('ruelle',)),
            ('sent', ('sentier',)),
            ('siderd', (
                'sd rd', 'sd ro', 'sd road', 'side rd', 'side road', 'side ro',
                'sdrd', 'sdro', 'sdroad', 'sidero', 'sideroad', 'sr')),
            ('sq', ('sqr', 'sqre', 'squar', 'square', 'squre')),
            ('st', ('str', 'stree', 'street')),
            ('subdiv', ('sub div', 'subd', 'subdivision')),
            ('terr', ('tc', 'tce','terrace',
                            'terrc',)),
            ('tsse',('terrasse',)),
            ('thick', ('thicket',)),
            ('towers', ('tower', 'twr', 'twrs')),
            ('tline', ('townl', 'town line', 'townline')),
            ('trail', ('taril', 'tl', 'tr', 'tri', 'trial', 'trl')),
            ('trnabt', ('turn about', 'turnabout')),
            ('view', ('vw',)),
            ('villge', ('village',)),
            ('villas', ('villa',)),
            ('walk', ('wk',)),
            ('wharf', ('wf',)),
            ('wood', ('wd', 'woods')),
            ('wynd', ('winde',)),
            rang
        )

        exceptions = ('ac', 'bf', 'bp', 'cw', 'gres', 'cx', 'cx', 'c', 'ds',
                      'ev', 'xy', 'hw', 'i', 'lg', 'lw', 'lk', 'lp', 'ps',
                      'rs', 'ry', 'sd', 'sr', 'sp', 'tw', 'tk', 'tail', 'tu')

        self.replace_domains_function(field='srch_nme',
                                      domain_values=spec_29_domain_values,
                                      max_words=3, exceptions=exceptions)

        self.replace_domains_function(field='srch_typ',
                                      domain_values=spec_29_domain_values,
                                      max_words=3)



    @tracer
    def spec_31(self):
        """
        Standardize spelled out street directions in srch_nme
        """
        spec_31_domain_values = (
            ('nw', ('nordouest', 'northwestern', 'northwest', 'north w', 'no',
                    'north west', 'n w', 'n o', 'nord ouest')),
            ('ne', (
                'nordest', 'northeastern', 'northeast', 'north e',
                'north east',
                'n e', 'nord est')), ('se', (
                'sudest', 'southeastern', 'southeast', 'south e', 'south east',
                's e', 'sud est')), ('sw', (
                'sudouest', 'southwestern', 'southwest', 'south w', 'so',
                'south west', 's w', 's o', 'sud ouest')), ('sw', ('sud o',)),
            ('nw', ('nord o',)), ('north', ('northern', 'nord')),
            ('east', ('eastern', 'est')), ('south', ('southern', 'sud')),
            ('west', ('western', 'ouest')))

        self.replace_domains_function(field='srch_nme',
                                      domain_values=spec_31_domain_values,
                                      max_words=2)

    # TODO: Refactor
    @tracer
    def spec_32(self):
        """
        If more than one word in srch_nme and word = str_typ, remove
        word from srch_nme
        """
        valid_str_typs = self.valid_str_typs

        split_words = self.srch_nme.split()
        field_length = len(split_words)

        to_remove = []
        if field_length > 1:
            if self.pr_uid != '24':
                for index, word in enumerate(split_words[-1::-1]):
                    if len(to_remove) != field_length - 1:
                        if word == self.srch_typ:
                            to_skip = field_length - 1 - index
                            to_remove.append(to_skip)

                        if (word in valid_str_typs and
                                not self.srch_typ):
                            self.srch_typ = word
                            to_skip = field_length - 1 - index
                            to_remove.append(to_skip)
            elif self.pr_uid == '24':
                for index, word in enumerate(split_words):
                    if len(to_remove) != field_length - 1:
                        if word == self.srch_typ:
                            to_remove.append(index)
                        elif (word in valid_str_typs and
                              not self.srch_typ):
                            self.srch_typ = word
                            to_remove.append(index)

        value = []

        for index, word in enumerate(split_words):
            if index not in to_remove:
                value.append(word)

        self.srch_nme = ' '.join(value)

    @tracer
    def spec_33(self):
        """
        Replace all words saint win srch_nme with st
        """
        current_field_value = self.srch_nme

        if 'saint' in current_field_value:
            regular_expression = re.compile(
                r"(?<![a-z\d'])saint(?![a-z\d'])")
            value = regular_expression.sub('st', current_field_value)

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_35(self):
        """
        The words defined on the right should be replaced with the ones on the
        left for srch_dir
        """
        spec_35_domain_values = (('n', ('northern', 'nord', 'north')),
                                 ('e', ('eastern', 'est', 'east')),
                                 ('s', ('southern', 'sud', 'south')),
                                 ('w', ('western', 'ouest', 'west', 'o')), (
                                     'nw', (
                                         'nordouest', 'northwestern', 'northwest',
                                         'no', 'nordo', 'northw')), ('ne', (
            'nordest', 'northeastern', 'northeast', 'norde', 'northe')), ('se', (
            'sudest', 'southeastern', 'southeast', 'sude', 'southe')), ('sw', (
            'sudouest', 'southwestern', 'southwest', 'so', 'sudo', 'southw')))

        if self.srch_dir:
            self.replace_domains_function(field='srch_dir',
                                          domain_values=spec_35_domain_values,
                                          max_words=1)

    @tracer
    def spec_36(self):
        """
        Replace cardinal direction from srch_nme if it is already
        part of srch_dir
        This has been modified to account for street names like "West Side Road,"
        where the street name is "West Side" and the type is "Road"
        """
        split_words = self.srch_nme.split()
        
        field_length = len(split_words)
        to_remove = []
        skip=False

        #there are a fair number of street names in NS of the form 'O 3' or 'S 10' that can be misclassified
        #as directions. So first we make sure if the province is NS, that those streets aren't processed.
        
        if (self.pr_uid=='12'):
            pattern1=re.compile('^[a-z] \d+$')
            pattern2=re.compile('^\d+ [a-z]$')
            if (re.match(pattern1, self.srch_nme)) or (re.match(pattern2, self.srch_nme)):
                pass
        else:
            if len(split_words) > 1:

                if split_words[0] in ('north', 'n','south','s','east','e','west','w') and split_words[1]=='side':
                    temp_list=split_words[-1:1:-1]

                else:
                    temp_list=split_words[-1::-1]

                for index, word in enumerate(temp_list):
                    to_skip = field_length - 1 - index

                    if len(to_remove) + 1 != field_length:
                        if word in (
                                'north', 'n') and self.srch_dir in (
                                '', 'n'):
                            self.srch_dir = 'n'
                            to_remove.append(to_skip)

                        if word in (
                                'south', 's') and self.srch_dir in (
                                '', 's'):
                            self.srch_dir = 's'
                            to_remove.append(to_skip)

                        if word in ('east', 'e') and self.srch_dir in (
                                '', 'e'):
                            self.srch_dir = 'e'
                            to_remove.append(to_skip)

                        if word in (
                                'west', 'w',
                                'o') and self.srch_dir in (
                                '', 'w'):
                            self.srch_dir = 'w'
                            to_remove.append(to_skip)

                        if word in ('north', 'n', 'south', 's') and \
                            self.srch_dir in ('e', 'w'):
                            value = word[0] + self.srch_dir
                            self.srch_dir = value
                            to_remove.append(to_skip)

                        if word in ('e', 'w') and self.srch_dir in (
                                'n', 's'):
                            value = self.srch_dir + word[0]
                            self.srch_dir = value
                            to_remove.append(to_skip)

                        if word == 'o' and self.srch_dir in ('n', 's'):
                            value = self.srch_dir + 'w'
                            self.srch_dir = value
                            to_remove.append(to_skip)

                        if word == 'nw' and self.srch_dir in (
                                '', 'nw'):
                            self.srch_dir = 'nw'
                            to_remove.append(to_skip)

                        if word == 'ne' and self.srch_dir in (
                                '', 'ne'):
                            self.srch_dir = 'ne'
                            to_remove.append(to_skip)

                        if word == 'sw' and self.srch_dir in (
                                '', 'sw'):
                            self.srch_dir = 'sw'
                            to_remove.append(to_skip)

                        if word == 'se' and self.srch_dir in (
                                '', 'se'):
                            self.srch_dir = 'se'
                            to_remove.append(to_skip)

        value = []
        for index, word in enumerate(split_words):
            if index not in to_remove:
                value.append(word)

        self.srch_nme = ' '.join(value)

    # TODO: Find out. What does this get applied to? Everything?
   



   
    @tracer
    def spec_41(self):
        """
        Create srch_nme_no_articles and assign it srch_nme
        """
        self.srch_nme_no_articles = self.srch_nme



    @tracer
    def spec_43(self):
        """
        If srch_nme_no_articles is empty, populate it with
        the srch_nme value
        """
        if not self.srch_nme_no_articles:
            self.srch_nme_no_articles = self.srch_nme

    @tracer
    def spec_44(self):
        """
        Remove all single quotes from srch_nme and
        srch_nme_no_articles
        """
        if "'" in self.srch_nme:
            self.srch_nme = self.srch_nme.replace("'", "")
            self.srch_nme_no_articles = \
                self.srch_nme_no_articles.replace("'", "")


    def run(self):
        """
        Runs all specification functions
        """
        functions = ( 'spec_1', 'spec_3', 'spec_3b_mod','spec_3c_mod', 'spec_4',
                    'spec_6', 'spec_7_1', 'spec_7_2', 'spec_7_3', 'spec_8', 
                     'spec_9', 'spec_10', 'spec_11',  'spec_15_1', 'spec_15_2',
                     'spec_15_3', 'spec_18', 'spec_20', 'spec_21', 
                     'spec_25', 'spec_26',  'spec_28', 'spec_29',
                     'spec_31', 'spec_32', 'spec_33', 'spec_35',
                     'spec_36', 'spec_41',
                     'spec_43', 'spec_44')

        for function in functions:
            getattr(self, function)()

        if self.srch_nme_no_articles:
            self.srch_nme_no_articles = self.srch_nme_no_articles

    def culprit(self):
        """
        Returns a list of function names and the time it took to execute each
        (in milliseconds), in ascending order
        """
        return sorted(self.times, key=lambda x: x[1], reverse=True)

    def __str__(self):
        return 'srch_nme=%s\n' \
               'srch_typ=%s\n' \
               'srch_dir=%s\n' \
               'pr_uid=%s' % (self.srch_nme_no_articles, self.srch_typ, self.srch_dir,
                              self.pr_uid)


