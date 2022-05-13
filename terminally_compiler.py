import re
def get_start_line():
    with open("gui.py", 'r') as f:
        for i, line in enumerate(f.readlines()):
            if line == "# {COMPILE FROM HERE}\n":
                return i
def get_read_content(fname,classname):
    class_txt = ""
    import_statements = ""
    classname_re = re.compile(r'^class ' + classname + r'\([^)]*\):')
    import_re = re.compile("^(?:from (?:[A-z\.])+ )?import (?:[A-z ,*])+$")
    print_smt = re.compile("( print\()")
    # tabs_re = re.compile(r"^(\t)")
    with open(fname,'r') as f:
        file = f.read().split('\n')
        for i, line in enumerate(file):
            if import_re.search(line) is not None:
                import_statements += line + '\n'
            if classname_re.search(line) is not None:
                class_txt += line + '\n'
                for line in file[i+1:]:
                    num_tabs = 0
                    for i, char in enumerate(line,1):
                        # print(char)
                        if char != '\t':
                            if char != ' ':
                                break
                            if i % 4 == 0:
                                num_tabs += 1
                        else:
                            num_tabs += 1
                    else:
                        num_tabs = 1
                    if num_tabs == 0:
                        break
                    else:
                        class_txt += print_smt.sub(" ROOT.maintab.output(",line) + '\n'
    return class_txt, import_statements
def write_copy(read_fname, write_fname, write_content,):
    if read_fname == write_fname:
        raise Exception("attempted to write to read file")
    with open(read_fname,'r') as rf:
        with open(write_fname,'w') as wf:
            for i, line in enumerate(rf.readlines()):
                if line == "# {COMPILE FROM HERE}\n":
                    wf.write(write_content)
                else:
                    wf.write(line)
TO_IMPORT = [
    ("packages/test.py","myclass"),
    ("packages/name_ager.py","name_ager"),
]
# start_line = get_start_line()
import_statements = ""
class_txt = ""
classes = "CLASSES = {"
for tupleobj in TO_IMPORT:
    a,b = get_read_content(tupleobj[0],tupleobj[1])
    class_txt += a
    import_statements += b
    classes += "'%s':%s," % (tupleobj[1],tupleobj[1])
class_txt = import_statements + class_txt + '\n\n' + classes[:-1] + '}\n'
write_copy("gui.py","compiled_gui.py",class_txt)