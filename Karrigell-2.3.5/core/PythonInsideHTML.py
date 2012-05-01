""" Decodes Python Inside HTML into Python scripts
The script is provided through the pythonCode() method

A PIH page is made of :
- normal HTML code
- Python statements : syntax <% (Python statements) %>
    For instance :
        <%
        for i in range(10):
            print i
        %>
    It must be valid Python code, with correct identation
- Python variables or expressions <%= (Python variable) %>
    For instance :
        <h1>Current directory is <%= os.getcwd() %> </h1>
        
- strings or variables which should be translated  <%_ (string) %>
    example : <%_ "bold" %> or <%_ name %>

INDENTATION

A PIH file is converted into Python code, which must be indented
according to Python rules ; whereas in normal HTML indentation is
used only for readability

So beware if you mix Python and HTML :

   1 <% for i in range(10): %>
   2 <%= i %>*<%= i %> : <b> <%= i*i %> </b>
   
   this will work because after a loop or a condition the following HTML
   is automatically indented by PIH
   
To decrement indentation, use <% end %> :
   
   1 <% for i in range(10): %>
   2 <%= i %>*<%= i %> : <b> <%= i*i %> </b>
   3 <% end %>
   4 <h3>done</h3>

    in this example, "done" will be written after the for loop is finished

Another example for an if... else... :
   1 <% if i: %>
   2   output someting
   3 <% end %>
   4 <% else: %>
   5   output someting else
   6 <% end %>
   7 <h3>done</h3>
   
   (don't forget the last <% end %> otherwise "done" would have the same
   indentation as line 5)
   
But this :

   1 <% for i in range(10): 
   2    print '%s * %s' %(i,i) %>
   3    <b> <%= i*i %> </b>
   4 <h3>done</h3>
   
   won't work, because after the print statement on line 2 indentation 
   goes back to 0 (it begins with plain HTML)

THE <INDENT> TAG
   
If you have complex code where Python and HTML are mixed, embed it
between the tags <indent> and </indent> :

   1  <indent>
   2  <% for i in range(10): 
   3    print '%s * %s' %(i,i) %>
   4    <b> <%= i*i %> </b>
   5  </indent>
   6  <h3>Table</h3>
   7  <table>
   8    <tr>
   9      <td>A cell</td>
   10   </tr>
   11 </table>
   
   <indent> means : from now on, and until the matching </indent> tag,
   use the indentation in PIH source and leave it as it is to produce 
   Python  code
   In the above example, indentation is used until line 5 and ignored 
   afterwards
   
   If the <indent> tag itself is indented, the following code is indented
   relatively to it :
   
   1   <table border=1>
   2     <tr>
   3       <th>Number</th>
   4       <th>Square</th>
   5     </tr>
   6     <indent>
   7     <% for i in range(10): %>
   8       <tr>
   9       <td><% print i %></td>
   10      <td><% print i**2 %></td>
   11      </tr>
   12    </indent>
   13  </table>

    In line 7, <% is aligned on <indent> so the Python code will not be
    indented
    

If you want to exit the script before the end of the document, raise a 
SCRIPT_END exception
    raise SCRIPT_END,message

See examples in the demo directory

The lineMapping dictionary maps the line numbers in the destination file 
(Python code) to line number in original file (.pih code) ; used for traceback"""

import os,string,cStringIO,re,sys
import traceback,tempfile,webbrowser

from k_stringio import KStringIO as StringIO

from k_encodings import k_encoding

import k_config

startIndent=re.compile("<\s*indent\s*>",re.IGNORECASE)
endIndent=re.compile("<\s*/indent\s*>",re.IGNORECASE)

class PIH_ParseError(Exception):

    def __init__(self,value):
        self.msg=value[0]
        self.errorLine=value[1]
        
    def __str__(self):
        return self.msg
        
