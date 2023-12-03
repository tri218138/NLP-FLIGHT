"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""
import re
from nltk import grammar, parse
import argparse

from nlp_parser import parse_to_procedure
from nlp_data import retrieve_result
from nlp_file import write_file


def main(args):
    """
    Main entry point for the program
    """
    # Load grammar from .fcfg file
    print("-------------Loading grammar---------------------")
    nlp_grammar = parse.load_parser(args.rule_file_name, trace=0)
    print("Grammar loaded at {}".format(args.rule_file_name))
    write_file(1, str(nlp_grammar.grammar()))

    question = args.question

    # Get parse tree
    print("-------------Parsed structure-------------")
    tree = nlp_grammar.parse_one(question.replace("?", "").split())
    print(question)
    print(tree)
    write_file(2, str(tree))

    # Parse to logical form
    print("-------------Parsed logical form-------------")
    print(question)
    logical_form = str(tree.label()["SEM"]).replace(",", " ")
    print(logical_form)
    write_file(3, str(logical_form))

    # Get procedure semantics
    print("-------------Procedure semantics-------------")
    procedure_semantics = parse_to_procedure(tree)
    print(procedure_semantics["str"])
    write_file(4, procedure_semantics["str"])

    # Retrive result:
    print("-------------Retrieved result-------------")
    results = retrieve_result(procedure_semantics)
    if len(results) == 0:
        print("No result found!")
    else:
        for result in results:
            print(result, end=" ", flush=True)
        print("")
        write_file(5, " ".join(results))


FIX_WORDS = [
    "máy bay",
    "mã hiệu",
    "thành phố",
    "hãng hàng không",
    "xuất phát",
    "khởi hành",
    "hạ cánh",
    "VietJet Air",
    "Hồ Chí Minh",
    "Đà Nẵng",
    "Hà Nội",
    "Khánh Hòa",
    "Hải Phòng",
    "thời gian",
    "phải không",
    "bao lâu"
]


def preprocess_query(query: str):
    query = query[0].lower() + query[1:]
    query = re.sub(r"T[P|p]\.", "TP. ", query)
    query = re.sub(r",", " và ", query)
    query = re.sub(r"\?", " ? ", query)
    query = re.sub(r" HR", "HR", query)
    for word in FIX_WORDS:
        query = re.sub(word, word.replace(" ", "_"), query)
    return query


def get_query(index: str = "1"):
    """
    start from 1
    """
    return {
        0: "",
        1: "Máy bay nào đến thành phố Huế lúc 13:30HR ?",
        1.1: "Máy bay nào khởi hành lúc 13:30HR đến thành phố Huế?",
        2: "Máy bay nào bay từ Đà Nẵng đến TP. Hồ Chí Minh mất 1 giờ ?",
        3: "Máy bay nào bay từ TP.Hồ Chí Minh đến Hà Nội ?",
        4: "Hãy cho biết mã hiệu các máy bay hạ cánh ở Huế ?",
        5: "Máy bay nào bay từ TP. Hồ Chí Minh đến Đà Nẵng mất 1:00 HR ?",
        6: "Máy bay của hãng hàng không VietJet Air bay đến những thành phố nào ?",
        7: "Thời gian máy bay VJ5 bay từ TP. Hà Nội đến Khánh Hòa mất mấy giờ ?",
        8: "Máy bay từ Hà Nội đến Khánh Hòa bay trong bao lâu?",
        8.1: "Máy bay bay từ Hà Nội đến Khánh Hòa trong bao lâu?",
        9: "Máy bay VJ1 xuất phát từ HCMC 10:00HR phải không ?",
        10: "Máy bay VN4 có xuất phát từ Đà Nẵng không ?",
        11: "Có máy bay nào xuất phát từ Hải Phòng không ?",
        12: "Có máy bay nào bay từ Hải Phòng đến Khánh Hòa không?",
        13: "Máy bay nào xuất phát từ Tp.Hồ Chí Minh, lúc mấy giờ ?",
        13.1: "Máy bay nào xuất phát từ Tp.Hồ Chí Minh, xuất phát lúc mấy giờ ?",
    }.get(float(index), 0.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")

    parser.add_argument(
        "--id",
        default=-1,
        help="Question to be parsed. Default = 'Which flight to Huế city arrives at 20:00HR ?'",
    )

    parser.add_argument(
        "--question",
        default=get_query(1),
        help="Question to be parsed. Default = 'Which flight to Huế city arrives at 20:00HR ?'",
    )

    parser.add_argument(
        "--rule_file_name",
        default="grammar.fcfg",
        help="Context Free Grammar file to be parsed. Default = 'grammar.fcfg'",
    )

    args = parser.parse_args()
    try:
        args.question = get_query(args.question)
    except:
        pass
    args.question = preprocess_query(args.question)
    print(args.question)
    main(args)
