"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""


def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree.label()["SEM"]
    print("====== logical_expr =====")
    f = "?f"
    arrival_location = "?sa"
    arrival_time = "?ta"
    departure_location = "?sd"
    departure_time = "?td"

    # [<ApplicationExpression ARRIVE1(a3,f2,TIME(t2,20:00HR))>, <AndExpression (FLIGHT1(f2) & DEST(f2,NAME(h3,'Hue')))>, <ApplicationExpression WH(f2,WHICH1)>]
    verb_expression, flight_expression, wh_expression = logical_expression.args
    gap = "?" + str(logical_tree.label()["GAP"])

    # ---------Check Flight Expression------------#
    np_variables = flight_expression.variables()
    np_preds = [pred.name for pred in flight_expression.predicates()]

    if "DEST" in np_preds:
        # DEST(f (NAME(a,B)))
        arrival_location = (
            "HUE" if list(flight_expression.constants())[0].name == "'Hue'" else "HCMC"
        )
    else:
        # SOURCE(f, NAME(a,B))
        departure_location = (
            "HUE" if list(flight_expression.constants())[0].name == "'Hue'" else "HCMC"
        )

    # Get flight variable (f1 or f2 or ...)
    f = "?" + [variable.name for variable in np_variables if "f" in variable.name][0]

    # -------------Check Verb expression-------------#
    verb_pred_list = [pred.name for pred in verb_expression.predicates()]

    # In case of this assignment, this condition will be always TRUE
    # because time must be specified or be asked in all questions
    if "TIME" in verb_pred_list:
        time_expression = verb_expression.args[2]
        if len(time_expression.args) == 1:
            # TIME(t)
            time = str(time_expression.args[0])
        else:
            # TIME(t,HOUR) (ex: TIME(t1,1600HR))
            time = str(time_expression.args[1])

        # ARRIVE or DEPART?

    if "ARRIVE1" in verb_pred_list:
        # ARRIVE1(v,f,t)
        arrival_time = time if time not in gap else gap
    else:
        # DEPART1(v,f,t)
        departure_time = time if time not in gap else gap

    # --------Fill with parsed values-----------------#
    flight = "(FLIGHT {})".format(f)
    arrival = "(ATIME {} {} {})".format(f, arrival_location, arrival_time)
    departure = "(DTIME {} {} {})".format(f, departure_location, departure_time)
    proceduce = "(PRINT-ALL {}{}{}{})".format(gap, flight, arrival, departure)

    return {
        "query": gap,
        "flight": f,
        "arrival_location": arrival_location,
        "arrival_time": arrival_time,
        "departure_location": departure_location,
        "departure_time": departure_time,
        "str": proceduce,
    }
