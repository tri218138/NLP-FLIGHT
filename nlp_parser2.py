"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""


def database_pattern(
    f: str = "?f",
    la: str = "?la",  # loc arrival
    ld: str = "?ld",  # loc departure
    ta: str = "?ta",  # time arrival
    td: str = "?td",  # time departure
    tr: str = "?tr",  # time run
):
    flight = "(MÁY_BAY {})".format(f)  # MÁY_BAY VN1
    arrival = "(ATIME {} {} {})".format(f, la, ta)  # ATIME VN1 HUE 11:00HR
    departure = "(DTIME {} {} {})".format(f, ld, td)  # DTIME VN1 HCMC 10:00HR
    run_time = "(RUN-TIME {} {} {} {})".format(
        f, ld, la, tr
    )  # RUN-TIME VN1 HCMC HUE 1:00HR
    return {
        "flight": flight,
        "arrival": arrival,
        "departure": departure,
        "run_time": run_time,
    }


def extract_variable_or_constant(expr):
    if len(expr.variables()):
        return list(expr.variables())[0].name
    elif len(expr.constants()):
        return list(expr.constants())[0].name
    raise Exception("NOT FOUND ANY VARIABLE OF CONSTANT")


def extract_time_variable(expr):
    time_mod = str(list(expr.predicates())[0].name)
    time_val = extract_variable_or_constant(expr)
    return time_mod, time_val


def procedure_wh(logic_expr):
    print("Procedure which")
    vars = {}
    for expr in logic_expr.args:
        pred = str(expr.pred)
        if pred == "WHICH":
            print(expr.predicates())
            print(expr.variables())
        if pred == "WHEN":
            print(expr.predicates())
            print(expr.variables())
        elif pred == "FLIGHT":
            vars["f"] = extract_variable_or_constant(expr)
        elif pred == "DEST":
            # DEST(CITY('Hue'),TIME(AT(13:30HR)))
            for var in expr.variables():
                print(var)
            for arg in expr.args:
                if str(arg.pred) == "CITY":
                    vars["la"] = extract_variable_or_constant(arg)
                elif str(arg.pred) == "TIME":
                    vars["ta"] = extract_variable_or_constant(arg)
        elif pred == "SOURCE":
            # SOURCE(CITY('DaNang') DEST(CITY('HoChiMinh')) TIME(IN('1:00HR')))
            for var in expr.variables():
                print(var)
            for arg in expr.args:
                if str(arg.pred) == "CITY":
                    vars["ld"] = extract_variable_or_constant(arg)
                elif str(arg.pred) == "TIME":
                    time_mod, time_val = extract_time_variable(arg)
                    if time_mod == "IN":  # time mod
                        vars["tr"] = time_val
                    elif time_mod == "AT":
                        vars["td"] = time_val
                elif str(arg.pred) == "DEST":
                    vars["la"] = extract_variable_or_constant(arg)

    return database_pattern(**vars)


def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree.label()["SEM"]
    # logical_expression: WHQUERY(WHICH(f2),FLIGHT(f2),DEST(CITY('Hue'),TIME(AT(13:30HR))))
    if str(logical_expression.pred) == "WHQUERY":
        print(logical_expression.args)
        # [<ApplicationExpression WHICH(f2)>, <ApplicationExpression FLIGHT(f2)>, <ApplicationExpression DEST(CITY('Hue'),TIME(AT(13:30HR)))>]
        for expression in logical_expression.args:
            if str(expression.pred) in ["WHICH", "WHEN"]:
                proceduce = procedure_wh(logical_expression)
                print(proceduce)
                return proceduce
    return None

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
        "proceduce": proceduce,
    }
