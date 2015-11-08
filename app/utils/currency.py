def cents_to_str(cents):
    if cents >= 0:
        return '${0:.2f}'.format(cents/100.0)
    else:
        return '-${0:.2f}'.format(abs(cents)/100.0)