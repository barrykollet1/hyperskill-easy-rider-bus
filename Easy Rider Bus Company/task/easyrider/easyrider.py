import json
import re
import time

json_str = input()

inp_list = json.loads(json_str)

stop_count = dict()

# compteur d'erreurs
err_count = dict(
    bus_id=0,
    stop_id=0,
    stop_name=0,
    next_stop=0,
    stop_type=0,
    a_time=0
)

# definition des types des champs
key_type = dict(
    bus_id=int,
    stop_id=int,
    stop_name=str,
    next_stop=int,
    stop_type=str,
    a_time=str
)

# Determiner si le champ peut etre vide ou pas
allow_empty = dict(
    bus_id=False,
    stop_id=True,
    stop_name=False,
    next_stop=True,
    stop_type=True,
    a_time=False
)

# definition des valeurs possibles pour chaque champ: None = any value
value_choice = dict(
    bus_id=None,
    stop_id=None,
    stop_name=None,
    next_stop=None,
    stop_type=['', 'S', 'O', 'F'],
    a_time=None
)

# definition des expression regulieres pour chaque champs
value_template = dict(
    stop_name=r'^[A-Z]{1}[\w ]+ (Street|Avenue|Boulevard|Road)$',
    stop_type=r'.{0,1}',
    a_time=r'[0-2]\d:[0-6]\d$'
)


def get_start_stop():
    """
    Determination du nombre de point de depart, arrêt et transit des bus.

    :return:
    """
    start_stop = []
    final_stop = []
    start = []
    final = []
    test_ok = True
    for i, b in enumerate(inp_list):
        # s'il y a un arret sans depart
        if b['bus_id'] not in start and b['stop_type'] != 'S':
            print("There is no start or end stop for the line: ", b['bus_id'])
            test_ok = False
            break
        else:
            if b['stop_type'] == 'S':
                start.append(b['bus_id'])
                start_stop.append(b['stop_name']) if b['stop_name'] not in start_stop else ''
            elif b['stop_type'] == 'F':
                del (start[start.index(b['bus_id'])])
                final.append(b['bus_id'])
                final_stop.append(b['stop_name']) if b['stop_name'] not in final_stop else ''

    # s'il y a un depart sans arret
    if len(start) > 0:
        print("There is no start or end stop for the line: ", start[0])
        test_ok = False
    elif test_ok:
        all_stops = [i for i in [j['stop_name'] for j in inp_list]]
        transfer_stop = [i for i in set(all_stops) if all_stops.count(i) > 1]
        if len(start_stop):
            print("Start stops: ", len(start_stop), sorted(start_stop))
        if len(transfer_stop):
            print("Transfer stops: ", len(transfer_stop), sorted(transfer_stop))
        if len(final_stop):
            print("Finish stops: ", len(final_stop), sorted(final_stop))

    return test_ok


def unlost_time():
    """
    Check that the arrival time for the upcoming stops for a given bus line is increasing.

    :return: 
    """
    print("Arrival time test:")

    last_bus = None
    last_time = None
    erros_stop = {}
    for i, bus in enumerate(inp_list):
        if bus['bus_id'] == last_bus and time.strptime(last_time, "%H:%M") > time.strptime(bus['a_time'], "%H:%M"):
            if bus['bus_id'] not in erros_stop:
                erros_stop[bus['bus_id']] = [bus['bus_id'], bus['stop_name']]

        last_bus = bus['bus_id']
        last_time = bus['a_time']

    if len(erros_stop):
        for bus in erros_stop.values():
            print("bus_id line {}: wrong time on {}".format(bus[0], bus[1]))
    else:
        print("OK")


def on_demand():
    start = []
    final = []
    transit = []
    demand = []
    for i, bus in enumerate(inp_list):
        if bus['stop_type'] == 'S':
            start.append(bus['stop_name'])
        elif bus['stop_type'] == 'O':
            demand.append(bus['stop_name'])
        elif bus['stop_type'] == 'F':
            final.append(bus['stop_name'])
        else:
            transit.append(bus['stop_name'])

    error_deman = [place for place in demand if place in start + final + transit]
    error_deman = sorted(list(set(error_deman)))

    print("On demand stops test:")
    if len(error_deman):
        print("Wrong stop type: {}".format(error_deman))
    else:
        print("OK")



# Debut d'execution du code
for item in inp_list:
    if not isinstance(item, dict):
        # ignorer si l'item n'est pas un dictionnaire
        continue
    for k, v in item.items():
        # Verifier la conformité du format des données <== EXO-1
        if any([
            # Si la valeur du champ ne correspond pas au type defini
            not isinstance(v, key_type.get(k)),
            # si la valeur du champ est vide alors qu'il ne devrait pas
            not v and not allow_empty.get(k),
            # si la valeur du champ ne correspond pas à la liste des choix
            value_choice.get(k) and v not in value_choice.get(k),
            k in value_template and not re.match(value_template[k], v)
        ]):
            err_count[k] += 1

    # Compter le nombre d'arrêt pour chaque bus <== EXO-2
    if item['bus_id'] not in stop_count:
        stop_count[item['bus_id']] = 1
    else:
        stop_count[item['bus_id']] += 1

    # Vérifier les depart et arrêt <== EXO-3

if sum(err_count.values()) > 0:
    print(f'Format validation: {sum(err_count.values())} errors')
    [print(f'{k}: {v}') for k, v in err_count.items() if k in value_template]
else:
    # get_start_stop() # Verification des point de depart et arret <== EXO4
    # unlost_time()  # Verification des heures d'arrets  <== EXO5
    on_demand()   # Vérification des arrêts à la demande
