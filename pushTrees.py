from manim import *
import random
import networkx as nx



defaultLanguage =  {
            ":x":{
                "needs":[],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda:PushItem(":x", type="number", done = True)}]},
            ":x1":{
                "needs":[],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda:PushItem(":x1", type="number", done = True)}]},
            ":x2":{
                "needs":[],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda:PushItem(":x2", type="number", done = True)}]},
            ":s1":{
                "needs":[],
                "products":
                    [{"stack":"string", 
                        "symbolic": lambda:PushItem(":s1", type="string", done = True)}]},
            ":b1":{
                "needs":[],
                "products":
                    [{"stack":"bool", 
                        "symbolic": lambda:PushItem(":b1", type="bool", done = True)}]},
            ":p1":{
                "needs":[],
                "products":
                    [{"stack":"point", 
                        "symbolic": lambda:PushItem(":p1", type="point", done = True)}]},
            ":p2":{
                "needs":[],
                "products":
                    [{"stack":"point", 
                        "symbolic": lambda:PushItem(":p2", type="point", done = True)}]},
            ":k1":{
                "needs":[],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda:PushItem(":k1", type="number", done = True)}]},
            ":k2":{
                "needs":[],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda:PushItem(":k2", type="number", done = True)}]},
            ":sin":{
                "needs":["number"],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda x:PushItem("({} :sin)".format(x.value), type="number", done = True)}]},
            ":len":{
                "needs":["string"],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda x:PushItem("({} :len)".format(x.value), type="number", done = True)}]},
            ":x-of":{
                "needs":["point"],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda x:PushItem("({} :x-of)".format(x.value), type="number", done = True)}]},
            ":y-of":{
                "needs":["point"],
                "products":
                    [{"stack":"number", 
                        "symbolic": lambda x:PushItem("({} :y-of)".format(x.value), type="number", done = True)}]},
            ":add":{
                "needs":["number","number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda x,y : PushItem("({} {} :add)".format(y.value, x.value), done = True, type="number")}]},
            ":sub":{
                "needs":["number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda x,y : PushItem("({} {} :sub)".format(y.value, x.value), done = True, type="number")}]},
            ":dist":{
                "needs":["point", "point"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda x,y : PushItem("({} {} :dist)".format(y.value, x.value), done = True, type="number")}]},
            ":mul":{
                "needs":["number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda x,y : PushItem("({} {} :mul)".format(y.value, x.value), done = True, type="number")}]},
            ":pdiv":{
                "needs":["number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda x,y : PushItem("({} {} :pdiv)".format(y.value, x.value), done = True, type="number")}]},
            ":or":{
                "needs":["bool", "bool"],
                "products":
                    [{"stack":"bool",
                        "symbolic": lambda x,y : PushItem("({} {} :or)".format(y.value, x.value), done = True, type="bool")}]},
            ":number-swap":{
                "needs":["number", "number"],
                "products":
                    [{"stack":"number", "symbolic": lambda x,y : x },
                        {"stack":"number", "symbolic": lambda x,y : y }]},
            ":number-dup":{
                "needs":["number"],
                "products":
                    [{"stack":"number", "symbolic": lambda x : x },
                        {"stack":"number", "symbolic": lambda x : copy.deepcopy(x) }]},
            ":exec-dup":{
                "needs":["exec"],
                "products":
                    [{"stack":"exec", "symbolic": lambda x : x },
                        {"stack":"exec", "symbolic": lambda x : copy.deepcopy(x) }]},
            ":string-reverse":{
                "needs":["string"],
                "products":
                    [{"stack":"string",
                        "symbolic": lambda x : PushItem("({} :string-reverse)".format(x.value), done = True, type="string")}]},
            ":ifelse":{
                "needs":["bool", "number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda b,n1,n2 : PushItem("({} {} {} :ifelse)".format(b.value, n2.value, n1.value), done = True, type="number")}]},
            ":ifLTZ":{
                "needs":["number", "number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda n1,n2,n3 : PushItem("({} {} {} :ifLTZ)".format(n3.value, n2.value, n1.value), done = True, type="number")}]},
            ":iflte":{
                "needs":["number", "number", "number", "number"],
                "products":
                    [{"stack":"number",
                        "symbolic": lambda a1,a2,r1,r2 : PushItem("({} {} {} {} :iflte)".format(r2.value, r1.value, a2.value, a1.value), done = True, type="number")}]},
            }

def getTokens(language=defaultLanguage):
    return list(language.keys())

def treeToString(t, parens=True):
    result = ""
    if isinstance(t,str):
        result += t
    elif isinstance(t,list):
        for i in t:
            result = result + " " + treeToString(i,parens=True) + " "
        if parens == True:
            result = "(" + result + ")"
    return result


def fixedTreeSize(num,language=defaultLanguage):
    choices = list(language.keys())
    arities = buildArityDictFrom(language)
    nodes = []
    netArity = 0
    for i in range(num+1):
        t = random.sample(choices,1)[0]
        nodes.append(t)
        netArity = netArity + 1 - arities[t]
    while netArity != 0:
        d = nodes.pop(0)
        netArity = netArity - 1 + arities[d]
        t = random.sample(choices,1)[0]
        nodes.append(t)
        netArity = netArity + 1 - arities[t]
    for i in range(num):
        nodes[i] = nodes[i] + "@" + str(i)
    result = streamToTreeBuilder(nodes,language,'postfix','standard')
    while (len(result) > 1) or (len(flatPush(result)) < num):
        random.shuffle(nodes)
        result = streamToTreeBuilder(nodes,language,'postfix','standard')
    return result
    

def stringToTileMobject(s):
    words = MarkupText(s, width=2)
    box = RoundedRectangle(width=words.width+0.5,height=words.height+0.5, 
                           corner_radius=0.1, stroke_color=DARK_GRAY)
    box.set_fill(invert_color(random_bright_color()), opacity=1.0)
    v = VMobject()
    v.add(box)
    v.add(words)
    return v

def stackSubmobjectsFrontToBack(mob):
    for i in range(len(mob.submobjects)):
        mob.submobjects[i].set_z_index(-i)

def gatherMobjects(items):
    result = []
    for i in items:
        result.append(i.mobject)
    return result 


def randomTokens(size, language=defaultLanguage):
    randTokens = []
    choices = getTokens(language)
    for i in range(size):
        t = random.sample(choices,1)[0] + "@" + str(i)
        randTokens.append(t)
    return randTokens
    
def tokensToPush(tokens=getTokens(defaultLanguage)):
    listing = "( "
    for t in tokens:
        listing = listing + t + " "
    return listing + ")"

def variantPopper(stack,count,method='standard'):
    argList = []
    for i in range(count):
        if method == 'backwards':
            argList.insert(0,stack.pop())
        elif method == 'bag':
            argList.append(stack.pop(random.randrange(len(stack))))
        else:
            argList.append(stack.pop())
    return tuple(argList)
        
def buildArityDictFrom(language):
    # at the moment this ignores types
    # you can pass in a language cartoon, with only arity as the values
    arityDict = {}
    for k in language.keys():
        arityDict[k] = 0
    for k,v in language.items():
        if isinstance(v,dict):
            arityDict[k] = len(v["needs"])
        elif isinstance(v,int):
            arityDict[k] = v
    return arityDict


def streamToTreeBuilder(items,language=defaultLanguage,dialect='postfix',argMethod='standard',memory=None):
    # NOTE the token matching is only using the string up to the symbol '@'
    # if memory is not None, it's assumed to be a DICT; te keys are strings made
    # by concatenating all flattened items in the subtree; the value a tuple
    # containing tuples of strings in postfix order: ("arg1", "arg2", ... , "op"),
    # all after the ID is removed
    
    stack = []
    arities = buildArityDictFrom(language)

    for t in items:
        id = t.split("@")[0]
        if (arities[id]==1) and (len(stack) > 0):
            (arg1) = variantPopper(stack,1,argMethod)[0]
            tup = [arg1, t] if dialect=='postfix' else [t, arg1]
            stack.append(tup)
            if memory is not None:
                memTuple = ( strippedPushString(arg1), id )
                memory[" ".join(memTuple)] = memTuple
        elif (arities[id]==2) and (len(stack) > 1):
            (arg1,arg2) = variantPopper(stack,2,argMethod)
            tup = [arg2, arg1, t] if dialect=='postfix' else [t, arg2, arg1]
            stack.append(tup)
            if memory is not None:
                memTuple = ( strippedPushString(arg2), strippedPushString(arg1), id )
                memory[" ".join(memTuple)] = memTuple
        elif (arities[id]==3) and (len(stack) > 2):
            (arg1,arg2,arg3) = variantPopper(stack,3,argMethod)
            tup = [arg3, arg2, arg1, t] if dialect=='postfix' else [t, arg3, arg2, arg1]
            stack.append(tup)
            if memory is not None:
                memTuple = ( strippedPushString(arg3), strippedPushString(arg2), strippedPushString(arg1), id )
                memory[" ".join(memTuple)] = memTuple
        elif (arities[id]==4) and (len(stack) > 3):
            (arg1,arg2,arg3,arg4) = variantPopper(stack,4,argMethod)
            tup = [arg4, arg3, arg2, arg1, t] if dialect=='postfix' else [t, arg4, arg3, arg2, arg1]
            stack.append(tup)
            if memory is not None:
                memTuple = ( strippedPushString(arg4), 
                             strippedPushString(arg3), 
                             strippedPushString(arg2), 
                             strippedPushString(arg1), 
                             id ) 
                memory[" ".join(memTuple)] = memTuple
        elif (arities[id] == 0):
            stack.append(t)
            if memory is not None:
                memTuple = (id,)
                memory[" ".join(memTuple)] = memTuple
    return stack

 
def flatPush(pushTree):
    flatter = []
    for i in pushTree:
        if isinstance(i,str):
            flatter.append(i)
        elif isinstance(i,list):
            flatter.extend(flatPush(i)) 
    return flatter

def strippedPush(pushTree):
    return [x.split('@')[0] for x in flatPush(pushTree)]

def strippedPushString(pushTree):
    if isinstance(pushTree,str):
        return pushTree.split('@')[0]
    else:
        return " ".join(strippedPush(pushTree))


def getAge(tokenName):
    return int(tokenName.split('@')[1]) if ("@" in tokenName) else 0

def makeTree(subtree, g=None, parent = None, notation='prefix'):
    # the label of a node will be the string split before '@', and its color the number after
    if g is None:
        g = nx.Graph()
    if isinstance(subtree,str):
        g.add_node(subtree)
        if parent is not None:
            g.add_edge(subtree,parent)
    else: # it is a branch, in a list
        if notation == 'prefix':
            operator = subtree.pop(0)
        else:
            operator = subtree.pop(-1)
        g.add_node(operator)
        if parent is not None:
            g.add_edge(operator,parent)
        for arg in subtree:
            g = makeTree(arg,g,operator,notation)
    return g



class PushItem:
    """Simple bundle of info for animations; argument should be a string, 
        or an array of strings, PushItems and arrays"""
    def __init__(self, value, type=None, done=False):
        self.type = type
        if done==False: # don't do any more processing otherwise
            if isinstance(value,list):
                self.type = "codeblock"
                self.value = list(map(lambda x: PushItem(x),value))
            elif isinstance(value,str):
                self.value = value
                if value.isnumeric() or value[0].isdigit() or value[0] == "-":
                    self.type = "number"
                    self.done = True
                elif (value == "True") or (value=="False"):
                    self.type = "bool"
                    self.done = True
                elif value[0] == ":":
                    self.type = "token"
                else:
                    self.type = "string"
                    self.done = True
        else:
            self.value = value
        self.label = treeToString(value)
        self.mobject = stringToTileMobject(self.label)
    

### INTERPRETER
###
# presentation parameters
defaultWorkbench = ORIGIN + 2*UP
fastTime = 0.1
mediumTime = 0.3
slowTime = 0.5

def createEmptyStacks(stackNames=["exec", "number"],useUnused=False):
    stacks = {}
    for s in stackNames:
        stacks[s] = {"base":ORIGIN, "contents":[]}
    if useUnused is True:
        stacks["unused"] = {"base":ORIGIN, "contents":[]}
    return stacks


def showQuickListing(context,pushItem,workbench=defaultWorkbench,previewScale=1.0):
    myListingBox = MarkupText(pushItem.label, width=4)
    myListingBox.move_to(workbench)
    context.play(Write(myListingBox.scale(previewScale)))
    return myListingBox
    
def handleCodeblockInWorkbench(context,stacks,pushItem,workbench=defaultWorkbench):
    items = pushItem.value
    boxes = VGroup(*map(lambda x: x.mobject.scale_to_fit_height(1), items))
    boxes.arrange(direction=(RIGHT), center=True).next_to(workbench,DOWN)
    context.play(ReplacementTransform(pushItem.mobject, boxes),run_time=slowTime)
    for i in range(len(items)):
        item = items.pop()
        moveTokenFromWorkbenchToStack(context,item,stacks,"exec")

def drawStackStages(context,stacks,useUnused=False):
    if useUnused is True:
        stacks["unused"] = {"base":ORIGIN, "contents":[]}
    else:
        stacks.pop("unused", None)

    numberOfStages = len(stacks.keys())
    separation = 14/(numberOfStages+1)

    halfLineWidth = 2*separation/5.0
    x_counter = 0


    for k,v in stacks.items():
        stacks[k]["base"] = (3.5*DOWN + 7*LEFT + RIGHT*separation + separation*x_counter*RIGHT)
        bar = Line(start=stacks[k]["base"]+halfLineWidth*LEFT,end=stacks[k]["base"]+halfLineWidth*RIGHT)
        bar.set_color(WHITE)
        bar.move_to(stacks[k]["base"])
        stacks[k]["line"] = bar
        label = MarkupText(k,font_size=18, font="Andale Mono")
        label.next_to(bar,DOWN)
        context.play(Write(bar), Write(label), run_time=fastTime)
        x_counter += 1

def moveTokenFromWorkbenchToStack(context,pushItem,stacks,targetStack):
    context.play(pushItem.mobject.animate.scale_to_fit_height(0.5),run_time=fastTime)
    if len(stacks[targetStack]["contents"]) == 0:
        where = stacks[targetStack]["base"]
    else:
        where = stacks[targetStack]["contents"][-1].mobject
    context.play(pushItem.mobject.animate.next_to(where,direction=UP, buff=0.05),run_time=fastTime)
    stacks[targetStack]["contents"].append(pushItem)

def instructionNeedsCount(needs):
    result = {}
    for s in needs:
        result[s] = result.get(s, 0) + 1
    return result

def gatherArgs(context,stacks,needs):
    args = []
    for n in needs:
        gotArg = stacks[n]["contents"].pop()
        args.append(gotArg)
    return args


def handleTokenInWorkbench(context,pushItem,stacks,language=defaultLanguage,useUnused=False):
    tile = pushItem.mobject
    context.play(tile.animate.shift(3*RIGHT),run_time=mediumTime)
    if pushItem.value not in language.keys(): 
        quickCaptionUnderTile(context,pushItem,"unknown token!")
        context.play(FadeOut(tile))
        context.remove(tile)
    else:
        token = pushItem.value
        details = language[token]
        needs = details["needs"]
        needsAreSatisfied = True
        for k,v in instructionNeedsCount(needs).items():
            needsAreSatisfied = needsAreSatisfied and (len(stacks[k]["contents"])>=v)
        if not needsAreSatisfied:
            if useUnused is True:
                quickCaptionUnderTile(context,pushItem,text="Wait for arguments")
                moveTokenFromWorkbenchToStack(context,pushItem,stacks,"unused")
            else:
                quickCaptionUnderTile(context,pushItem,"missing arguments")
                context.play(FadeOut(tile))
                context.remove(tile)
        else:
            args = gatherArgs(context,stacks,needs)
            fist = MarkupText("☜", font_size=36).next_to(tile,LEFT)
            context.play(Write(fist),run_time=fastTime)
            for a in range(len(args)):
                bumper = fist if a == 0 else args[a-1].mobject
                context.play(args[a].mobject.animate.next_to(bumper,LEFT).scale_to_fit_height(1),run_time=mediumTime)
            context.play(ReplacementTransform(tile,fist),run_time=slowTime)
            for arg in args: 
                context.play(FadeOut(arg.mobject), run_time=fastTime)
                context.remove(arg)
            newItems = []
            for outcome in details["products"]:
                result = outcome["symbolic"](*args)
                if isinstance(result,list):
                    newItems += result
                else:
                    newItems.append(result)                
            for p in range(len(newItems)):
                pi = newItems[p]
                bumper = fist if p==0 else newItems[p-1].mobject
                pi.mobject.scale_to_fit_height(1).next_to(bumper, LEFT)
                context.play(Write(pi.mobject))
                quickCaptionUnderTile(context,pi)
            for i in newItems:
                moveTokenFromWorkbenchToStack(context,i,stacks,details["products"][p]["stack"])
            context.play(Uncreate(fist),run_time=fastTime)
    
def quickCaptionUnderTile(context,pushItem,text=None):
    text = text or pushItem.type
    caption = MarkupText(text, font_size=24).next_to(pushItem.mobject,DOWN)
    context.play(FadeIn(caption), run_time=mediumTime)
    context.play(FadeOut(caption), run_time=slowTime)

def processEveryItem(context,stacks,language=defaultLanguage,workbench=defaultWorkbench,useUnused=False):
    while len(stacks["exec"]["contents"]) > 0:
        x = stacks["exec"]["contents"].pop()
        context.play(x.mobject.animate.move_to(workbench).scale_to_fit_height(1),run_time=slowTime)
        quickCaptionUnderTile(context,x)
        if x.type in stacks.keys():
            moveTokenFromWorkbenchToStack(context,x,stacks,x.type)
        elif x.type == "codeblock":
            context.play(FadeOut(x.mobject),run_time=fastTime)
            handleCodeblockInWorkbench(context,stacks,x,workbench)
        elif x.type == "token":
            handleTokenInWorkbench(context,x,stacks,language,useUnused)
    if useUnused is True:
        print("disabled")
        # remains = []
        # leftoverTiles = VGroup(*map(lambda x: x.mobject, stacks["unused"]["contents"]))
        # context.play(leftoverTiles.animate.arrange(RIGHT).scale_to_fit_height(1).move_to(workbench),run_time=slowTime)
        # while len(stacks["unused"]["contents"]) > 0:
        #     leftover = stacks["unused"]["contents"].pop()
        #     remains.append(leftover)
        # while len(remains) > 0:
        #     restage = remains.pop()
        #     moveTokenFromWorkbenchToStack(context,restage,stacks,"exec")
        # processEveryItem(context,stacks,language,workbench,False)
