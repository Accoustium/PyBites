NAMES = ['arnold schwarzenegger', 'alec baldwin', 'bob belderbos',
         'julian sequeira', 'sandra bullock', 'keanu reeves',
         'julbob pybites', 'bob belderbos', 'julian sequeira',
         'al pacino', 'brad pitt', 'matt damon', 'brad pitt']


def dedup_and_title_case_names(names):
    """Should return a list of title cased names,
       each name appears only once"""
    names = set(names)

    names = [
        f"{name.split(' ')[0].capitalize()} {name.split(' ')[1].capitalize()}"
        for name in names
    ]

    return names


def sort_by_surname_desc(names):
    """Returns names list sorted desc by surname"""
    names = dedup_and_title_case_names(names)
    last_names = [name.split(" ")[1] for name in names]
    last_names = sorted(last_names, reverse=True)
    for index, last in enumerate(last_names):
        for name in names:
            if name.find(last) != -1:
                last_names[index] = name

    return last_names


def shortest_first_name(names):
    """Returns the shortest first name (str).
       You can assume there is only one shortest name.
    """
    names = dedup_and_title_case_names(names)
    shortest = [100, 50]
    for index, name in enumerate(names):
        if len(name.split(" ")[0]) < shortest[1]:
            shortest = [index, len(name.split(" ")[0])]

    return names[shortest[0]].split(" ")[0]
