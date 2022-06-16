
from time import sleep

from random import choice, shuffle
from crappy.check import checkFile, checkFolder


class ModelSet():
    def __init__(self, supercrap:object ):
        """ Model for Sub-Classes """
        # paths
        self.confpath:  str
        self.file_path: str
        # configurations holders
        self.sets_map:  dict
        self.sets_list: list
        # unsaved changes
        self.unsaved_changes: bool
        # auxiliary
        self.settable_choices: list
        self.disabled_choices: list
        # output control
        self.space:     str
        self.morespace: str
        # messages
        self.TXT_crap:     str
        self.MSG_choices:  str
        self.MSG_options:  str
        self.MSG_examples: str
        # retrieve the configuration from file
        #self.readConfigs( supercrap )
    
        
    
    def readConfigs(self, supercrap:object ):
        """ Model for Sub-Classes """
    
    
    def writeConfigs(self, supercrap:object ):
        """ Model for Sub-Classes """
    
    
    def checkIntegrity(self, supercrap:object ) -> bool :
        """ Model for Sub-Classes """
        return True
    
    
    
    def run(self, supercrap:object ) ->  tuple :
        """
        Run the configuration process
        """
        def splitConcept( concept_:str, separator_:str=" ", start_:int=0 ) -> list :
            phrase_ = []
            for word_ in concept_[start_:].split( separator_ ):
                word_ = word_.strip()
                if word_ != "":
                    phrase_.append( word_ )
            return phrase_
        
        def printShow( to_show:list ):
            nonlocal supercrap
            print("%s{cyan}Actual configuration{default}%s"\
                .format(**supercrap.text_colors)\
                %( self.space,self.morespace ))
            max_len = max([ len(s) for s in to_show ])
            for opt in to_show:
                col = supercrap.text_colors['yellow']
                val = self.sets_map[ opt ]
                val_type = type(val)
                if val_type is list:
                    val = " ".join( val )
                elif val_type is not str:
                    val_ = val
                    val = str(val)
                    col = supercrap.text_colors['azul']
                    if val_type is bool:
                        if val_ is True:
                            col = supercrap.text_colors['green']
                        else:
                            col = supercrap.text_colors['rose']
                print("  {grey}[{paradise}%s{grey}]{default}%s  %s%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( opt, " "*(max_len-len(opt)), col, val ))
        
        def printDiscarded( discarded_:list ):
            nonlocal supercrap
            print("%s{cyan}Discarded input:{default}%s"\
                .format(**supercrap.text_colors)\
                %( self.space,self.morespace ))
            space = "\n "
            if supercrap.less_output is True:
                space = ""
            else:
                print(" ",end="")
            for opt in discarded_:
                print(" {rose}%s{default}%s"\
                    .format(**supercrap.text_colors)\
                    %( opt, space ), end="",flush=True)
            if supercrap.less_output is True:
                # step on a new line after last flush
                print()
            if supercrap.more_output is True:
                sleep(0.5)
        
        quit_crapset = False
        redirect = None
        loop = True
        while loop is True:
            discarded = []
            to_show = []
            if supercrap.less_output is False:
                print("{grey}(Enter {white}help{default}{grey} to view a help message){default}"\
                    .format(**supercrap.text_colors))
            user_input = input("{bold}What to edit about %s?%s {paradise}:{default} "\
                .format(**supercrap.text_colors)\
                %( self.TXT_crap, self.space )).lower().strip()
            if user_input.startswith('-')\
            or user_input.startswith(':'):
                c = user_input[0]
                cc = {'-':"dashes",':':"columns"}[user_input[0]]
                supercrap.printWarning("input","%s {grey}[{default}{bold}%s{default}{grey}]{default} are not required"\
                    .format(**supercrap.text_colors)%(cc,c))
                if supercrap.more_output is True:
                    print("                really, you better totally avoid them here")
                if supercrap.less_output is False:
                    print()
            elif user_input in ["q","quit","exit","bye"]:
                loop = False
                quit_crapset = True
            elif user_input in ["b","back","main"]:
                loop = False
            elif user_input in ["s","w","save","write"]:
                self.writeConfigs()
            elif user_input in ["h","help","help me","show help"]:
                print(self.MSG_choices)
                print(self.MSG_options)
            elif user_input in ["e","ex","eg","example","examples","show example","show examples"]:
                print(self.MSG_examples)
            
            elif user_input[:user_input.find(' ')] in self.disabled_choices:
                # leave this normal yellow, it's secondary and doesn't need real attention
                print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( user_input ))
                if supercrap.less_output is False:
                    print()
                    sleep(1)
            
            elif user_input.startswith("go "):
                # process a redirection
                if user_input.startswith("go fuck yourself"):
                    # smile, that's a joke ;)
                    msg = ["ok"]*80+["... thanks, you're so nice"]*19+["go fuck YOURself"]
                    msg.shuffle()
                    print("{bold}%s{default}".format(**supercrap.text_colors)%( choice(msg) ))
                    if msg == "go fuck YOURself":
                        exit() # LOL
                    sleep(choice([1,2,3,4,5,6,7,8,9])*choice([1,2]))
                    continue
                phrase = splitConcept( user_input )
                i = 1
                if phrase[i] in ["to","2"]:
                    i += 1
                if phrase[i] in ["b","back","main"]:
                    loop = False
                elif phrase[i] in ["log","craplog"]:
                    loop = False
                    redirect = "log"
                elif phrase[i] in ["view","crapview"]:
                    loop = False
                    redirect = "view"
                elif phrase[i] in ["set","crapset"]:
                    loop = False
                    redirect = "set"
                elif phrase[i] in ["up","crapup"]:
                    loop = False
                    redirect = "up"
                else:
                    supercrap.printWarning("redirection","not a valid destination: {rose}%s{default}"\
                        .format(**supercrap.text_colors))
            
            elif user_input in ["show","view"]:
                printShow( self.sets_list )
                if supercrap.less_output is False:
                    print()
                
            
            elif user_input.startswith("show ") or user_input.startswith("voew ")\
              or user_input.startswith("set ") or user_input.startswith("assign ")\
              or user_input.startswith("use ") or user_input.startswith("enable ")\
              or user_input.startswith("don't use ") or user_input.startswith("disable "):
                # split in concepts
                phrases = splitConcept( user_input, " and " )
                for phrase in phrases:
                    s = phrase.find(' ')
                    if s == -1:
                        s = len(phrase)
                    if phrase.startswith("don't "):
                        if phrase[s+1:phrase.find(' ', s+1)] != "use":
                            if supercrap.less_output is False:
                                printDiscarded( [phrase] )
                                if supercrap.more_output is True:
                                    sleep(0.5)
                            continue
                        s += 4
                    # get the action
                    action = phrase[:s].strip()
                    phrase = phrase[s+1:].strip()
                    if len(phrase) == 0\
                    and action not in ["show","view"]:
                        continue
                    # get the arguments of the action
                    phrase = splitConcept( phrase, "," )
                    # show the actual value of one or more options
                    if action in ["show","view"]:
                        for word in phrase:
                            if word in self.sets_list\
                            and to_show.count(word) == 0:
                                to_show.append( word )
                            else:
                                discarded.append( word )
                        if len(to_show) == 0:
                            if len(discarded) == 0:
                                printShow( self.sets_list )
                        else:
                            printShow( to_show )
                        to_show = []
                        if supercrap.more_output is True\
                        and len(discarded) > 0:
                            printDiscarded( discarded )
                            discarded = []
                    # appòy a boolean value
                    elif action == "use" or action == "enable"\
                      or action == "don't use" or action == "disable":
                        # assign the correct value
                        if action in ["use","enable"]:
                            val = True
                        else:
                            val = False
                        for word in phrase:
                            if word in self.sets_map.keys():
                                self.sets_map[ word ] = val
                                self.unsaved_changes = True
                            else:
                                discarded.append( word )
                        if supercrap.less_output is False\
                        and len(discarded) > 0:
                            printDiscarded( discarded )
                            discarded = []
                    # apply an argument
                    elif action == "set" or action == "assign":
                        # skip if the target is not valid
                        for option in phrase:
                            found = False
                            for settable in self.settable_choices:
                                if option.startswith("%s "%(settable)):
                                    found = True
                                    break
                            if found is False:
                                if supercrap.less_output is False:
                                    discarded.append( option )
                                continue
                            # get the target option
                            arguments = splitConcept( option )
                            target = arguments[0]
                            if target != "whitelist":
                                target = "%s %s" %( arguments[0],arguments[1] )
                                arguments = arguments[2:]
                            else:
                                arguments = arguments[1:]
                            # get the value to be assigned
                            if len(arguments) == 0:
                                continue
                            if target in ["warning size","trash path","logs path"]:
                                value = arguments[0]
                                # to number
                                if target == "warning size":
                                    try:
                                        value = float(value)
                                        if len(arguments) > 1\
                                        and supercrap.less_output is False:
                                            printDiscarded([" ".join(arguments[i:])])
                                    except:
                                        discarded.append( option )
                                        continue
                                        
                                # to path
                                elif len(arguments) > 1:
                                    i = 1
                                    while True:
                                        if value.endswith('\\'):
                                            value += " %s" %(arguments[i])
                                            i += 1
                                            if i >= len(arguments):
                                                value = value.strip('\\')
                                                break
                                        else:
                                            if i < len(arguments)-1:
                                                if supercrap.less_output is False:
                                                    discarded.append(" ".join(arguments[i:]))
                                            break
                            else:
                                value = []
                                for v in arguments:
                                    v = v.strip()
                                    if v != "":
                                        value.append( v )
                                if len(value) == 0:
                                    continue
                            
                            self.sets_map[ target ] = value
                            self.unsaved_changes = True
                        if supercrap.less_output is False\
                        and len(discarded) > 0:
                            printDiscarded( discarded )
                            discarded = []
                
                if supercrap.less_output is False:
                    print()
            
            
            else:
                # leave this normal yellow, it's secondary and doesn't need real attention
                print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( user_input ))
                if supercrap.less_output is False:
                    print()
                    sleep(1)
        
        return (not quit_crapset, redirect)
    
