from Part1 import Read, Operations
from flask import *

'''Creates a flask instance that includes the variable name which takes the 'main' value when the code is excecuted'''
myapp = Flask(__name__)

'''Create objects of type Operations neccessary to call registry functions of part 1.'''
data_g = Operations('Gene')
data_d = Operations('Disease')

'''Declaring the route of the homepage, in which all the hyperlinks leading to specific operations are shown.
The hyperlinks and the content of the 'homepage' are written in the 'index.html' file.'''
@myapp.route('/')
def homepage():
    return render_template('index.html')

'''This route displays the 1st operation carried out by part 2.
We set two variables 'shape_1' and 'shape_2' each one calling the key 'Shape', paired with the value of Part 1 registry 
that contains the Part 2 operation. 'Sh_1 ' and 'Sh_2' are references for the jinja2 part in the template.
In the webpage there are shown the Numerical Metadata of each data collection.'''
@myapp.route('/shapes')
def shapes():  
    shape_1 = data_g.oper_No('Shape')
    shape_2 = data_d.oper_No('Shape')
    return render_template('shape.html', Sh_1=shape_1, Sh_2=shape_2)

'''This route displays the 2nd operation carried out by part 2.
We set two variables 'semantics_1' and 'semantics_2' each one calling the key 'Semantics', paired with the value of Part 1 registry 
that contains the Part 2 operation. 'Sem1 ' and 'Sem2' are references for the jinja2 part in the template.
In the webpage there are shown the general semantics of each data collection.'''
@myapp.route('/semantics')
def semantics():
    semantics_1 = data_g.oper_No('Semantics')
    semantics_2 = data_d.oper_No('Semantics')
    return render_template('sem.html', Sem1=semantics_1, Sem2=semantics_2)

'''This route displays the 3rd operation carried out by part 2.
We set a variable 'result' that calls the key 'ID' paired with the value of Part 1 registry that contains 
the Part 2 operation. 'choice_1' is a reference for the jinja2 part in the template and allows to use the same template
also for the homologous operation for the diseases.
In the webpage is shown the list of genes present in the data collection.'''
@myapp.route('/list.genes')
def list_genes():
    result = data_g.oper_No('ID')
    chose_1 = 'genes'
    return render_template('id.html', CHOSE=chose_1, RESULT=result)

'''This route displays the 5th operation carried out by part 2.
We set a variable 'result' that calls the key 'ID' paired with the value of Part 1 registry that contains 
the Part 2 operation. 'choice_2' is a reference for the jinja2 part in the template.
In the webpage is shown the list of diseases present in the data collection.'''
@myapp.route('/list.diseases')
def list_disease():
    result = data_d.oper_No('ID')
    chose_2 = 'diseases'
    return render_template('id.html', CHOSE=chose_2, RESULT=result)

'''This route displays the form in which the user chooses the gene of interest, by providing its ID or Symbol.
We set a variable 'gene' which allows us to use the same template here as well as with the homologous 
operation performend on disesase '''
@myapp.route('/sentences.Gene')
def g_sentences():
    gene = 'Gene'
    return render_template('sentences_inputs.html', CHOICE=gene)

'''This route displays the result of the 4th operation, carried out by part 2.
The key comand of this function is the method 'POST' which allows us to access the data of the HTML form.
We set again the variable 'gene' needed for template reuse, as well as 'result' which calls the key 'COVID-symbol' 
paired with the value of Part 1 registry that contains the Part 2 operation. We apply 
'request.form.get('name of the choices in form), to access the input provided by user. 'filt' variable will 
be used as indicator for the filter, while 'inp' as a value for the key.
In the webpage there would appear the list of all sentences that provide an evidence about possible relation between 
COVID and gene of interest. If no correlation found or the input is not valid, the webpage displays an error message.'''
@myapp.route('/sentences.Gene.result', methods=['POST'])
def gs_results():
    gene = 'Gene'
    filt = request.form.get('choice')
    inp = request.form.get('keyword')
    if filt == 'Symbol':
        data_g.set_it(4)
        data_g.set_key(inp)
    else:
        data_g.set_it(0)
        data_g.set_key(inp)
    result = data_g.oper_Yes('COVID-symbol')
    return render_template('sentences_results.html', CHOICE=gene, RESULT=result)

'''This route displays the form in which the user chooses the disease of interest, by providing its ID or Name.
We set a variable 'disease' which allows us to use the same template here as well as with the homologous 
operation performend on genes '''
@myapp.route('/sentences.Disease')
def d_sentences():
    disease = 'Disease'
    return render_template('sentences_inputs.html', CHOICE=disease)

