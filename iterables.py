def take_while_inclusive(p, xs):
    for x in xs:
        if not p(x):
            yield x
            break

        yield x
