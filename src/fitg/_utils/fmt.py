

def toCTimeFormat(simpleFormat):

    # a little care is needed here to avoid clashes between formats
    answer = simpleFormat
    answer = answer.replace('DDDD', '%A')
    answer = answer.replace('DDD', '%a')
    answer = answer.replace('DD', '%d')
    answer = answer.replace('D', '%d')      # was %e

    answer = answer.replace('YYYY', '%Y')
    answer = answer.replace('YY', '%y')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('mm', '%M')
    answer = answer.replace('m', '%-M')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('ss', '%S')
    answer = answer.replace('s', '%<single-digit-second>')

    answer = answer.replace('MMMM', '%B')                           # Month as locale’s full name
    answer = answer.replace('MMM', '%b')                            # Month as locale’s abbreviated name
    answer = answer.replace('MM', '%m')                             # Month as a zero-padded decimal number
    answer = answer.replace('M', '%<single-digit-month>')
    answer = answer.replace('%%<single-digit-month>', '%M')
    answer = answer.replace('%-%<single-digit-month>', '%-M')

    answer = answer.replace('hh', '%H')                             # 0 padded 12 hour
    answer = answer.replace('h', '%-H')
    answer = answer.replace('HH', '%I')                             # 0 padded 24 hour
    answer = answer.replace('H', '%-I')
    answer = answer.replace('%%-I', '%H')
    answer = answer.replace('%-%-I', '%-H')

    answer = answer.replace('TT', '%p')                             # Locale’s equivalent of either AM or PM

    answer = answer.replace('city', '%<city>')
    answer = answer.replace('z/z', '%<IANA>')
    answer = answer.replace('z', '%Z')                              # Time zone name (empty string if the object is naive)
    return answer