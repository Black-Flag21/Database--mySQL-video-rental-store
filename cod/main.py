from http import client

from flask import Flask, render_template, jsonify, request, redirect

import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_8")
from datetime import datetime

app = Flask(__name__)

with open(app.root_path + '\config.cfg', 'r') as f:
    app.config['ORACLE_URI'] = f.readline()

con_tns = cx_Oracle.makedsn('bd-dc.cs.tuiasi.ro', '1539', service_name='orcl')
try:
    con = cx_Oracle.connect('bd168', 'bd168', dsn=con_tns)

except Exception:
    print('Unexpected error')
else:
    print('Conexiune stabilita')


# employees begin code
@app.route('/')
@app.route('/clienti')
def clt():
    clienti = []

    cur = con.cursor()
    cur.execute('select * from clienti')
    for result in cur:
        client = {}
        client['id_client'] = result[0]
        client['serie_act_identitate'] = result[1]
        client['tip_act'] = result[2]
        client['nume'] = result[3]
        client['prenume'] = result[4]
        client['email'] = result[5]
        client['nr_telefon'] = result[6]
        client['data_nasterii'] = datetime.strptime(str(result[7]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')

        clienti.append(client)
    cur.close()
    return render_template('clienti.html', clienti=clienti)


# ------------------
@app.route('/clienti1')
def clt1():
    clienti = []

    cur = con.cursor()
    cur2 = con.cursor()
    cur.execute('select * from clienti ')
    for result in cur:
        client = {}
        client['id_client'] = result[0]
        client['serie_act_identitate'] = result[1]
        client['tip_act'] = result[2]
        client['nume'] = result[3]
        client['prenume'] = result[4]
        client['email'] = result[5]
        client['nr_telefon'] = result[6]
        client['data_nasterii'] = datetime.strptime(str(result[7]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')

        clienti.append(client)
    cur.close()
    return render_template('clienti.html', client=clienti)


@app.route('/addClient', methods=['GET', 'POST'])
def add_clt():
    error = None
    if request.method == 'POST':

        cur = con.cursor()
        values = []

        values.append("'" + request.form['id_client'] + "'")
        values.append("'" + request.form['serie_act_identitate'] + "'")
        values.append("'" + request.form['tip_act'] + "'")
        values.append("'" + request.form['nume'] + "'")
        values.append("'" + request.form['prenume'] + "'")
        values.append("'" + request.form['email'] + "'")
        values.append("'" + request.form['nr_telefon'] + "'")
        values.append("'" + datetime.strptime(str(request.form['data_nasterii']), '%Y-%m-%d').strftime('%d-%b-%y') + "'")

        fields = ['id_client', 'serie_act_identitate', 'tip_act', 'nume', 'prenume', 'email', 'nr_telefon',
                  'data_nasterii']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('clienti', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/clienti')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select id_client from clienti')
        for result in cur:
            cont_in.append(result[0])
        cur.close()
        cur = con.cursor()
        tip_act = []
        tip_act.append('CI')
        tip_act.append('Pasaport')

        return render_template('addClient.html', tip_act=tip_act)


@app.route('/delClient', methods=['POST'])
def del_clt():
    emp = request.form['id_client']
    cur = con.cursor()
    cur.execute('delete from contracte_inchirieri where id_client =' + emp)
    cur.execute('delete from clienti where id_client=' + emp)

    cur.execute('commit')
    return redirect('/clienti')


@app.route('/editClient', methods=['POST'])
def edit_clt():
    emp = 0

    cur = con.cursor()

    id_client = "'" + request.form['id_client'] + "'"
    serie_act_identitate = "'" + request.form['serie_act_identitate'] + "'"
    tip_act = "'" + request.form['tip_act'] + "'"
    nume = "'" + request.form['nume'] + "'"
    prenume = "'" + request.form['prenume'] + "'"
    cur.execute('select id_client from clienti where nume=' + nume)
    for result in cur:
        emp = result[0]
    cur.close()
    email = "'" + request.form['email'] + "'"
    nr_telefon = "'" + request.form['nr_telefon'] + "'"
    data_nasterii = "'" + datetime.strptime(str(request.form['data_nasterii']), '%Y-%m-%d').strftime('%d-%b-%y') + "'"

    cur = con.cursor()
    query = "UPDATE clienti SET id_client=%s, serie_act_identitate=%s, tip_act=%s, nume=%s, prenume=%s, email=%s, nr_telefon=%s, data_nasterii=%s where id_client=%s" % (
        id_client, serie_act_identitate, tip_act, nume, prenume, email, nr_telefon, data_nasterii, emp)
    cur.execute(query)
    cur.execute('commit')

    return redirect('/clienti')


@app.route('/getClient', methods=['POST'])
def get_clt():
    emp = request.form['id_client']
    cur = con.cursor()
    cur.execute('select * from clienti where id_client=' + emp)

    emps = cur.fetchone()
    id_client = emps[0]
    serie_act_identitate = emps[1]
    tip_act = emps[2]
    nume = emps[3]
    prenume = emps[4]
    email = emps[5]
    nr_telefon = emps[6]
    data_nasterii = datetime.strptime(str(emps[7]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
    cur.close()

    return render_template('editClient.html', id_client=id_client, serie_act_identitate=serie_act_identitate,
                           tip_act=tip_act, nume=nume, prenume=prenume, email=email, nr_telefon=nr_telefon,
                           data_nasterii=data_nasterii)


# Clienti end code
# -----------------------------------------#
# Detalii_film start code

@app.route('/detalii_film')
def Detalii():
    detalii_film = []

    cur = con.cursor()
    cur.execute('select * from Detalii_film')
    for result in cur:
        detalii = {}
        detalii['id_film'] = result[0]
        detalii['nume'] = result[1]
        detalii['gen_film'] = result[2]
        detalii['durata_min'] = result[3]
        detalii['an_aparitie'] = result[4]
        detalii['actor_principal'] = result[5]
        detalii['tip_film'] = result[6]
        detalii['restrictie_varsta'] = result[7]
        detalii['tarif'] = result[8]

        detalii_film.append(detalii)
    cur.close()
    return render_template('detalii_film.html', detalii_film=detalii_film)


@app.route('/addDetalii', methods=['GET', 'POST'])
def add_detalii():
    error = None
    if request.method == 'POST':

        cur = con.cursor()
        values = []

        values.append("'" + request.form['id_film'] + "'")
        values.append("'" + request.form['nume'] + "'")
        values.append("'" + request.form['gen_film'] + "'")
        values.append("'" + request.form['durata_min'] + "'")
        values.append("'" + request.form['an_aparitie'] + "'")
        values.append("'" + request.form['actor_principal'] + "'")
        values.append("'" + request.form['tip_film'] + "'")
        values.append("'" + request.form['restrictie_varsta'] + "'")
        values.append("'" + request.form['tarif'] + "'")

        fields = ['id_film', 'nume', 'gen_film', 'durata_min', 'an_aparitie', 'actor_principal', 'tip_film',
                  'restrictie_varsta', 'tarif']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('detalii_film', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/detalii_film')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select id_film from detalii_film')
        for result in cur:
            cont_in.append(result[0])
        cur.close()
        cur = con.cursor()
        tip_film = []
        tip_film.append('2D')
        tip_film.append('3D')

        varsta_min = []
        varsta_min.append('12')
        varsta_min.append('15')
        varsta_min.append('18')

        return render_template('addDetalii.html', tip_film=tip_film, varsta_min=varsta_min)


@app.route('/delDetalii', methods=['POST'])
def del_detalii():
    emp = request.form['id_film']
    cur = con.cursor()
    cur.execute('delete from detalii_film where id_film=' + emp)
    cur.execute('commit')
    return redirect('/detalii_film')


@app.route('/editDetalii', methods=['POST'])
def edit_detalii():
    emp1 = 0

    cur = con.cursor()

    id_film = "'" + request.form['id_film'] + "'"
    nume = "'" + request.form['nume'] + "'"
    cur.execute('select id_film from detalii_film where nume=' + nume)
    for result in cur:
        emp1 = result[0]
    cur.close()
    gen_film = "'" + request.form['gen_film'] + "'"
    durata_min = "'" + request.form['durata_min'] + "'"
    an_aparitie = "'" + request.form['an_aparitie'] + "'"
    actor_principal = "'" + request.form['actor_principal'] + "'"
    tip_film = "'" + request.form['tip_film'] + "'"
    restrictie_varsta = "'" + request.form['restrictie_varsta'] + "'"
    tarif = "'" + request.form['tarif'] + "'"

    cur = con.cursor()
    query = "UPDATE detalii_film SET id_film=%s, nume=%s, gen_film=%s, durata_min=%s, an_aparitie=%s, actor_principal=%s, tip_film=%s, restrictie_varsta=%s, tarif=%s where id_film=%s" % (
        id_film, nume, gen_film, durata_min, an_aparitie, actor_principal, tip_film, restrictie_varsta, tarif, emp1)
    cur.execute(query)
    cur.execute('commit')

    return redirect('/detalii_film')


@app.route('/getDetalii', methods=['POST'])
def get_detalii():
    emp = request.form['id_film']
    cur = con.cursor()
    cur.execute('select * from detalii_film where id_film=' + emp)

    emps = cur.fetchone()
    id_film = emps[0]
    nume = emps[1]
    gen_film = emps[2]
    durata_min = emps[3]
    an_aparitie = emps[4]
    actor_principal = emps[5]
    tip_film = emps[6]
    restrictie_varsta = emps[7]
    tarif = emps[8]
    cur.close()

    return render_template('editDetalii.html', id_film=id_film, nume=nume, gen_film=gen_film, durata_min=durata_min,
                           an_aparitie=an_aparitie, actor_principal=actor_principal, tip_film=tip_film,
                           restrictie_varsta=restrictie_varsta, tarif=tarif)


# Detalii_film end code
# -----------------------------------------#
# Contracte_inchirieri start code

@app.route('/contracte_inchirieri')
def Contract():
    contracte_inchirieri = []

    cur = con.cursor()
    cur.execute('select * from contracte_inchirieri')
    for result in cur:
        contracte = {}
        contracte['nr_contract'] = result[0]
        contracte['data_inchiriere'] = datetime.strptime(str(result[1]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        contracte['data_retur'] = datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        contracte['tarif'] = result[3]
        contracte['id_client'] = result[4]
        contracte['id_film'] = result[5]

        contracte_inchirieri.append(contracte)
    cur.close()
    return render_template('contracte_inchirieri.html', contracte_inchirieri=contracte_inchirieri)


@app.route('/addContract', methods=['GET', 'POST'])
def add_contract():
    error = None
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['nr_contract'] + "'")
        values.append("'" + datetime.strptime(str(request.form['data_inchiriere']), '%Y-%m-%d').strftime('%d-%b-%y') + "'")
        values.append("'" + datetime.strptime(str(request.form['data_retur']), '%Y-%m-%d').strftime('%d-%b-%y') + "'")

        values.append("'" + request.form['tarif'] + "'")
        values.append("'" + request.form['id_client'] + "'")
        values.append("'" + request.form['id_film'] + "'")

        fields = ['nr_contract', 'data_inchiriere', 'data_retur', 'tarif', 'id_client', 'id_film']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('contracte_inchirieri', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/contracte_inchirieri')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select nr_contract from contracte_inchirieri')
        for result in cur:
            cont_in.append(result[0])
        cur.close()

        return render_template('addContract.html')


@app.route('/delContract', methods=['POST'])
def del_contract():
    emp = request.form['nr_contract']
    cur = con.cursor()
    cur.execute('delete from contracte_inchirieri where nr_contract=' + emp)
    cur.execute('commit')
    return redirect('/contracte_inchirieri')


@app.route('/editContract', methods=['POST'])
def edit_contract():
    emp1 = 0

    cur = con.cursor()

    tarif = "'" + request.form['tarif'] + "'"
    cur.execute('select id_film from contracte_inchirieri where tarif=' + tarif)
    for result in cur:
        emp1 = result[0]
    cur.close()
    nr_contract = "'" + request.form['nr_contract'] + "'"
    data_inchiriere = "'" + request.form['data_inchiriere'] + "'"
    data_retur = "'" + request.form['data_retur'] + "'"
    id_client = "'" + request.form['id_client'] + "'"
    id_film = "'" + request.form['id_film'] + "'"

    cur = con.cursor()
    query = "UPDATE contracte_inchirieri SET nr_contract=%s, data_inchiriere=%s, data_retur=%s, tarif=%s, id_client=%s, id_film=%s where id_film=%s" % (
        nr_contract, data_inchiriere, data_retur, tarif, id_client, id_film, emp1)
    cur.execute(query)
    cur.execute('commit')

    return redirect('/contracte_inchirieri')


@app.route('/getContract', methods=['POST'])
def get_contract():
    emp = request.form['nr_contract']
    cur = con.cursor()
    cur.execute('select * from contracte_inchirieri where nr_contract=' + emp)

    emps = cur.fetchone()
    nr_contract = emps[0]
    data_inchiriere = emps[1]
    data_retur = emps[2]
    tarif = emps[3]
    id_client = emps[4]
    id_film = emps[5]

    cur.close()

    return render_template('editContract.html', nr_contract=nr_contract, data_inchiriere=data_inchiriere,
                           data_retur=data_retur, tarif=tarif,
                           id_client=id_client, id_film=id_film)


# Contracte_inchirieri end code
# -----------------------------------------#
# Film start code

@app.route('/film')
def fm():
    film = []

    cur = con.cursor()
    cur.execute('select * from film')
    for result in cur:
        f = {}
        f['id_film'] = result[0]
        f['buget'] = result[1]

        film.append(f)
    cur.close()
    return render_template('film.html', film=film)


@app.route('/addFilm', methods=['GET', 'POST'])
def add_film():
    error = None
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['id_film'] + "'")
        values.append("'" + request.form['buget'] + "'")

        fields = ['id_film', 'buget']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('film', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/film')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select id_film from film')
        for result in cur:
            cont_in.append(result[1])
        cur.close()

        return render_template('addFilm.html')


@app.route('/delFilm', methods=['POST'])
def del_film():
    emp = request.form['id_film']
    cur = con.cursor()
    cur.execute('delete from film where id_film=' + emp)
    cur.execute('commit')
    return redirect('/film')


# Film end code
# -----------------------------------------#
# Particularitati start code

@app.route('/particularitati')
def particularitati():
    particularitati = []

    cur = con.cursor()
    cur.execute('select * from particularitati')
    for result in cur:
        p = {}
        p['id_particularitati'] = result[0]
        p['Box_office'] = result[1]
        p['nume_regizor'] = result[2]
        p['companie_producatoare'] = result[3]

        particularitati.append(p)
    cur.close()
    return render_template('particularitati.html', particularitati=particularitati)


@app.route('/addParticularitati', methods=['GET', 'POST'])
def add_particularitati():
    error = None
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['id_particularitati'] + "'")
        values.append("'" + request.form['Box_office'] + "'")
        values.append("'" + request.form['nume_regizor'] + "'")
        values.append("'" + request.form['companie_producatoare'] + "'")

        fields = ['id_particularitati', 'Box_office', 'nume_regizor', 'companie_producatoare']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('particularitati', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/particularitati')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select id_particularitati from particularitati')
        for result in cur:
            cont_in.append(result[1])
        cur.close()

        return render_template('addParticularitati.html')


@app.route('/delParticularitati', methods=['POST'])
def del_particularitati():
    emp = request.form['id_particularitati']
    cur = con.cursor()
    cur.execute('delete from particularitati where id_particularitati=' + emp)
    cur.execute('commit')
    return redirect('/particularitati')


# Particularitati end code
# -----------------------------------------#
# Particularitati-Film start code


@app.route('/film_particularitati')
def film_particularitati():
    film_particularitati = []

    cur = con.cursor()
    cur.execute('select * from film_particularitati')
    for result in cur:
        fp = {}
        fp['id_film'] = result[0]
        fp['id_particularitati'] = result[1]

        film_particularitati.append(fp)
    cur.close()
    return render_template('film_particularitati.html', film_particularitati=film_particularitati)


@app.route('/addFilm_particularitati', methods=['GET', 'POST'])
def add_film_particularitati():
    error = None
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['id_film'] + "'")
        values.append("'" + request.form['id_particularitati'] + "'")

        fields = ['id_film', 'id_particularitati']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('film_particularitati', ', '.join(fields), ', '.join(values))

        cur.execute(query)
        cur.execute('commit')
        return redirect('/film_particularitati')
    else:
        cont_in = []
        cur = con.cursor()
        cur.execute('select id_film from film_particularitati')
        for result in cur:
            cont_in.append(result[1])
        cur.close()

        return render_template('film_particularitati.html')


@app.route('/delFilm_particularitati', methods=['POST'])
def del_film_particularitati():
    emp = request.form['id_film']
    cur = con.cursor()
    cur.execute('delete from film_particularitati where id_film=' + emp)
    cur.execute('commit')
    return redirect('/film_particularitati')


# main
if __name__ == '__main__':
    app.run(debug=True)
    con.close()
