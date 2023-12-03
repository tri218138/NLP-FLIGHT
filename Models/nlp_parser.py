"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

"""
(MÁY_BAY M1) => (MÁY_BAY ?f)
(ATIME VN1 HUE 11:00HR) => (ATIME ?f ?al ?at)
(DTIME VN1 HCMC 10:00HR) => (DTIME ?f ?dl ?dt)
(RUN-TIME VN1 HCMC HUE 1:00 HR) => (RUN-TIME ?f ?dl ?al ?rt)
"""
from copy import copy
from nltk.sem.logic import (
    AndExpression,
    Variable,
    FunctionVariableExpression,
    ApplicationExpression,
    LambdaExpression,
)


def postprocess_location(location):
    location = str(location)
    if location == "'Hue'":
        return "HUE"
    if location == "'HoChiMinh'":
        return "HCM"
    if location == "'DaNang'":
        return "ĐN"
    if location == "'HaNoi'":
        return "HN"
    if location == "'HaiPhong'":
        return "HP"
    if location == "'KhanhHoa'":
        return "KH"


def add_query(query: list, expr):
    if isinstance(query[0], str):
        query[0] = expr
    else:
        query.append(expr)
    return query


def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expr = logical_tree.label()["SEM"]
    # print("====== logical_expr =====")

    f = "?f"
    aloc = "?al"
    dloc = "?dl"
    atime = "?at"
    dtime = "?dt"
    runtime = "?rt"
    query = ["WHICH"]  # default
    if str(logical_expr.pred) == "YNQUERY":
        query = add_query(query, logical_expr)
    np_expr, vp_expr = logical_expr.args
    # apply variable to lambda function
    if type(np_expr) is LambdaExpression:
        np_expr = ApplicationExpression(
            np_expr, FunctionVariableExpression(Variable("f"))
        ).simplify()

    ##### NP #####
    exprs = []
    expr = np_expr
    while type(expr) is AndExpression:
        if type(expr.second) is LambdaExpression:
            expr.second = ApplicationExpression(
                expr.second, FunctionVariableExpression(Variable("f"))
            ).simplify()
        exprs.append(expr.second)
        expr = expr.first
    if type(expr) is LambdaExpression:
        expr = ApplicationExpression(
            expr, FunctionVariableExpression(Variable("f"))
        ).simplify()
    exprs.append(expr)
    for expr in exprs:
        pred = str(expr.pred)
        if pred == "FLIGHT":
            if expr.constants():
                f = list(expr.constants())[0].name[1:-1]
            else:
                f = "?" + list(expr.variables())[0].name
        elif pred == "SOURCE":
            if expr.constants():
                dloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "DEST":
            if expr.constants():
                aloc = postprocess_location(list(expr.constants())[0].name)

    for expr in exprs:
        pred = str(expr.pred)
        if pred == "AIRLINE":
            if expr.constants():
                f = list(expr.constants())[0].name[1:-1]
                if f == "VietJetAir":
                    f = "VJ"

    for expr in exprs:
        for index, pred in enumerate(expr.predicates()):
            if pred.name in ["WHICH", "WHEN", "HOWLONG"]:
                query = add_query(query, expr)

    ##### VP #####
    exprs = []
    expr = vp_expr
    while type(expr) is AndExpression:
        exprs.append(expr.second)
        expr = expr.first
    exprs.append(expr)
    for expr in exprs:
        pred = str(expr.pred)
        if pred == "SOURCE":
            if expr.constants():
                dloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "DEST":
            if expr.constants():
                aloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "ARRIVE":
            for arg in expr.args:
                while type(arg) is AndExpression:
                    if str(arg.second.pred) == "CITY":
                        aloc = list(arg.second.variables())[0].name
                    elif str(arg.second.pred) == "WHICH":
                        query = add_query(query, arg.second)
                    arg = arg.first
                if str(arg.pred) == "CITY":
                    aloc = list(arg.variables())[0].name
                elif str(arg.pred) == "WHICH":
                    query = add_query(query, arg)
            # print(query[0].pred)
        elif pred == "LEAVE":
            expr = expr.args[0]
            for arg in expr.args:
                while type(arg) is AndExpression:
                    if str(arg.second.pred) == "HOUR":
                        dtime = list(arg.second.variables())[0].name
                    elif str(arg.second.pred) == "WHEN":
                        query = add_query(query, arg.second)
                    arg = arg.first
                if str(arg.pred) == "HOUR":
                    dtime = list(arg.variables())[0].name
                elif str(arg.pred) == "WHEN":
                    query = add_query(query, arg)
            # print(query[0].pred)
        elif pred == "IN":
            if expr.constants():
                runtime = list(expr.constants())[0].name[1:-1]
            else:
                for arg in expr.args:
                    while type(arg) is AndExpression:
                        if str(arg.second.pred) == "HOUR":
                            runtime = list(arg.second.variables())[0].name
                        elif str(arg.second.pred) == "WHEN":
                            query = add_query(query, arg.second)
                        elif str(arg.second.pred) == "HOWLONG":
                            query = add_query(query, arg.second)
                        arg = arg.first
                    if str(arg.pred) == "HOUR":
                        runtime = list(arg.variables())[0].name
                    elif str(arg.pred) == "WHEN":
                        query = add_query(query, arg)
                    elif str(arg.pred) == "HOWLONG":
                        query = add_query(query, arg)
                # print(query[0].pred)

    for expr in exprs:
        pred = str(expr.pred)
        if pred == "AT" and dloc != "?dl":
            dtime = list(expr.constants())[0].name[1:-1]
        if pred == "AT" and aloc != "?al":
            atime = list(expr.constants())[0].name[1:-1]

    if type(query[0]) is str:
        for expr in exprs:
            for index, pred in enumerate(expr.predicates()):
                if pred.name in ["WHICH", "WHEN", "HOWLONG"]:
                    query = add_query(query, expr)

    flight = "(MÁY_BAY {})".format(f)
    arrival_time = "(ATIME {} {} {})".format(f, aloc, atime)
    departure_time = "(DTIME {} {} {})".format(f, dloc, dtime)
    run_time = "(RUN-TIME {} {} {} {})".format(f, dloc, aloc, runtime)

    ret = []
    # print(query)
    for index in range(len(query)):
        key = query[index] if isinstance(query[index], str) else str(query[index].pred)
        command = {
            "WHICH": "PRINT-ALL",
            "WHEN": "PRINT-ALL",
            "HOWLONG": "PRINT-ALL",
            "YNQUERY": "FIND-ONE-TRUE",
        }[key]
        try:
            variable = "?" + list(query[index].variables())[0].name
        except:
            try:
                variable = "?" + list(np_expr.variables())[0].name
            except:
                variable = ""
        procedure = "({} {} {} {} {} {})".format(
            command, variable, flight, arrival_time, departure_time, run_time
        )
        ret.append(
            {
                "procedure": procedure,
                "command": command,
                "variable": variable,
                "flight": f,
                "atime": atime,
                "dtime": dtime,
                "aloc": aloc,
                "dloc": dloc,
                "runtime": runtime,
            }
        )

    return ret