'''This route displays the result of the 6th operation, carried out by part 2.
The key comand of this function is the method 'POST' which allows us to access the data of the HTML form.
We set again the variable 'disease' needed for template reuse, as well as 'result' which calls the key 'COVID-symbol' 
paired with the value of Part 1 registry that contains the Part 2 operation. We apply 
'request.form.get('name of the choices in form), to access the input provided by user. 'filt' variable will 
be used as indicator for the filter, while 'inp' as a value for the key.
In the webpage there would appear the list of all sentences that provide an evidence about possible relation between 
COVID and disease of interest. If no correlation found or the input is not valid, the webpage displays an error message. '''
@myapp.route('/sentences.Disease.result', methods=['POST'])
def ds_results():
    disease = 'Disease'
    filt = request.form.get('choice')
    inp = request.form.get('keyword')
    if filt == 'Symbol':
        data_d.set_it(4)
        data_d.set_key(inp)
    else:
        data_d.set_it(0)
        data_d.set_key(inp)
    result = data_d.oper_Yes('COVID-symbol')
    return render_template('sentences_results.html', CHOICE=disease, RESULT=result)

'''This route displays the 7th operation, carried out by Part 2.
 We set a variable 'top' which inserts in the template the result of the operation with key 'Top' 
 in the Part 1 registry. The result is directly displayed in the webpage by the template.'''
@myapp.route('/top10')
def top_10():
    top = data_g.oper_No('Top')
    return render_template('top.html', TOP=top)


'''This route displays the form in which the user choses the gene of interest, by providing its ID or Name.
We set a variable 'Gene' which allows us to use the same template here as well as with the homologous 
operation performend on diseases '''
@myapp.route('/associations.gene')
def g_association():
    gene = 'Gene'
    return render_template('association_inputs.html', CHOICE=gene)

'''This route displays the result of the 8th operation, carried out by part 2.
The key command of this function is the method 'POST' which allows us to access the data of the HTML form.
We set again the variable 'gene' and 'other' needed for template reuse, as well as 'result' which calls the key 'Association' 
paired with the value of Part 1 registry that contains the Part 2 operation. We apply 
'request.form.get('name of the choices in form), to access the input provided by user. 'filt' variable will 
be used as indicator for the filter, while 'inp' as a value for the key.
In the webpage there would appear the list of all diseases related to the gene of interest.
If no correlation found or the input is not valid, the webpage displays an error message. '''
@myapp.route('/associations.Gene.result', methods=['POST'])
def g_ass_results():
    gene = 'gene'
    other = 'Diseases'
    filt = request.form.get('choice')
    inp = request.form.get('keyword')
    if filt == 'Symbol':
        data_g.set_it(4)
        data_g.set_key(inp)
    else:
        data_g.set_it(0)
        data_g.set_key(inp)
    result = data_g.oper_Yes('Association')
    return render_template('associations_results.html', CHOICE=gene, RESULT=result, OTHER=other)


'''This route displays the form in which the user choses the disease of interest, by providing its ID or Name.
We set a variable 'Disease' which allows us to use the same template here as well as with the homologous 
operation performend on genes '''
@myapp.route('/associations.disease')
def d_association():
    disease = 'Disease'
    return render_template('association_inputs.html', CHOICE=disease)

'''This route displays the result of the 9th operation, carried out by part 2.
The key command of this function is the method 'POST' which allows us to access the data of the HTML form.
We set again the variable 'disease' and 'other' needed for template reuse, as well as 'result' which calls the key 'Association' 
paired with the value of Part 1 registry that contains the Part 2 operation. We apply 
'request.form.get('name of the choices in form), to access the input provided by user. 'filt' variable will 
be used as indicator for the filter, while 'inp' as a value for the key.
In the webpage there would appear the list of all genes related to the disease of interest.
If no correlation found or the input is not valid, the webpage displays an error message. '''
@myapp.route('/associations.Disease.result', methods=['POST'])
def d_ass_results():
    disease = 'disease'
    other = 'Genes'
    filt = request.form.get('choice')
    inp = request.form.get('keyword')
    if filt == 'Symbol':
        data_d.set_it(4)
        data_d.set_key(inp)
    else:
        data_d.set_it(0)
        data_d.set_key(inp)
    result = data_d.oper_Yes('Association')
    return render_template('associations_results.html', CHOICE=disease, RESULT=result, OTHER=other)

'''In order to start using the Software please run the program from this module.
NOTE: the Software exploit external libraries such as flask.py and pandas.py, thus they must be already installed in the machine
before running it. '''
if __name__ == '__main__':
    myapp.run(debug=True)
