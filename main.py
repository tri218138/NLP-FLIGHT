"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""
import nltk
from nltk import grammar, parse
import argparse

from nlp_parser import parse_to_procedure
from nlp_data import retrieve_result
from nlp_file import write_file

def main(args):
    """
    Main entry point for the program
    """
    #Load grammar from .fcfg file
    print("-------------Loading grammar---------------------")
    nlp_grammar = parse.load_parser(args.rule_file_name, trace = 0)
    print("Grammar loaded at {}".format(args.rule_file_name))
    #write_file(1, str(nlp_grammar.grammar()))
               
    question = args.question
    
    #Get parse tree
    print("-------------Parsed structure-------------")
    tree = nlp_grammar.parse_one(question.replace('?','').split())
    print(question)
    print(tree)
    #write_file(2, str(tree))
 
    #Parse to logical form
    print("-------------Parsed logical form-------------")
    logical_form = str(tree.label()['SEM']).replace(',',' ')
    print(logical_form)
    #write_file(3, str(logical_form))
               
    #Get procedure semantics
    print("-------------Procedure semantics-------------")
    procedure_semantics = parse_to_procedure(tree)
    print(procedure_semantics['str'])
    #write_file(4, procedure_semantics['str'])
    
    #Retrive result:
    print("-------------Retrieved result-------------")
    results = retrieve_result(procedure_semantics)
    if len(results) == 0:
        print("No result found!")
    else:
        for result in results:
            print(result, end=' ', flush=True)
        print('')
        #write_file(5, " ".join(results))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
      '--question',
      default= "Which flight to Huế city arrives at 20:00HR ?",
      help= "Question to be parsed. Default = 'Which flight to Huế city arrives at 20:00HR ?'"
      )
    
    parser.add_argument(
      '--rule_file_name',
      default= "grammar.fcfg",
      help= "Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
      )
    
    args = parser.parse_args()
    main(args)