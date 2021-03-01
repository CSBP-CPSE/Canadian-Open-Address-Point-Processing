from functools import wraps
import time
import re


def tracer(f):
    @wraps(f)
    def wrapper(self, *args, **kwds):
        logging = self.logging
        if logging:
            start_time = time.time()

        # Replace multiple spaces with a single one
        regular_expression = re.compile(r'( {2,})')

        fields = ('srch_nme', 'srch_typ',
                  'srch_dir', 'srch_nme_no_articles')
        current_values = {}
        for field in fields:
            current_values[field] = getattr(self, field, None)

        result = f(self, *args, **kwds)

        if logging:
            changes = {}

        for field in fields:
            value = getattr(self, field, None)
            if current_values[field] != value:
                value = regular_expression.sub(' ', value).strip()
                setattr(self, field, value)
                if logging:
                    changes[field] = value

        if logging:
            function_name = f.__name__
            if changes:
                self.trace[function_name] = changes

            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            if elapsed_time:
                self.times.append([function_name, elapsed_time])

        return result

    return wrapper
