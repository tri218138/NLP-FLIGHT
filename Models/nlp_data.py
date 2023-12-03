"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

from Input.database import raw_database


def categorize_database(database):
    """
    Categorize raw database to collections of FLIGHT, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    # Remove ( )
    flights = [
        data.replace("(", "").replace(")", "") for data in database if "MÁY_BAY" in data
    ]
    arrival_times = [
        data.replace("(", "").replace(")", "") for data in database if "ATIME" in data
    ]
    departure_times = [
        data.replace("(", "").replace(")", "") for data in database if "DTIME" in data
    ]
    run_times = [
        data.replace("(", "").replace(")", "")
        for data in database
        if "RUN-TIME" in data
    ]

    return {
        "flights": flights,
        "arrival": arrival_times,
        "departure": departure_times,
        "run_time": run_times,
    }


class ReturnType:
    Flight = "flight"
    Location = "location"
    Time = "time"
    YesNo = "yes/no"
    ArrivalTime = "arrival_time"
    DepartureTime = "departure_time"


def retrieve_flight(database, procedure_semantics):
    flight_check_result = [
        f.split()[1] for f in database["flights"] if procedure_semantics["flight"] in f
    ]

    arrival_flight_result = [
        a.split()[1]
        for a in database["arrival"]
        if procedure_semantics["aloc"] in a
        and procedure_semantics["atime"] in a
        and a.split()[1] in flight_check_result
    ]

    departure_flight_result = [
        d.split()[1]
        for d in database["departure"]
        if procedure_semantics["dloc"] in d
        and procedure_semantics["dtime"] in d
        and d.split()[1] in arrival_flight_result
    ]

    run_flight_result = [
        r.split()[1]
        for r in database["run_time"]
        if (procedure_semantics["dloc"] in r.split()[2])
        and (procedure_semantics["aloc"] in r.split()[3])
        and (procedure_semantics["runtime"] in r)
        and (r.split()[1] in departure_flight_result)
    ]

    run_flight_result2 = [
        r.split()[1]
        for r in database["run_time"]
        if (procedure_semantics["dloc"] in r.split()[2])
        and (procedure_semantics["aloc"] in r.split()[3])
        and (procedure_semantics["runtime"] in r)
    ]

    if run_flight_result != []:
        return run_flight_result
    else:
        return run_flight_result2


def retrieve_time(database, procedure_semantics):
    arrival_time_result = [
        a.split()[3]
        for a in database["arrival"]
        if procedure_semantics["flight"] in a and procedure_semantics["aloc"] in a
    ]

    departure_time_result = [
        d.split()[3]
        for d in database["departure"]
        if procedure_semantics["flight"] in d and procedure_semantics["dloc"] in d
    ]

    run_time_result = [
        r.split()[4]
        for r in database["run_time"]
        if procedure_semantics["flight"] in r.split()[1]
        if procedure_semantics["dloc"] in r.split()[2]
        and procedure_semantics["aloc"] in r.split()[3]
    ]

    return run_time_result


def retrieve_location(database, procedure_semantics):
    if procedure_semantics["aloc"] in procedure_semantics["variable"]:
        arrival_loc_result = [
            a.split()[2]
            for a in database["arrival"]
            if procedure_semantics["flight"] in a and procedure_semantics["atime"] in a
        ]

        return arrival_loc_result

    if procedure_semantics["dloc"] in procedure_semantics["variable"]:
        departure_loc_result = [
            d.split()[2]
            for d in database["departure"]
            if procedure_semantics["flight"] in d and procedure_semantics["dtime"] in d
        ]

        return departure_loc_result


def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """
    procedure_semantics = semantics
    database = categorize_database(raw_database)

    query = procedure_semantics["variable"]
    command = procedure_semantics["command"]
    if "?f" in query and command == "PRINT-ALL":
        result_type = ReturnType.Flight
    elif "?c" in query and command == "PRINT-ALL":
        result_type = ReturnType.Location
    elif "?t" in query and command == "PRINT-ALL":
        result_type = ReturnType.Time
    elif command == "FIND-ONE-TRUE":
        result_type = ReturnType.YesNo

    # remove unknown args: ?t ?f ?s
    for arg in list(procedure_semantics.keys()):
        if "?" in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ""
        elif procedure_semantics[arg] == query and arg != "variable":
            # arrive or depart time
            procedure_semantics[arg] = ""

    # print(procedure_semantics)
    # Iterate after FLIGHT, ATIME and DTIME to have result

    if result_type == ReturnType.Flight:
        result = retrieve_flight(database, procedure_semantics)
    elif result_type == ReturnType.Location:
        result = retrieve_location(database, procedure_semantics)
    elif result_type == ReturnType.Time:
        result = retrieve_time(database, procedure_semantics)
    if result_type == ReturnType.YesNo:
        result = [str(retrieve_flight(database, procedure_semantics) != [])]

    return result
