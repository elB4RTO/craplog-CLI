
import curses

from os import walk as growing

from crappy.elements.model import UIobj


class Tree( UIobj ):
    """
    Sub-Class for the TREE interface
    """
    def initContent(self, crappath:str ):
        """
        Correctly initializes the content variable
        """
        self.roots = crappath
        self.tree = {}
        self.growTree()
        # the actual branch on the tree
        self.branch = {}
        # holds the actual branch's content
        self.leafs = []
        # holds every step needed to climb-up to the actual branch
        self.steps = []
        # holds the steps needed to reach the actually viewed file, may differ from self.steps
        self.selected_file_steps = []
        # visual line index
        self.vli     = 0
        self.aux_vli = 0
        self.selected = 0
        # printable content
        self.content = []
        # symbols
        self.MORE = "‥"
        self.ROOT = "⟤"
        self.FILE = "⧠"
        self.DIR  = "⧈"
        # alternative symbols
        self.FILE_ = "□"
        self.DIR_  = "◳"
        # namespaces for crapstat fiels
        self.names = {
            'IP'  : "Clients IPs",
            'UA'  : "User-Agents",
            'REQ' : "Requests",
            'RES' : "Response codes",
            'ERR' : "Error reports",
            'LEV' : "Error levels"
        }
        self.seman = {
            'Clients IPs'    : "IP",
            'User-Agents'    : "UA",
            'Requests'       : "REQ",
            'Response codes' : "RES",
            'Error reports'  : "ERR",
            'Error levels'   : "LEV"
        }
        # build the directory tree
        self.newTree()
    
    
    
    def clearAll(self ):
        """
        Clear the content viewth and delete data
        """
        self.climbDown( len(self.steps) )
        self.newTree()
        self.cleanContentArea()
        self.drawContent()
    
    
    
    def newTree(self):
        """
        Re-initialize the directory tree
        """
        self.vli = 0
        self.aux_vli = 0
        self.selected = 0
        self.selected_file_steps.clear()
        self.growTree()
        self.climbTree()
        self.pickLeafs()
        self.buildContent()
    
    
    
    def growTree(self):
        """
        Scans the crapstats to make the directory tree
        """
        def cutDriedBranches( branch ):
            for k,v in branch.items():
                if type(v) is dict:
                    if len(v) == 0:
                        _ = branch.pop( k )
                    else:
                        cutDriedBranches( v )
                        if len(v) == 0:
                            _ = branch.pop( k )
        
        # dig the soil
        self.tree.clear()
        # climb the tree
        trunk = "%s/crapstats" %( self.roots )
        trunk_len = len(trunk)+1
        for path,dirs,files in growing( trunk ):
            # step in the correct position
            branch = self.tree
            if len(path) > trunk_len:
                chunks = path[trunk_len:].split('/')
                for i in range(len(chunks)):
                    if chunks[i] == "":
                        continue
                    branch = branch[ chunks[i] ]
            # append directories as dictionaries
            for dir_name in dirs:
                if dir_name.startswith('.')\
                or dir_name in ["CVS", "backups"]:
                    dirs.remove( dir_name )
                    continue
                branch.update({ dir_name : {} })
            # append crapstat files as paths
            for file_name in files:
                if not file_name.startswith('.')\
                and file_name.endswith(".crapstat"):
                    branch.update({ file_name[:-9] : "%s/%s" %( path, file_name ) })
        # recursively remove empty folders
        cutDriedBranches( self.tree )
    
    
    
    def climbTree(self):
        """
        Recursively climbs the directory tree up to the actual branch
        """
        self.branch = self.tree
        for step in self.steps:
            self.branch = self.branch[ step ]
    
    
    
    def climbUp(self, step:str ):
        """
        One branch foreward on the tree
        """
        self.steps.append( step )
        self.branch = self.branch[ step ]
    
    
    def climbDown(self, steps:int ):
        """
        One branch backward on the tree
        """
        self.steps = self.steps[:-steps]
        self.climbTree()
    
    
    
    def pickLeafs(self):
        """
        Picks-up the elements in the actual branch
        """
        dirs  = []
        files = []
        self.leafs.clear()
        for k,v in self.branch.items():
            if type(v) is dict:
                dirs.append(k)
            else:
                files.append(k)
        for name in sorted(dirs):
            self.leafs.append("%s %s" %( self.DIR, name ))
        for name in sorted(files):
            self.leafs.append("%s %s" %( self.FILE, self.names[name] ))
    
    
    
    def buildContent(self):
        """
        Prepares the actual content to be ready-to-draw
        """
        self.content.clear()
        # add crapstats' trunk
        self.content.append("%s crapstats%s" %( self.ROOT, " "*(self.w-13) ))
        # add all the previous branches
        i = -1
        for i in range(len(self.steps)):
            line = " "*(i+1)
            line += "└%s %s" %( self.DIR, self.steps[i] )
            if len(line) < (self.w-2):
                line += " "*( self.w-2-len(line) )
            elif len(line) > (self.w-2):
                line = "%s%s" %( line[:self.w-3], self.MORE )
            self.content.append( line )
        if i < 0:
            i = 0
        else:
            i += 1
        # add the leafs of the actual branch
        self.pickLeafs()
        for leaf in self.leafs:
            line = " "*(i+1)
            line += "├%s" %( leaf )
            if len(line) < (self.w-2):
                line += " "*( self.w-2-len(line) )
            elif len(line) > (self.w-2):
                line = "%s%s" %( line[:self.w-3], self.MORE )
            self.content.append( line )
        # replace the last line's symbol to be the final one
        self.content[-1] = self.content[-1].replace("├","└")
    
    
    
    def smartRedraw(self):
        """
        Just redraw the current and the next line
        """
        t_color = curses.color_pair(31)
        h_color = curses.color_pair(32)
        # redraw the actual line as non-highlighted
        self.window.addstr(
            self.aux_vli+1, 1,
            self.content[self.aux_vli],
            t_color )
        # redraw the next line as highlighted
        self.window.addstr(
            self.vli+1, 1,
            self.content[self.vli],
            h_color )
        # push the updates
        self.window.noutrefresh()
    
    
    
    def smartClean(self):
        """
        Cleans only the needed content
        """
        soap = " "*(self.w-2)
        brush = len(self.steps) + len(self.leafs) + 1
        if brush > self.h-2:
            brush = self.h-2
        for i in range(1,brush+1):
            self.window.addstr(
                i, 1,
                soap )
        # push the updates
        self.window.noutrefresh()
    
    
    
    def drawContent(self):
        """
        Draws the entire content
        """
        # set the color for the content
        t_color = curses.color_pair(21)
        h_color = curses.color_pair(22)
        if self.focus is True:
            t_color = curses.color_pair(31)
            h_color = curses.color_pair(32)
        else:
            self.setSelectVLI()
        # print the content
        i = 0
        mark = self.vli
        for line in self.content:
            # choose the color
            color = t_color
            if i == mark:
                color = h_color
            # draw
            i += 1
            self.window.addstr(
                i, 1,
                line, color )
        # push the updates
        self.window.noutrefresh()
    
    
    
    def updateVLI(self, diff:int ):
        """
        Updates the Visual Line Index
        """
        new_vli = self.vli + diff
        if new_vli >= 0\
        and new_vli < len(self.content):
            self.aux_vli = self.vli
            self.vli = new_vli
    
    
    
    def resetVLI(self):
        """
        Resets the Visual Line Index
        """
        if self.aux_vli != self.vli != self.selected:
            self.aux_vli = self.vli = self.selected
            if self.focus is False:
                self.setSelectVLI()
    
    
    
    def setSelectVLI(self):
        """
        Get the appropriate Visual Line Index
        """
        result = True
        if len(self.selected_file_steps) == len(self.steps)+1:
            for x,y in zip(self.steps,self.selected_file_steps):
                if x != y:
                    # different branches
                    result = False
                    break
        else:
            result = False
        # decide what to show
        if result is True:
            # the actual selected file is still visible in the tree
            self.leafSelect( self.selected_file_steps[-1] )
        else:
            # select the last branch
            try:
                branch = self.steps[-1]
            except:
                branch = "crapstats"
            self.branchSelect( branch )
    
    
    
    def backSelect(self):
        """
        Set the VLI to the old branch position
        """
        i = 0
        try:
            branch = self.steps[-1]
        except:
            branch = "crapstats"
        if branch != "crapstats":
            for line in self.content:
                line = line.strip(" ├└%s%s" %( self.DIR, self.ROOT ))
                if line == branch:
                    break
                i += 1
        self.selected = self.vli + ( i - self.vli )
        self.aux_vli = self.vli = self.selected
    
    
    
    def branchSelect(self, branch:str ):
        """
        Set the VLI to the new branch position
        """
        i = 0
        if branch != "crapstats":
            for line in self.content:
                line = line.strip(" ├└%s%s" %( self.DIR, self.ROOT ))
                if line == branch:
                    break
                i += 1
        self.selected = self.vli + ( i - self.vli )
        self.aux_vli = self.vli = self.selected
    
    
    
    def leafSelect(self, leaf:str ):
        """
        Set the VLI to the viewed leaf position
        """
        i = 0
        for line in self.content:
            line = line.strip(" ├└%s" %( self.FILE ))
            if line == leaf:
                break
            i += 1
        self.selected = self.vli + ( i - self.vli )
        self.aux_vli = self.vli = self.selected
    
    
    
    def select(self):
        """
        Select a branch/leaf to expand/view
        """
        item = self.content[self.vli].strip(" ├└")
        if item == "":
            # empty string
            raise Exception("tree.select&selection item is empty")
        elif item.startswith( self.DIR ):
            # expand the dir content
            item = item.strip("%s " %(self.DIR))
            steps_len = len(self.steps)
            rebuild = True
            if self.vli != steps_len:
                self.smartClean()
                if self.vli > steps_len:
                    self.climbUp( item )
                else:
                    self.climbDown( steps_len-self.vli )
                # build the content
                self.buildContent()
                self.drawContent()
        elif item.startswith( self.FILE ):
            # view the file
            item = item.strip("%s " %(self.FILE))
            self.selected_file_steps = self.steps.copy() + [item]
            self.ui.tree2view( self.branch[ self.seman[ item ]] )
        else:
            # crapstats root
            self.smartClean()
            self.climbDown( len(self.steps) )
            self.buildContent()
            self.drawContent()
        # finally assign the new selection
        self.selected = self.vli
    
    
    
    def search(self, char:chr ):
        """
        Finds the first occurrence matching the char
        Tries in the leafs first, tries in the branches if fails
        """
        found = -1
        # search in the visualized leafs
        i = 1
        for leaf in self.leafs:
            leaf = leaf.strip(" %s%s" %(self.DIR,self.FILE))
            if leaf[0].lower() == char:
                found = i + len(self.steps)
                break
            i += 1
        if found < 0:
            # search in the visualized branches
            i = 0
            for branch in ["crapstats"]+self.steps:
                if branch[0] == char:
                    found = i
                    break
                i += 1
        # update the VLI if found any
        if found >= 0:
            self.aux_vli = self.vli
            self.vli = found
            self.smartRedraw()
    
    
    
    def feed(self, key:int ):
        """
        Manages a keyboard input
        """
        def getBranch() -> str :
            try:
                branch = self.steps[-1]
            except:
                branch = "crapstats"
            return branch
            
        # help
        if key == curses.KEY_HELP:
            # help mode
            pass # 2 COMPLETE !!!
        # arrow up
        elif key == curses.KEY_UP:
            # one line up
            self.updateVLI( -1 )
            self.smartRedraw()
        # arrow down
        elif key == curses.KEY_DOWN:
            # one line down     
            self.updateVLI( +1 )
            self.smartRedraw()
        # enter
        elif key == curses.KEY_ENTER\
          or key == 10:
            # expand/view the selection
            self.select()
            self.branchSelect( getBranch() )
            self.buildContent()
            self.drawContent()
        # backspace
        elif key == curses.KEY_BACKSPACE\
          or key == 127:
            # one step back
            branch = getBranch()
            self.smartClean()
            self.climbDown( 1 )
            self.buildContent()
            self.branchSelect( branch )
            self.drawContent()
        # canc
        elif key == curses.KEY_CANCEL\
          or key == 330:
            # back to the crapstats root
            self.smartClean()
            self.climbDown( len(self.steps) )
            self.buildContent()
            self.branchSelect( "crapstats" )
            self.drawContent()
        # canc + shift
        elif key == 383:
            # re-build the tree (re-scan the crapstats)
            self.clearAll()
        
        # assume everything else is text
        else:
            if key < 127:
                # skip non-ascii chars
                try:
                    # convert to char
                    char = str(chr( key )).lower()
                    # skip invalid chars
                    if char.isalnum():
                        self.search( char )
                    elif char == ':':
                        self.ui.switch2CLI()
                except:
                    # failed to convert to char
                    pass
    
    
    
    def cliTree(self, new_tree:list ):
        """
        Receive a tree from the CLI and tries to apply it
        """
        is_leaf = False
        apply_tree = True
        # try from the actual branch first
        new_steps = self.steps.copy()
        new_branch = self.branch
        for step in new_tree:
            try:
                new_branch = new_branch[ step ]
                new_steps.append(step)
            except:
                try:
                    new_leaf = step.upper()
                    new_visual_name = self.names[new_leaf]
                    new_leaf_path = new_branch[new_leaf]
                    is_leaf = True
                except:
                    # not valid as tree
                    apply_tree = False
                    break
        # try from roots if failed
        if apply_tree is False:
            apply_tree = True
            new_steps.clear()
            new_branch = self.tree
            for step in new_tree:
                try:
                    new_branch = new_branch[ step ]
                    new_steps.append(step)
                except:
                    try:
                        new_leaf = step.upper()
                        new_visual_name = self.names[new_leaf]
                        new_leaf_path = new_branch[new_leaf]
                        is_leaf = True
                    except:
                        # not valid as tree
                        apply_tree = False
                        break
        # apply the new vaules if succesful
        if apply_tree is True:
            self.branch = new_branch
            self.steps  = new_steps
            if is_leaf is True:
                self.selected_file_steps = new_steps.copy() + [new_visual_name]
                self.leafSelect( new_visual_name )
            else:
                self.backSelect()
            self.buildContent()
            self.drawContent()
            if is_leaf is True:
                self.ui.tree2view( new_leaf_path )
            else:
                self.ui.switch2tree()
    