class PIH:

    endTag={"<%":"%>","<%=":"%>","<%_":"%>","<%%":"%%>"}

    def __init__(self,fileName=None):
        self.fileName=fileName
        self.defaultEncoding=k_config.outputEncoding
        if fileName:
            fileObject=open(fileName)
            self.parse(fileObject)
        
    def parse(self,fileObject):
        """Parses the PIH code in the file object open for reading"""   
        sourceCode=fileObject.readlines()
        sourceCode=map(self.stripCRLF,sourceCode)
        sourceCode=string.join(sourceCode,'\n')
        self.sourceCode=sourceCode+'\n'
        # normalize <indent> tag
        self.pihCode=startIndent.sub("<indent>",self.sourceCode)
        self.pihCode=endIndent.sub("</indent>",self.pihCode)

        self.pointer=0
        self.indentation="off"
        self.indent=0
        self.defaultIndentation=0
        self.startHTML=self.endHTML=0
        self.sourceLine=0   # current line in source code
        self.lineMapping={} # maps lines in resulting Python code to original line
        self.output=cStringIO.StringIO() # cStringIO because this is a raw python code
                                         # we are assembling
        self.output.write("import sys\n")
        self.destLine=1 # first line with an origin in pih code
        while self.pointer<len(self.pihCode):
            rest=self.pihCode[self.pointer:]
            if rest.startswith("<indent>"):
                # start a part where indentation is on
                self.flushHTML()
                self.indentation="on"
                self.defaultIndentation=self.getAbsLineIndent(self.pointer)
                self.pointer=self.pointer+8
                self.startHTML=self.pointer
            elif rest.startswith("</indent>"):
                # ends a part where indentation is on
                self.flushHTML()
                self.indentation="off"
                self.indent=0
                self.pointer=self.pointer+9
                self.startHTML=self.pointer
            elif rest.startswith("<%=") or rest.startswith("<%_"):
                # inserting a variable or string to translate
                # translates a variable as sys.stdout.write(variable)
                # and a string to translate as sys.stdout.write(_(translated))
                # a variable can be on several lines
                tag=self.pihCode[self.pointer:self.pointer+3]
                taggedCode,start,end=self.initTag(tag)
                taggedCode=string.strip(taggedCode)
                if self.indentation=="on":
                    self.indent=self.getLineIndent(self.pointer)
                self.output.write(" "*4*self.indent)
                if tag=="<%=":
                    # this will break with non-ascii strings intended
                    # as original phrases for gettext
                    # fortunately, everyone uses English as the original
                    # if not, we'll wait for the bugreports :-/
                    self.output.write('sys.stdout.write(str(')
                else:
                    self.output.write('sys.stdout.write(_(')
                startLineNum=self.getLineNum(start)
                varCodeLines=string.split(taggedCode,"\n")
                for i in range(len(varCodeLines)):
                    line=varCodeLines[i]
                    if not string.strip(line):
                        continue
                    line=string.rstrip(line)
                    if i!=0:
                        self.output.write(" "*4*self.indent)
                    self.output.write(line)
                    if i !=len(varCodeLines)-1:
                        self.output.write("\n")
                    self.lineMapping[self.destLine]=startLineNum+i
                    self.destLine+=1
                self.output.write("))\n")
                self.pointer=end
                self.startHTML=self.pointer
            elif rest.startswith("<%"):
                # inserting Python statements
                pythonCode,pythonStart,pythonEnd=self.initTag("<%")
                startLineNum=self.getLineNum(pythonStart)
                if string.lower(string.strip(pythonCode))=="end":
                    # if <% end %>, only decrement indentation
                    self.indent-=1
                else:
                    pythonCodeLines=string.split(pythonCode,"\n")
                    for i in range(len(pythonCodeLines)):
                        line=pythonCodeLines[i]
                        if not string.strip(line):
                            continue
                        if i==0:
                            self.indent=self.getLineIndent(self.pointer)
                            if self.indentation=="off":
                                self.indent1=self.getAbsLineIndent(self.pointer)
                        else:
                            self.indent=self.getIndent(line)
                        if self.indentation=="on":
                            line=string.strip(line)
                        elif i>0:
                            # if not under <indent>, removes the same heading whitespace
                            # as the first line
                            j=0
                            while line and line[j] in string.whitespace:
                                j+=1
                            if j<self.indent1:
                                errorLine=startLineNum+i+1
                                errMsg="Indentation error :\nline %s"
                                errMsg+=" can't be less indented than line %s"
                                raise PIH_ParseError, [errMsg \
                                    %(errorLine,startLineNum+1),errorLine-1]
                            line=" "*4*(j-self.indent1)+line.strip()
                        self.output.write(" "*4*self.indent)
                        self.output.write(string.rstrip(line)+"\n")
                        self.lineMapping[self.destLine]=startLineNum+i
                        self.destLine+=1
                    if self.indentation=="off":
                        if line.strip().endswith(":"):
                            self.indent+=1
                self.pointer=pythonEnd
                self.startHTML=self.pointer
            else:
                self.pointer=self.pointer+1
                self.endHTML=self.pointer
        self.flushHTML()
        if self.defaultEncoding:
            # now we can guess the encoding of output...
            val = self.output.getvalue()
            enc = k_encoding.guess_buffer_encoding(val, self.defaultEncoding)
            # this is ugly, but unfortunately exec cannot take unicode strings,
            # neither can be told about encoding the code is using
            # so we have to do it this way...
            self.output=cStringIO.StringIO() 
            self.output.write("# -*- coding: %s -*-\n" % enc.pyencoding)
            self.output.write(val)
            self.lineMapping = dict([(k+1,v) 
                            for (k,v) in self.lineMapping.iteritems()])

    def stripCRLF(self,line):
        while line and line[-1] in ['\r','\n']:
            line=line[:-1]
        return line

    def initTag(self,tag):
        """Search the closing tag matching +tag+, move pointer
        and flush current HTML
        """
        tagEnd=string.find(self.pihCode,self.endTag[tag],self.pointer)
        if tagEnd<0:
            errorLine=self.getLineNum(self.pointer)+1
            raise PIH_ParseError, \
                ["unclosed %s tag in line %s" %(tag,errorLine),errorLine]
        # flushes existing html
        self.flushHTML()
        start=self.pointer+len(tag)
        while self.pihCode[start] in string.whitespace:
            start=start+1
        code=self.pihCode[start:tagEnd]
        end=tagEnd+len(self.endTag[tag])
        return code,start,end

    def flushHTML(self):
        """Flush aggregated HTML"""
        html=self.pihCode[self.startHTML:self.endHTML]
        if html:
            htmlLines=string.split(html,"\n")
            p=self.startHTML
            for i,htmlLine in enumerate(htmlLines):
                if htmlLine:
                    if self.indentation=="on":
                        self.indent=self.getLineIndent(p)
                    out=htmlLine
                    #if i>0:
                    #   out=string.lstrip(htmlLine) # strips indentation
                    out=string.replace(out,"\\",r"\\")
                    out=string.replace(out,"'",r"\'")
                    out=string.replace(out,'"',r'\"')
                    if out:
                        if i==len(htmlLines)-1 and not out.strip():
                            # if last HTML chunk is whitespace, ignore
                            # (must be the indentation of next Python chunk)
                            break
                        if i!=len(htmlLines)-1:
                            out=out+'\\n'
                        self.output.write(" "*4*self.indent)
                        self.output.write('sys.stdout.write("%s")\n' %out)
                        self.lineMapping[self.destLine]=self.getLineNum(p)
                        self.destLine+=1
                p=p+len(htmlLine)+1

    def getLineNum(self,pointer):
        return string.count(self.pihCode,"\n",0,pointer)

    def nextNoSpace(self,p):
        while p<len(self.pihCode) and self.pihCode[p] in [' ','\t']:
            p=p+1
        return p
    
    def countLeadingTabs(self,line):
        res=0
        while res<len(line) and line[res] in ["\t"," "]:
            res+=1
        return res

    def getIndent(self,line):
        if self.indentation=="off":
            return self.indent
        else:
            i=0
            while i<len(line) and line[i] in string.whitespace:
                i=i+1
            return i-self.defaultIndentation

    def getAbsLineIndent(self,pointer):
        """Get the absolute indentation of the line where +pointer+ is"""
        p=pointer
        while p>0 and self.pihCode[p]!="\n":
            p=p-1
        p=p+1
        indent=0
        while p<len(self.pihCode) and self.pihCode[p] in string.whitespace:
            p+=1
            indent+=1
        return indent

    def getLineIndent(self,pointer):
        """Returns indentation of the line which includes the position
        +pointer+ in self.pihCode
        If we're under <indent>, indentation is relative to 
        self.defaultIndentation"""
        if self.indentation=="on":
            self.indent=self.getAbsLineIndent(pointer)-self.defaultIndentation
        return self.indent
    
    def pythonCode(self):
        """Returns Python code as a string"""
        return self.output.getvalue()

    def getLineMapping(self):
        return self.lineMapping
    
    def trace(self,data):
        sys.stderr.write("%s\n" %data)

if __name__=="__main__":
    import PIHapp