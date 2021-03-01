# -*- coding: utf-8 -*-
from collections import OrderedDict
from rask_cask.helpers import tracer
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
        self.pr_uid = pr_uid
        self.logging = logging

        if logging:
            self.trace = OrderedDict()
            self.times = []

    valid_str_typs = ('abbey',
'acres',
'allée',
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
'côte',
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
'éch',
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
'montée',
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

            if python_version == 3:
                value = str(normalize('NFKD', value)
                            .encode('ascii',
                                    'ignore').lower(), 'utf-8')
            elif python_version == 2:
                value = normalize('NFKD',
                                  unicode(value)).encode('ascii',
                                                         'ignore').lower()

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
        Replaces accented characters with their ascii equivalent
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
        value = regular_expression.sub(' ', ''.join(character_list))

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

    @tracer
#    def spec_14(self):
#        """
#        If any words in srch_nme start with mac, replace with mc
#        """
#        current_field_value = self.srch_nme

#        if 'mac' in current_field_value:
#            regular_expression = re.compile(r"(?<![a-z\d'])mac")
#            value = regular_expression.sub('mc', current_field_value)
#            if current_field_value != value:
#                self.srch_nme = value

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

    @tracer
#    def spec_22_1(self):
#        """
#        Remove any leading zeros from any type of word.#

#        0 => 0
#        0A => 0
#        10001 => 10001
#        00 => 0
#        000 => 0
#        exit001 099 => exit001 99
#        """
#        current_field_value = self.srch_nme

#        if '0' in current_field_value:
#            regular_expression = re.compile(r"(?<![a-z\d'])0+(?=[\d]+)")
#            value = regular_expression.sub('', current_field_value)
#            if current_field_value != value:
#                self.srch_nme = value

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
        spec_26_domain_values = (('9000', ('neuf mille', 'nine thousand')),
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
        if self.pr_uid in (13, 24):
            self.replace_domains_function(field='srch_nme',
                                          domain_values=spec_26_domain_values_extra,
                                          max_words=1)

    @tracer
#    def spec_27(self):
#        """
#        While srch_nme contains the word no or nos, and the next word
#        is a numeral or a numeral followed by a single letter
#        """
#        current_field_value = self.srch_nme
#        if 'no' in current_field_value:
#            value = current_field_value

#            regular_expression = re.compile(
#                r"(?<![a-z\d'])(no|nos)(?![a-z\d']) (?=(?<![a-z\d'])\d+[a-z]?(?![a-z\d']))")

#            while regular_expression.search(value):
#                value = regular_expression.sub('', value)

#            if current_field_value != value:
#                self.srch_nme = value

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
        if self.pr_uid == 24:
            special_replacement_1 = 'rang'
            avenue = ('av', ('ave', 'avenue', 'aveneue'))
            boulevard = ('boul', ('boul', 'boule', 'boulev', 'boulevard','boulv', 'bv', 'blv', 'bvd'))
            centre =  ('c', ('ctr', 'center', 'centre', ))
                        
            point = ('pointe', ('pnt', 'poin', 'point','pt'))

        else:
            avenue = ('ave', ('ave', 'avenue', 'aveneue'))
            boulevard =  ('blvd', ('boul', 'boule', 'boulev', 'boulevard','boulv', 'bv', 'blv', 'bvd'))
            centre = ('ctr', ('c', 'center', 'centre'))
            point = ('pt', ('pnt', 'poin', 'point', 'pointe'))

        spec_29_domain_values = \
            ( avenue, boulevard, centre, point,
            ('abbey', ('abby',)),                         
            ('acres', ('ac', 'acer', 'acers', 'acre')),
            ('allée',('allee',)), #FR
            ('alley', ('al',  'ally',)),
            ('aut', ('autoroute',)),
         
            ('bay', ('ba', 'baie', )),
            ('beach', ('bch',)), 
            ('bend', ('bn', 'bnd')),
           
            ('bypass', ('bp', 'byps', 'byp')), 
            ('byway', ('bwy', 'by way')),
            ('campus', ('campu',)), 
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
            ('éch', ('echangeur','échangeur',)),
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
            ('montée', ('mo', 'mte', 'mtee','montee',)),
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
            ('pl', ('place', 'plc')),
            ('place', ('pl', 'plc')), #FR
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
            ('wynd', ('winde',))
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
    def spec_29_5(self):
        """
        Move side and cross from srch_nme to srch_typ
        under certain circumstances
        """
        current_srch_nme_value = self.srch_nme
        current_srch_typ_value = self.srch_typ

        split_words = current_srch_nme_value.split()
        if len(split_words) > 1:
            if split_words[-1] == 'side':
                if current_srch_typ_value == 'rd':
                    self.srch_nme = ' '.join(split_words[0:-1])
                    self.srch_typ = 'siderd'
            elif split_words[-1] == 'cross':
                if current_srch_typ_value == 'rd':
                    self.srch_nme = ' '.join(split_words[0:-1])
                    self.srch_typ = 'crssrd'

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
            if self.pr_uid != 24:
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
            elif self.pr_uid == 24:
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
        """
        split_words = self.srch_nme.split()
        field_length = len(split_words)
        to_remove = []

        if len(split_words) > 1:
            for index, word in enumerate(split_words[-1::-1]):
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
    def spec_37(self):
        """
        In srch_nme, for any two digits separated by a blank,
        insert the word and between them
        """
        current_field_value = self.srch_nme

        # Check to see if there are any numbers
        regular_expression = re.compile(r'[\d]')

        if regular_expression.search(current_field_value):
            regular_expression = re.compile(r"(?<=\d)+ +(?=\d)")
            value = regular_expression.sub(' and ', self.srch_nme)

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_38(self):
        """
        Change the order of srch_nme given certain conditions
        """
        current_field_value = self.srch_nme
        # Number or a number plus a single letter
        reg_exp = re.compile(r"([\d]|[\d][a-z])(?![a-z\d'])")

        if reg_exp.search(current_field_value):
            split_words = current_field_value.split()
            # number_words = len(split_words)
            road_types = ('conc', 'div', 'line', 'base', 'baseline', 'rg',
                          'ft', 'mun', 'reg', 'twp', 'cty')

            words_dict = {}
            for index, word in enumerate(split_words):
                words_dict['word_%s' % (index + 1)] = word

            word_1 = words_dict.get('word_1', '')
            word_2 = words_dict.get('word_2', '')
            word_3 = words_dict.get('word_3', '')
            word_4 = words_dict.get('word_4', '')
            word_5 = words_dict.get('word_5', '')

            # If first word is a number or a number plus a single letter
            # TODO: Refactor
            if reg_exp.search(word_1):
                if (word_2 in road_types and word_3 not in road_types and not
                reg_exp.search(word_3)):
                    remaining = ' '.join(split_words[2:])
                    self.srch_nme = '%s %s %s' % (word_2, word_1,
                                                  remaining)
                elif (word_2 and word_3 in road_types and
                      word_4 not in road_types and not reg_exp.search(
                            word_4)):
                    remaining = ' '.join(split_words[3:])
                    self.srch_nme = '%s %s %s %s' % (word_2, word_3,
                                                     word_1, remaining)
                elif (word_2 == 'and' and word_4 in road_types
                      and word_5 not in road_types and reg_exp.search(word_3)
                      and not reg_exp.search(word_5)):
                    remaining = ' '.join(split_words[4:])
                    self.srch_nme = '%s %s %s %s %s' % (word_4, word_1,
                                                        word_2, word_3,
                                                        remaining)
                elif (word_2 == 'and' and reg_exp.search(word_3) and
                      word_4 in road_types and word_5 in road_types):
                    remaining = ' '.join(split_words[5:])
                    self.srch_nme = '%s %s %s %s %s %s' % (
                        word_4, word_5,
                        word_1, word_2,
                        word_3,
                        remaining)

    @tracer
    def spec_38_2(self):
        """
        In srch_nme, for any two digits separated by a blank,
        insert the word and between them
        """
        current_field_value = self.srch_nme

        # Check to see if there are any numbers
        regular_expression = re.compile(r'[\d]')

        if regular_expression.search(current_field_value):
            regular_expression = re.compile(r"(?<=\d)+ +(?=\d)")
            value = regular_expression.sub(' and ', current_field_value)

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_41(self):
        """
        Create srch_nme_no_articles and assign it srch_nme
        """
        self.srch_nme_no_articles = self.srch_nme

    @tracer
    def spec_42(self):
        """
        Remove the following consecutive word pairs from
        srch_nme_no_articles
        """
        current_field_value = self.srch_nme_no_articles

        split_words = current_field_value.split()
        split_words = self.find_me(split_words, max_words=2)

        domain_values = ("a l'", 'a la', 'de', 'des', 'du', 'la', 'le', 'les',
                         'aux', 'au', "l'", "o'", "d'")

        check = []
        for word_combinations in split_words:
            if word_combinations in domain_values:
                check.append(word_combinations)

        if check:
            value = current_field_value
            for value_to_replace in check:
                regular_expression_string = r"(?<![a-z\d'])%s(?![a-z\d'])" % value_to_replace
                regular_expression = re.compile(regular_expression_string)
                value = regular_expression.sub('', value)

            if current_field_value != value:
                self.srch_nme_no_articles = value

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

    def spec_45(self):
        """Remove all spaces from srch_nme and srch_nme_no_articles"""
        self.srch_nme = self.srch_nme.replace(" ", "")
        self.srch_nme_no_articles = self.srch_nme_no_articles.replace(" ", "")

    def run(self):
        """
        Runs all specification functions
        """
        functions = ( 'spec_1', 'spec_4', 'spec_6', 'spec_7_1',
                     'spec_7_2', 'spec_7_3', 'spec_8', 'spec_9', 'spec_10',
                     'spec_11',  'spec_15_1', 'spec_15_2',
                     'spec_15_3', 'spec_18', 'spec_20', 'spec_21', 
                     'spec_25', 'spec_26',  'spec_28', 'spec_29',
                     'spec_29_5', 'spec_31', 'spec_32', 'spec_33', 'spec_35',
                     'spec_36', 'spec_37', 'spec_38', 'spec_38_2', 'spec_41',
                     'spec_42', 'spec_43', 'spec_44')#, 'spec_45')

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


class CASK(RASK):
    def __init__(self, csd_name, pr_uid, logging=False):
        self.srch_nme = csd_name
        self.srch_typ = ''
        self.srch_dir = ''
        self.pr_uid = pr_uid
        self.logging = logging

        if logging:
            self.trace = OrderedDict()
            self.times = []

    # A FUNNY RULE. If city's, the 's gets separated
    '''
    If city's of toronto => torontos
    If citys of toronto => citytoronto
    '''

    @tracer
    def rad_cask(self):
        current_field_value = self.srch_nme
        if "CITY'S" in current_field_value:
            value = current_field_value
            regular_expression = re.compile(
                "(?<![a-z0-9'])(city's)(?![a-z0-9'])")
            value = regular_expression.sub('city s', value)
            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_3_cask(self):
        """
        Replace all occurrences of the words city or city of
        """
        current_field_value = self.srch_nme
        value = current_field_value

        replace = 'city of|city'
        regular_expression = re.compile(
            r"(?<![a-z0-9'])(%s)(?![a-z0-9'])" % replace)

        value = regular_expression.sub('', value)
        if current_field_value != value:
            self.srch_nme = value

    @tracer
    def spec_4_cask(self):
        """
        This is a place holder. The tracer decorator already removes multiple
        spaces with a single blank
        """
        pass

    @tracer
    def spec_5_cask(self):
        current_field_value = self.srch_nme
        value = current_field_value

        replace = 'sprg|sprgs|sprng|sprngs'
        regular_expression = re.compile(
            r"(?<![a-z0-9'])(%s)(?![a-z0-9'])" % replace)

        value = regular_expression.sub('springs', value)
        if current_field_value != value:
            self.srch_nme = value

    @tracer
    def spec_7_cask(self):
        cask_rules = \
            {10   : (
                ('benoits cove', ('benoit cv',)), ('carbonear', ('carb',)),
                ('coleys point', ("coley'spoint",)),
                ('cornerbrook', ('crbrk',)), ('coxs cove', ('cox cv',)),
                ('creston south', ('crestonsouth',)),
                ('fox harbour', ('foxharbour',)),
                ('georgestown cb', ('georgetown',)),
                ('happy valley goose bay', ('happy valley goose b',)),
                ('mount carmel', ('mountcarmel',)),
                ('new harbour tb', ('newharbour',)),
                ('northern arm', ('northernarm',)),
                ('portugal cove st philips', ('portugal cove', 'portugalcove',
                                              'stphillips',
                                              'portugal cv st phili',
                                              'portugal cove st phi')),
                ('south dildo', ('dildo south',)),
                ("st john's", ('st j', 'stjohns')),
                ('stephenville', ('steph',)),
                ('stephenville crossing', ('steph x',))),
                11: (('borden carleton', ('borden',)),
                     ('charlottetown', ('charlottetown pei',)),
                     ('covehead road', ('covehead',)),
                     ('summerside', ('summerside pei',)),
                     ('winsloe', ('winslow',))),
                12: (('cape breton',
                      ('c b', 'cap bret', 'cp bret', 'c bret', 'cbrm')),
                     ('cross roads country harbour',
                      ('cross roads country',)),
                     ('dartmouth', ('dart',)),
                     ('east stewiacke', ('stewiacke e',)),
                     ('halifax',
                      ('hal',
                       'halfax',
                       'hfx',
                       'halifax regional municipality',
                       'hrm')),
                     ('head of st margarets bay', ('head st margarets',)),
                     ('le goulet', ('legoulet',)),
                     ('marion bridge', ('marion brg',)),
                     ('mount uniacke', ('mountuniacke',)),
                     ('prospect', ('prospect road',)),
                     ('st margaret village', ('st margarets',)),
                     ('upper nine mile river', ('upr nine mile river',)),
                     ('upper rawdon', ('u rawdon',))),
                13: (('chamberlain settlement', ('chamberlain settleme',)),
                     (
                         'eel river bar first nation',
                         ('eel river bar first',)),
                     ('elsipogtog first nation', ('elsipogtog first nat',)),
                     ('florenceville bristol', ('florenceville bristo',)),
                     ('fredericton', ('fred',)),
                     ('grand falls', ('grand falls nb',)),
                     ('grand sault grand falls',
                      ('grand sault grand f',
                       'grand sault grand fa',
                       'grand falls grand sa',
                       'grand falls grand sault')),
                     ('haut riviere du portage', ('haut riviere du port',)),
                     ('kingsclear first nation', ('kingsclear first nat',)),
                     ('madawaska maliseet first nation',
                      ('mmfn', 'madawaska maliseet f')),
                     ('moncton', ('monc', 'mnc', 'mctn')),
                     ('notre dame des erables',
                      ('notre dame des erabl,', 'notre dame erab')),
                     ('red bank reserve', ('red bank indian rese',)),
                     ('saint francois de madawaska',
                      ('st francois de ma',
                       'st francois mad',
                       'st francois madawas')),
                     ('saint john', ('st j', 'saintjohn')),
                     ('sainte anne de madawaska',
                      ('st anne de madaw',
                       'st anne de madawask',
                       'st anne de mad',
                       'st anne mad',
                       'st anne madawas',
                       'st ann madawask')),
                     ('sainte marie saint raphael', ('st marie st r',)),
                     ('st andrews', ('stand',)),
                     ('st joseph de madawaska', ('st joseph mad',)),
                     ('village st laurent', ('village st lauren',)),
                     ('woodstock', ('woodstock nb',)),
                     ('youngs cove', ('youngs cove road',))),
                24: (('acton vale', ('act vl',)),
                     ('ancienne lorette', ('ancienne lo',)),
                     ('ange gardien', ('ange gard', 'liange grdn')),
                     ('anse saint jean', ('anse st jn',)),
                     ('baie sainte catherine', ('baie sainte catherin',)),
                     ('becancour', ('becan', 'ville becancour')),
                     ('begin', ('canton begin',)),
                     ('berthierville', ('berth',)),
                     ('blue sea lake', ('baue sea lake',)),
                     ('bolton east', ('bolton e',)),
                     ('bolton ouest', ('bolton o',)),
                     ('bonne esperance', ('bonne esperance 379',)),
                     ('boucherville', ('bchvl',)),
                     ('breakeyville', ('breakeyvl',)),
                     ('brompton', ('bromp',)),
                     ('brossard', ('bross',)),
                     ('camp valcartier', ('base vlcr',)),
                     ('canton de granby', ('canton de gnby',)),
                     ('canton de hatley', ('canton de hatly',)),
                     ('cap de la madeleine', ('cap de la mad', 'cap mad')),
                     ('cascapedia saint jules', ('cascapedia saint jul',)),
                     ('chateauguay', ('chtgy',)),
                     ('chicoutimi', ('chtmi',)),
                     ('coleraine station', ('coleraine stn',)),
                     ('cote saint luc', ('csl', 'c luc')),
                     ('degelis', ('ville degelis',)),
                     ('des ruisseaux', ('ds ruiss',)),
                     ('dolbeau mistassini', ('dolb mistsn',)),
                     ('dollard des ormeaux', ('dol des ormea',)),
                     ('dorval', ('drvl',)),
                     ('drummondville', ('dmvl', 'drumvl', 'drmvl')),
                     ('duvernay', ('duvrny',)),
                     ('east broughton', ('e brotn',)),
                     ('east hereford', ('e hrfd',)),
                     ('fossambault sur le lac', ('fossambault sur le l',)),
                     ('fugereville', ('fugerev',)),
                     ('gatineau', ('gat',)),
                     ('granby', ('grnby', 'gby', 'gnby')),
                     ("grand'mere", ('gmere',)),
                     ('grenville', ('gren',)),
                     ('grenville sur la rouge', ('grenville sur la rou',)),
                     ('harrington', ('harringtn hbr',)),
                     ('hebertville station', ('hebrtvlle stn',)),
                     ('hull', ('ottawa hull',)),
                     ('ile bizard', ('ile biz',)),
                     ('ile du grand calumet', ('ile grd calum',)),
                     ('jonquiere', ('jonq',)),
                     ("l'ascension de notre seigneur",
                      ('lascension de notre s',)),
                     ("l'ile perrot", ('ile per',)),
                     ('la macaza', ('lamacaza',)),
                     ('la malbaie', ('lamalbaie',)),
                     ('la minerve', ('la minrv',)),
                     ('la motte', ('lamotte',)),
                     ('la pocatiere', ('la pocatier', 'la poc')),
                     ('lac a la tortue', ('lacalatortue',)),
                     ('lac bouchette', ('l boucht',)),
                     ('lac brome', ('ville lac brome',)),
                     ('lac des iles', ('lcdsiles', 'lc ds iles')),
                     ('lac drolet', ('lac drt',)),
                     ('lac la peche', ('la peche',)),
                     ('lachenaie', ('lchnaie',)),
                     ('lachine', ('lchn',)),
                     ('laval', ('lav', 'lvl', 'lanal')),
                     ('lebel sur quevillon', ('lebel quevill',)),
                     ('levis', ('lev',)),
                     ('longue rive', ('longuerive',)),
                     ('longueuil', ('long',)),
                     ('lots renverses', ('lotsrenv',)),
                     ('mandeville', ('mandvl',)),
                     ('metabetchouan lac a la croix',
                      ('metabetchouan lac cr',)),
                     ('mistissini', ('mistiss',)),
                     ('mont laurier', ('mtlaur',)),
                     ('mont lebel', ('mlebel',)),
                     ('mont saint gregoire',
                      ('mt st grgoire', 'mont st greg')),
                     ('mont saint hilaire', ('mt st hilr', 'st hilaire')),
                     ('montreal', ('mon', 'mntl', 'mtl', 'mtrl', 'montral')),
                     ('montreal est', ('mtl e',)),
                     ('montreal nord', ('mtl n',)),
                     ('morin heights', ('mor hts',)),
                     ('notre dame de ham', ('nd de ham',)),
                     ("notre dame de l'ile perrot",
                      ('nd ile perrot', 'n d ile per')),
                     ('notre dame de la merci',
                      ('notre dame de la mer', 'nd la merci')),
                     ('notre dame de la paix', ('nd la paix',)),
                     ('notre dame de montauban', ('notre dame de montau',)),
                     ('notre dame de pontmain', ('nd pontmain',)),
                     ('notre dame de stanbridge',
                      ('notre dame stanbr', 'nd stanbridge')),
                     ('notre dame des bois', ('nd des bois',)),
                     ('notre dame des laurentides',
                      ('notre dame des laure',)),
                     ('notre dame des monts', ('nd des monts',)),
                     ('notre dame des prairies',
                      ('notre dame des prair', 'nd prairies', 'n d p')),
                     ('notre dame du lac', ('nd du lac',)),
                     ('notre dame du laus', ('nd du laus',)),
                     ('notre dame du mont carmel',
                      ('nd mont crmel', 'notre dame du mont c')),
                     ('notre dame du nord', ('nd du nord',)),
                     ('ouje bougoumou', ('ouje boug',)),
                     ('peribonka', ('peribk',)),
                     ('pointe calumet', ('pt cal',)),
                     ('pointe claire', ('pt clr',)),
                     ('quebec',
                      ('que', 'qu bec', 'qubel', 'quber', 'gubec',
                       'zoebec')),
                     ('rapid lake', ('l rap',)),
                     ('repentigny', ('repent', 'rptgny', 'reptgny')),
                     ('rimouski', ('rmski',)),
                     ('riviere bleue', ('riv bleue',)),
                     ('riviere heva', ('r heva',)),
                     ('riviere trois pistoles', ('riviere trois pistol',)),
                     ('rock forest', ('rk forest',)),
                     ('rouyn noranda', ('rouynnor', 'rouyn nor', 'ryn nor')),
                     ('roxton pond', ('r pond',)),
                     ('sacre coeur saguenay', ('sc saguenay',)),
                     ('sacre couer de jesus', ('s c de jesus',)),
                     ('saguenay', ('sagny', 'sgny', 'sag')),
                     ("saint adolphe d'howard", ("st a d'how",)),
                     ('saint adrien', ('st adr',)),
                     ('saint aime des lacs', ('staimedeslacs',)),
                     ("saint alexandre d'iberville",
                      ("st alexandre d'iberv",)),
                     ('saint alexandre de kamouraska',
                      ('st alexandre de kamour',
                       'st alexandre kamourask')),
                     ('saint alexis de montcalm',
                      ('st alexis de montcal', 'st alxis m')),
                     ('saint alphonse de caplan', ('saint alphonse de ca',)),
                     ('saint ambroise de kildare', ('st ambr de k',)),
                     ("saint andre d'argenteuil",
                      ("saint andre d'argent", "st andre d'argntl")),
                     ('saint antoine de lavaltrie',
                      ('st antoine de lavltr',)),
                     ('saint antoine de tilly', ('saint antoine de til',)),
                     ('saint antoine sur richelieu',
                      ('st antoine sur riche', 'st antoine sur ri')),
                     ('saint apollinaire', ('st apoll',)),
                     ('saint armand', ('st arm',)),
                     ('saint augustin de desmaures',
                      ('saint augustin de de',)),
                     ('saint barthelemy', ('st barth',)),
                     ('saint bernard de lacolle', ('st bernard lac',)),
                     ('saint boniface de shawinigan',
                      ('saint boniface de sh',)),
                     ('saint bruno', ('st bno',)),
                     ('saint calixte', ('st calx',)),
                     ('saint camille', ('st caml',)),
                     ('saint cesaire', ('st ces', 'stces')),
                     ('saint charles borromee',
                      ('saint charles borrom', 's c b')),
                     ('saint charles de bellechasse',
                      ('saint charles de bel',)),
                     ('saint charles de bourget',
                      ('st charles bou', 'stcharlesdebourget')),
                     ('saint charles de drummond',
                      ('st charles bellecha',
                       'st charles de drummo',
                       'st charles de drmd',
                       'saint charles de dru')),
                     ('saint charles garnier', ('st charles garnie',)),
                     ('saint charles sur richelieu',
                      ('st charles sur riche', 'st charles sur ri')),
                     ("saint christophe d'arthabaska",
                      ("saint christophe d'a",
                       "st christophe d'arth",
                       'st christophe arthab',
                       'st christophe art')),
                     ('saint cleophas de brandon', ('st cleophas br',)),
                     ('saint clotilde de horton', ('st clotilde h',)),
                     ('saint cuthbert', ('st cuth',)),
                     ("saint cyrille de l'islet", ("saint cyrille de l'i",)),
                     ('saint cyrille de wendover', ('st cyr w',)),
                     ('saint damase', ('st dam',)),
                     ('saint damien de brandon', ('st damn de b',)),
                     ('saint damien de buckland', ('saint damien de buck',)),
                     ("saint david d'yamaska", ('st david y',)),
                     ('saint denis de la bouteillerie',
                      ('st denis de la boute',)),
                     ('saint denis sur richelieu',
                      ('stdenissurrich', 'st denis sur richeli')),
                     ('saint dominique', ('stdom', 'st dom')),
                     ('saint donat de montcalm', ('saint donat de montc',)),
                     ('saint edmond de grantham',
                      ('saint edmond de gran', 'st edm gr')),
                     ('saint edmond les plaines', ('st edmond pla',)),
                     ('saint edouard de lotbiniere',
                      ('saint edouard de lot',)),
                     ('saint edouard de napierville',
                      ('st edouard de napier', 'st edouard napiervi')),
                     ('saint elphege', ('st elph',)),
                     ('saint elzear de temiscouata',
                      ('st elzear de temisco', 'st elzear temiscoua')),
                     ('saint emile de suffolk', ('st emile suffo',)),
                     ('saint etienne de beauharnois',
                      ('stetiennedebeauharno',)),
                     ('saint etienne des gres',
                      ('saint etienne des gr', 'stetiennedesgres')),
                     ('saint eugene de grantham', ('st eugene de grantha',)),
                     ('saint eustache', ('st eust',)),
                     ('saint faustin lac carre', ('stfaustlaccarre',)),
                     ('saint felix de kingsey',
                      ('st flx de kingsy', 'stflxdekingsy')),
                     ('saint felix de valois',
                      ('saint felix de valoi', 'st flx de v',
                       'st felix v')),
                     ('saint ferreol les neiges',
                      ('saint ferreol les ne', 'stferreollesneiges')),
                     ('saint francois de sales', ('saint francois de sa',)),
                     ('saint frederic', ('st fred',)),
                     ('saint fulgence', ('st fulg',)),
                     ('saint gabriel de brandon',
                      ('saint gabriel de bra', 'st gab de b')),
                     ('saint gabriel de valcartier',
                      ('saint gabriel de val', 'st gabriel valcarti')),
                     ('saint gedeon', ('st gedn', 'stgedn')),
                     ('saint gedeon de beauce', ('saint gedeon de beau',)),
                     ('saint georges de champlain',
                      ('saint georges de cha', 'st g champ')),
                     ('saint georges de windsor', ('st georges de windso',)),
                     ('saint gerard des laurentides',
                      ('st gerard des lauren',
                       'stgerdesl',
                       'st gerard laurenti')),
                     ('saint germain de grantham',
                      ('saint germain de gra', 'st germ gr')),
                     ('saint guillaume', ('st guill',)),
                     ('saint hermenegilde', ('st hermngld',)),
                     ('saint hippolyte', ('st hip',)),
                     ('saint honore de chicoutimi',
                      ('st honore de chicoutim',
                       'st honore de chicout',
                       'saint honore de chic')),
                     ('saint honore de temiscouata',
                      ('st honore de temisco', 'st honore temiscoua')),
                     ('saint hubert', ('st hub', 'st hudert', 'sthudert')),
                     ('saint hyacinthe', ('st hya', 'sthya', 'st hyc')),
                     ('saint ignace de loyola', ('st ignace loyo',)),
                     ('saint ignace de stanbridge',
                      ('st ignacedestanbridg',)),
                     ('saint isidore de laprairie',
                      ('st isidore de laprai',)),
                     ('saint jacques', ('st jacq', 'st jacques')),
                     ('saint jacques de leeds',
                      ('saint jacques de lee', 'st jac de leeds')),
                     ('saint jacques le mineur', ('st jac min',)),
                     ('saint jean baptiste', ('st j bapt',)),
                     ('saint jean de dieu', ('st jean di',)),
                     ('saint jean de matha', ('st jn de m', 'st jean ma')),
                     ('saint jean sur richelieu',
                      ('st jean sur richelie',
                       'st jean sur rich',
                       'st jean sur r',
                       'saint jean sur riche',
                       'sjsr',
                       's j s r',
                       'st jean sr',
                       'stjeansurrich',
                       'stjeansurricheliev')),
                     ('saint jerome', ('st jer', 'stjer')),
                     (
                         'saint joachim de shefford',
                         ('st joachim de sheffo',)),
                     ('saint joseph de beauce', ('saint joseph de beau',)),
                     ('saint joseph de coleraine',
                      ('st joseph de colera',
                       'st jos de col',
                       'saint joseph de cole')),
                     ('saint joseph de kamouraska',
                      ('st joseph de kamoura',)),
                     ('saint just de bretenieres', ('st just bretenier',)),
                     ('saint lambert', ('st lam',)),
                     ('saint lambert de lauzon', ('saint lambert de lau',)),
                     ('saint laurent', ('st lnt', 'st laurent')),
                     ("saint laurent ile d'orleans", ("stlrentd'orleans",)),
                     ('saint lazare', ('st laz', 'st lazare')),
                     ('saint lazare de bellechasse',
                      ('saint lazare de bell',)),
                     ('saint louis de france', ('st ls france',)),
                     ('saint marc des carrieres', ('saint marc des carri',)),
                     ('saint marc sur richelieu', ('st marc sur richelie',)),
                     ('saint marcel de richelieu', ('st marcelrich',)),
                     ('saint mathias sur richelieu',
                      ('saint mathias sur ri',)),
                     ('saint mathieu de beloeil', ('st m bel',)),
                     ('saint mathieu de rioux', ('saint mathieu de rio',)),
                     ('saint mathieu du parc',
                      ('saint mathieu du par', 'stmathieuduparc')),
                     ('saint michel des saints',
                      ('saint michel des sai', 'st mch des s')),
                     ('saint narcisse de beaurivage',
                      ('saint narcisse de be',)),
                     ('saint narcisse de rimouski',
                      ('saint narcisse de ri', 'st narcisse rimousk')),
                     ('saint nazaire de dorchester', ('st nazaire dor',)),
                     ('saint nicephore', ('st niceph', 'stniceph')),
                     ('saint nicolas', ('st nclas',)),
                     ('saint norbert', ('st nrbrt',)),
                     ("saint norbert d'arthabaska",
                      ("saint norbert d'arth", "st norbertd'arthabas")),
                     ('saint patrice de beaurivage',
                      ('saint patrice de bea', 'st patrice beauriva')),
                     ("saint paul de l'ile aux noix",
                      ('st paul i n', 'st paul ile n')),
                     ('saint philippe de neri',
                      ('st phil neri', 'stphilneri')),
                     ("saint pierre ile d'orleans",
                      ("saint pierre ile d'o",)),
                     (
                         'saint pierre les becquets',
                         ('saint pierre les bec',)),
                     ('saint prosper de dorchester',
                      ('st prosper dorchest', 'st prosper do')),
                     ('saint redempteur', ('st redem', 'stredem')),
                     ("saint roch de l'achigan", ("saint roch de d'achi",)),
                     ('saint roch de richelieu', ('st rochrich',)),
                     ('saint roch des aulnaies', ('saint roch des aulna',)),
                     ('saint romuald', ('st rom',)),
                     ('saint sauveur', ('st sauv',)),
                     ('saint simon de bagot', ('stsimbagot',)),
                     ('saint urbain premier', ('st urbain pre',)),
                     ('saint zenon', ('st zen', 'stzen')),
                     ('sainte adele', ('ste ade',)),
                     ('sainte agathe de lotbiniere',
                      ('sainte agathe de lot', 'ste agathe de lotbin')),
                     ('sainte agathe des monts', ('sainte agathe des mo',)),
                     ('sainte agathe nord', ('ste aga n',)),
                     ('sainte angele de monnoir', ('ste angele de monnoi',)),
                     ('sainte anne de beaupre',
                      ('sainte anne de beaup',
                       'sa beaupre',
                       'st anne b',
                       'steabpre')),
                     ('sainte anne de la perade', ('sainte anne de la pe',)),
                     ('sainte anne de la rochelle',
                      ('ste anne de la roche',)),
                     ('sainte anne des plaines',
                      ('sainte anne des plai', 'ste a des p')),
                     (
                         'sainte apolline de patton',
                         ('sainte apolline de p',)),
                     ('sainte beatrix', ('ste beatx',)),
                     ("sainte brigide d'iberville", ('ste brig iber',)),
                     ('sainte brigitte de laval', ('sainte brigitte de l',)),
                     ('sainte catherine',
                      ('st cather',
                       'st catherine',
                       'stecatherine',
                       'ville st catherine')),
                     ('sainte cecile de levrard',
                      ('ste cecile de levrar', 'stececiledelev')),
                     ('sainte cecile de masham', ('sainte cecile de mas',)),
                     ('sainte cecile de milton',
                      ('ste cec milton', 'stececmilton',
                       'stececiledemilton')),
                     ('sainte christine', ('st chrstn',)),
                     ('sainte clotilde de chateauguay',
                      ('st clotilde de cha',)),
                     ('sainte elisabeth', ('ste elisbth',)),
                     ("sainte emelie de l'energie",
                      ("ste emelie de d'ener", 'ste emelie de l')),
                     ('sainte genevieve', ('st genevi',)),
                     ('sainte genevieve de batiscan',
                      ('ste genevieve de bat',)),
                     ('sainte hedwidge de roberval',
                      ('ste hedwidge de robe',)),
                     ('sainte helene de breakeyville',
                      ('sainte helene de bre',
                       'ste helene de breake',
                       'stehelenedebreakeyvl',
                       'st helene breakeyvl',
                       'st helene breakeyv',
                       'st helene breakeyvill')),
                     ('sainte julienne', ('ste julnne',)),
                     ('sainte justine de newton', ('ste justine de newto',)),
                     ('sainte lucie de beauregard',
                      ('ste lucie de beaureg',)),
                     ('sainte lucie de laurentides', ('st lucie laurenti',)),
                     ('sainte madeleine', ('ste mad',)),
                     ('sainte marguerite esterel',
                      ('sainte marguerite es', 'st marguerite este')),
                     (
                         'sainte marie de blandford',
                         ('sainte marie de blan',)),
                     ('sainte marthe sur la lac',
                      ('stemarthe surle lac',
                       'stemarthesurle lac',
                       'stemarthesurlelac')),
                     ('sainte monique de nicolet',
                      ('sainte monique de ni', 'st monique nicol')),
                     ('sainte petronille', ('stepetrio', 'st petrio')),
                     ('sainte rose', ('ste rse', 'sterose')),
                     ("sainte sophie d'halifax", ('st sophie hali',)),
                     ('sainte sophie de levrard', ('sainte sophie de lev',)),
                     ('sainte therese',
                      ('ste ther',
                       'stether',
                       'st teresa',
                       'st theresa',
                       'st therese')),
                     ('salaberry de valleyfield',
                      ('salaberry de valleyf',
                       'sala de valfd',
                       'sal valleyfield',
                       'salaberrydevalleyfi')),
                     ('senneterre', ('sennet',)),
                     ('shawinigan', ('shawin', 'shaw', 'shwngn')),
                     ('sherbrooke', ('shbk', 'sher', 'sherb')),
                     ('st alexandre', ('st alex',)),
                     ('st ambroise de chicout',
                      ('st ambroise de chico', 'st ambroise chico')),
                     ('st boniface', ('st bon',)),
                     ('st dominique de bagot', ('st dominique de bago',)),
                     ('st francois', ('st frs',)),
                     ('st gabriel', ('st gab', 'stgabriel')),
                     ('st germain de kamouraska', ('st germain de kamour',)),
                     (
                         'st isidore de dorchcester',
                         ('st isidore de dorche',)),
                     ('st janvier', ('st janv',)),
                     ('st michel de napierville',
                      ('st michel de napiervil', 'st michel de napierv')),
                     ('st michel de wentworth', ('st michel de wentwor',)),
                     ('st nazaire du lac st jean',
                      ('st nazaire du lac st j',)),
                     ("st paul d'abbotsford", ("st p d'a",)),
                     ('st paul jol', ('st paul de j',)),
                     ('st pierre de la riviere du sud',
                      ('st pierre de la rivi', 'st pierre riviere')),
                     ('st regis', ('streg',)),
                     ('stanbridge east', ('stan e',)),
                     ('ste anne de la pocatiere',
                      ('ste anne de la poc', 'st anne pocat')),
                     ('ste catherine de la j cartier',
                      ('ste cath de laj cart',
                       'ste cath de la j car',
                       'st catherine j c')),
                     ('ste genev de berthier',
                      ('ste genviev de b', 'st genevieve berthier')),
                     ('ste marcelline', ('ste marclne',)),
                     ('ste marguerite de dorchester',
                      ('ste marguerite de do', 'st marguerite dorches')),
                     ('ste marguerite de lingwick',
                      ('ste marguerite de li',)),
                     (
                         'ste marguerite du lac masson',
                         ('ste marg lac mass',)),
                     (
                         'ste therese de blainville',
                         ('ste therese de blain',)),
                     ('terrasse vaudreuil', ('terr vaudreui',)),
                     ('terrebonne', ('ter bon', 'terr bon')),
                     ('thetford mines', ('thet mns',)),
                     ('thornby', ('thorne',)),
                     ('tres saint redempteur', ('tres saint redempteu',)),
                     ('tring jonction', ('tring jctn',)),
                     ('trois pistoles', ('trois pistols',)),
                     ('trois rivieres', ('3 riv', '3riv', 'trois riv')),
                     ('trois rivieres ouest',
                      ('trois rivieresuest', 'trois riv o', 't riv o')),
                     ("val d'or", ('valdior',)),
                     ('val david', ('v dav',)),
                     ('valcartier village', ('valcartier vlg',)),
                     ('varennes', ('vrns',)),
                     ('vaudreuil dorion', ('vaud dor',)),
                     ('vaudreuil sur le lac', ('vaudreuil lac',)),
                     ('victoriaville', ('victorvl', 'victvl', 'vicvl'))),
                35: (('ajax', ('ajay',)),
                     ('barrie', ('barr',)),
                     ('belleville', ('belvl', 'bellville', 'belville')),
                     ('blue mountains', ('blue moun',)),
                     ('bowmanville', ('bowman',)),
                     ('brampton', ('bram', 'bmtn', 'frampton')),
                     ('brantford', ('bran', 'btfd')),
                     ('brights grove', ('brights grv',)),
                     ('burlington', ('burl', 'burlgtn')),
                     ('caledon', ('cal', 'caldon', 'cldn', 'caldon')),
                     ('cambridge', ('camb', 'cbdg', 'cbg', 'cmbg')),
                     ('chatham', ('chat', 'chtm')),
                     ('clarington', ('clar', 'cltn')),
                     ('cornwall', ('crnwll', 'cornw', 'cwall', 'corn')),
                     ('cumberland beach', ('cumberland be',)),
                     ('delhi', ('deihl',)),
                     ('durham', ('dunham', 'durhm')),
                     ('guelph', ('glph',)),
                     ('haldimand', ('hald', 'hlmd')),
                     ('halton hills', ('hh', 'halt hls', 'hltn hls')),
                     ('hamilton', ('ham', 'hmltn', 'haml')),
                     ('hawkesbury', ('hawk',)),
                     ('iroquois falls', ('iroquois falls nt',)),
                     ('kapuskasing', ('kpsks',)),
                     ('kawartha lakes',
                      ('kwartha lakes', 'kwartha lks', 'kaw lks',
                       'kaw lakes')),
                     ('kitchener',
                      ('kit', 'kitch', 'kch', 'kichner', 'kich')),
                     ('london', ('lond', 'lon', 'ldn')),
                     ('manotick', ('manotich',)),
                     ('markham', ('mkhm', 'mark')),
                     ('mississauga',
                      ('miss',
                       'missauga',
                       'missg',
                       'mississagi',
                       'missisaugua',
                       'mississaugas')),
                     ('mount forest', ('mountforest',)),
                     ('newmarket',
                      ('new mkt',
                       'nmkt',
                       'n mkt',
                       'nw mkt',
                       'nwmkt',
                       'new market')),
                     ('niagara falls', ('niagra falls', 'n falls')),
                     ('norfolk', ('nflk', 'nor')),
                     ('north bay', ('n bay', 'nby', 'n by')),
                     ('oakville', ('oakvil', 'oakvl', 'oakv', 'okvl')),
                     ('orillia', ('oril', 'orilla')),
                     ('orleans', ('drleans',)),
                     ('oshawa', ('osh', 'oshwa')),
                     ('ottawa',
                      ('ott',
                       'ottwa',
                       'ottawa carleton',
                       'rmoc',
                       'ottawa hull',
                       'ottaw',
                       'ottowa')),
                     ('pelham fenwk', ('pelham',)),
                     ('peterborough', ('peteb',)),
                     ('pickering', ('pick', 'pickg')),
                     ('picton', ('pictou',)),
                     ('quinte west', ('qt w', 'qt west')),
                     (
                         'richmond hill',
                         ('richmond hl', 'rmd hill', 'rmd hl')),
                     ('sarnia', ('sarn',)),
                     ('sault st marie',
                      ('ssm',
                       's s m',
                       'soo',
                       'ss marie',
                       's s marie',
                       'sue st marie')),
                     ('scarborough', ('scarbord', 'scarboro')),
                     ('st catharines',
                      ('st cath',
                       'st cth',
                       'st c',
                       'st catherines',
                       'st catherine')),
                     ('stoney creek',
                      ('stoney creek ontari', 'stoneycreek ont')),
                     ('sudbury',
                      ('sudb',
                       'sudbry',
                       'sud',
                       'greater sudbury grand sudbury',
                       'greater sudbury')),
                     ('thornhill', ('thornhiii',)),
                     ('thunder bay',
                      ('thun bay', 'th bay', 't bay', 'tb', 't b')),
                     ('timmins', ('tim', 'timm', 'tmns')),
                     ('toronto',
                      ('toron',
                       'tor',
                       'to',
                       't o',
                       'gta',
                       'toront',
                       'tronto',
                       'tonoto',
                       'torontoo')),
                     ('vaughan', ('vghn', 'vaughn', 'vaughan city')),
                     ('waterloo', ('wat', 'wloo')),
                     ('welland', ('welld', 'well', 'wel')),
                     ('west lincoln wldpt', ('west lincoln',)),
                     ('whitby', ('whtby', 'whit')),
                     ('windsor', ('wind', 'win', 'winsor'))),
                46: (('brandon', ('bran', 'bdn')),
                     ('fort alexander indian reserve',
                      ('fortalexanderindianr',)),
                     ('fort garry', ('ftgry',)),
                     ('la salle', ('lasalle',)),
                     ('north kildonan', ('nkld',)),
                     ('springfield', ('spr',)),
                     ('st andrews', ('stand',)),
                     ('st boniface', ('stbon',)),
                     ('st clements', ('stclem',)),
                     ('st georges', ('stgeorges',)),
                     ('st james', ('stjas',)),
                     ('st vital', ('stvtl',)),
                     ('the pas', ('thepas',)),
                     (
                         'waywayseecappo first nation',
                         ('waywayseecapporsve',)),
                     ('west hawk lake', ('westhawklake',)),
                     ('winnipeg', ('wpg', 'winn', 'win', 'winipeg'))),
                47: (('martensville', ("mart'vile",)),
                     ('regina', ('reg', 'regina sask')),
                     ('saskatoon', ('stoon',))),
                48: (('bellevue', ('belvue',)),
                     ('black diamond', ('blk dmnd',)),
                     ('blairmore', ('blrmre',)),
                     ('calgary',
                      ('calgayr', 'caglary', 'cal', 'calg', 'cgy',
                       'calary')),
                     ('coleman', ('clmn',)),
                     ('edmonton',
                      ('edmnton',
                       'edmonotn',
                       'edmotnon',
                       'edmotton',
                       'edtn',
                       'edmn',
                       'edm',
                       'edmonto')),
                     ('fort mcmurray', ('fortmcmurray',)),
                     ('hillcrest mines', ('hllcrst mns',)),
                     ("john d'or prairie", ("jean d'or prairie",)),
                     ('la crete', ('lacrete',)),
                     ('la glace', ('laglace',)),
                     ('lethbridge', ('leth', 'lethbg', 'lethb')),
                     ('medicine hat', ('med hat',)),
                     ('red earth creek', ('red earth',)),
                     ('redcliff', ('rdclf',)),
                     ('rocky mountain house',
                      ('rocky mt hse', 'rocky mtn hse')),
                     ('siksika 146', ('siksika ir 146 ab',)),
                     ('st albert', ('st albt', 'st alb')),
                     ('strathcona county', ('strath',)),
                     ('wood buffalo',
                      ('wd buff', 'wood buff', 'wd buffalo'))),
                59: (('100 mile house', ('loo mile house',)),
                     ('abbotsford', ('abbtfd', 'abbt', 'abb')),
                     ('appledale', ('appldl',)),
                     ('bridge lake', ('bridge lk',)),
                     ('burnaby', ('bby', 'burn', 'burnby')),
                     ('central saanich', ('c saan',)),
                     ('chilliwack', ('chlwk', 'chil', 'chill')),
                     ('coquitlam', ('coq',)),
                     ('decker lake', ('deck lk',)),
                     ('dragon lake', ('dragon lk',)),
                     ('fairmont hot springs', ('fairmont ht sp',)),
                     ('gallagher lake', ('galaghr lake',)),
                     ('gillies bay', ('gils b',)),
                     ('hagensborg', ('hagen',)),
                     ('kamloops', ('kam', 'kmlps')),
                     ('kelowna', ('kel',)),
                     ('krestova', ('krestva',)),
                     ('langley', ('lang', 'langly')),
                     ('lantzville', ('lantz',)),
                     ('maple ridge', ('mpl rdg', 'mpl ridge')),
                     ('merville', ('neuville',)),
                     ('nanaimo', ('nan', 'nmo')),
                     ('new westminster',
                      ('new west', 'n west', 'new westminister')),
                     ('north saanich', ('n saan',)),
                     ('north vancouver', ('n van', 'north van')),
                     ('pender harbour', ('p hbr',)),
                     ('pender island', ('north pender island',)),
                     ('port alberni', ('pt alberni',)),
                     ('port coquitlam',
                      ('pt coquitlam', 'pt coq', 'ptcoq', 'port coq')),
                     ('prince george', ('pr george', 'pr geo')),
                     ('prince rupert', ('pr rupert', 'pr rup')),
                     ('quadra isld', ('quadra island',)),
                     ('richmond', ('richmd', 'rich', 'rmd')),
                     ('saanich', ('saan',)),
                     ('saanichton', ('sanchtn',)),
                     ('savory island', ('sav isld',)),
                     (
                         'surrey',
                         ('surr', 'surry', 'sry', 'su rry', 'surley')),
                     ('vancouver',
                      ('van', 'vcr', 'vanc', 'vancou', 'vanc bc')),
                     ('victoria', ('vic', 'victo')),
                     ('west vancouver', ('w van', 'west van')))}

        '''
        # DISABLED SINCE THEY DO AN EXACT MATCH ON THE WHOLE STRING
        self.replace_domains_function(field='srch_nme',
                                      domain_values=cask_rules[self.pr_uid],
                                      max_words=6)
        '''
        current_field_value = self.srch_nme
        value = current_field_value
        to_replace = cask_rules.get(self.pr_uid)
        if to_replace:
            for official_name, alternate_names in to_replace:
                if value in alternate_names:
                    value = official_name
                    break

            if current_field_value != value:
                self.srch_nme = value

    @tracer
    def spec_11_cask(self):
        """
        Concatenate srch_nme, srch_typ, and srch_dir
        """
        self.srch_nme = '%s%s%s' % (self.srch_nme,
                                    self.srch_typ,
                                    self.srch_dir)
        self.srch_nme_no_articles = '%s%s%s' % (
            self.srch_nme_no_articles,
            self.srch_typ,
            self.srch_dir)

    def run(self):
        """
        Runs all specification functions
        """
        functions = ('spec_1', 'spec_3','spec_6', 'rad_cask', 'spec_3_cask',
                     'spec_5_cask',
                     'spec_7_cask', 'spec_7_1', 'spec_7_2', 'spec_7_3',
                     'spec_8', 'spec_10', 'spec_11', 'spec_14', 'spec_15_1',
                     'spec_15_2', 'spec_15_3', 'spec_18', 'spec_20', 'spec_21',
                     'spec_22_1', 'spec_25', 'spec_26', 'spec_27', 'spec_28',
                     'spec_29', 'spec_29_5', 'spec_31', 'spec_32', 'spec_33',
                     'spec_35', 'spec_36', 'spec_37', 'spec_38', 'spec_38_2',
                     'spec_41', 'spec_42', 'spec_43', 'spec_44',
                     'spec_11_cask')#, 'spec_45')  we don't want spaces removed

        for function in functions:
            getattr(self, function)()

    def __str__(self):
        return '%s, pr_uid - %s' % (self.srch_nme, self.pr_uid)