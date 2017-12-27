"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

raw_database = ["(FLIGHT F1)",
                    "(ATIME F1 HUE 17:00HR)",
                    "(DTIME F1 HCMC 15:00HR)",
                    "(FLIGHT F2)",
                    "(ATIME F2 HCMC 16:00HR)",
                    "(DTIME F2 HUE 14:30HR)",
                    "(FLIGHT F3)",
                    "(ATIME F3 HUE 20:00HR)",
                    "(DTIME F3 HCMC 18:30HR)",
                    "(FLIGHT F4)",
                    "(ATIME F4 HCMC 10:00HR)",
                    "(DTIME F4 HUE 8:30HR)"]

def categorize_database(database):
    """
    Categorize raw database to collections of FLIGHT, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    #Remove ( )
    flights = [data.replace('(','').replace(')','') for data in database if 'FLIGHT' in data]
    arrival_times = [data.replace('(','').replace(')','') for data in database if 'ATIME' in data]
    departure_times = [data.replace('(','').replace(')','') for data in database if 'DTIME' in data]
    return {'flights': flights, 
            'arrival':arrival_times, 
            'departure':departure_times}

def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """
    procedure_semantics = semantics
    database = categorize_database(raw_database)
    
    #remove unknown args: ?t ?f ?s
    query =  procedure_semantics['query']
    result_type = 'flight'
    
    for arg in list(procedure_semantics.keys()):
        if '?' in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ''
        elif procedure_semantics[arg] == query and arg != 'query':
            #arrive or depart time
            procedure_semantics[arg] = ''
            result_type = arg
                 
    #Iterate after FLIGHT, ATIME and DTIME to have result
    flight_check_result = [f.split()[1] for f in database['flights'] if procedure_semantics['flight'] in f]

    arrival_flight_result = [a.split()[1] for a in database['arrival']
                            if procedure_semantics['arrival_location'] in a
                            and procedure_semantics['arrival_time'] in a
                            and a.split()[1] in flight_check_result]

    departure_flight_result = [d.split()[1] for d in database['departure'] 
                              if procedure_semantics['departure_location'] in d
                              and procedure_semantics['departure_time'] in d
                              and d.split()[1] in arrival_flight_result]

    if result_type == 'flight':
        result = departure_flight_result
    elif result_type == 'arrival_time':
        result = [a.split()[3] for a in database['arrival'] if a.split()[1] in departure_flight_result]
    else:
        result = [d.split()[3] for d in database['departure'] if d.split()[1] in departure_flight_result]
    return result