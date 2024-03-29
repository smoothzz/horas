from flask import Flask, request, render_template, session, redirect, url_for, flash
from auth import login_required
from settings import app, crypt, db
from models import users, registro_horas, sites
import datetime
from datetime import datetime as dt
from datetime import timedelta


@app.before_request
def set_session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["POST", "GET"])    
@login_required         
def home():
    if request.method == "POST":
        mindate = request.form["mindate"]
        maxdate = request.form["maxdate"]
        if mindate > maxdate:
            flash('Data inicial não pode ser maior que data final', 'error')
            return redirect(url_for("home"))
        if not mindate and not maxdate:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=session['login']).order_by(registro_horas.date.desc()).paginate(per_page=10)
            return render_template("index.html", registros=registros)
        else:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=session['login']).filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            return render_template("index.html", registros=registros)
    else:
        page = request.args.get('page', 1, type=int)
        registros = registro_horas.query.filter_by(login=session['login']).order_by(registro_horas.date.desc()).paginate(per_page=10)
        return render_template("index.html", registros=registros)

@app.route("/registros", methods=["POST", "GET"])    
@login_required         
def registros():
    if session["user_type"] != 3:
        flash("Apenas usuários de nível elevado podem acessar essa página!", "error")
        return redirect(url_for('home'))
    if request.method == "POST":
        mindate = request.form["mindate"]
        maxdate = request.form["maxdate"]
        login = request.form["user"]
        aonde = request.form["aonde"]
        if not mindate and not maxdate and not login and not aonde:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if mindate and not maxdate and not login and not aonde:
            flash('Você precisa definir a data final para gerar um intervalo de tempo!', 'error')
            return redirect(url_for("registros"))
        if maxdate and not mindate and not login and not aonde:
            flash('Você precisa definir a data inicial para gerar um intervalo de tempo!', 'error')
            return redirect(url_for("registros"))
        if mindate > maxdate and not login and not aonde:
            flash('Data inicial não pode ser maior que data final', 'error')
            return redirect(url_for("registros"))
        if mindate > maxdate and not login and aonde:
            flash('Data inicial não pode ser maior que data final', 'error')
            return redirect(url_for("registros"))
        if mindate > maxdate and login and not aonde:
            flash('Data inicial não pode ser maior que data final', 'error')
            return redirect(url_for("registros"))
        if login and aonde and mindate > maxdate:
            flash('Data inicial não pode ser maior que data final', 'error')
            return redirect(url_for("registros"))
        if not mindate and not maxdate and not login and aonde:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(aonde=aonde).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if not mindate and not maxdate and login is not None and not aonde:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=login).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if not mindate and not maxdate and login is not None and aonde is not None:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=login,aonde=aonde).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if mindate and maxdate and not login and not aonde:
            page = request.args.get('page', 1, type=int)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            registros = registro_horas.query.filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            return render_template("registros.html", registros=registros, sites=unidades)
        if mindate and maxdate and login is not None and not aonde:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=login).filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if mindate and maxdate and not login and aonde:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(aonde=aonde).filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        if mindate and maxdate and login is not None and aonde is not None:
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=login,aonde=aonde).filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registros.html", registros=registros, sites=unidades)
        else:
            page = request.args.get('page', 1, type=int)
            unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            registros = registro_horas.query.filter(registro_horas.date.between(mindate, maxdate)).order_by(registro_horas.date.desc()).paginate(per_page=10)
            return render_template("registros.html", registros=registros, sites=unidades)
    else:
        page = request.args.get('page', 1, type=int)
        registros = registro_horas.query.order_by(registro_horas.date.desc()).paginate(per_page=10)
        unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("registros.html", registros=registros, sites=unidades)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        found_user = users.query.filter_by(login=request.form["login"]).first()
        if not found_user:
            flash('Dados inválidos, favor procurar pelo seu analista.', 'error')
            return redirect(url_for('login'))
        if crypt.check_password_hash(found_user.password, request.form["password"]) == False:
            flash('Dados inválidos, favor procurar pelo seu analista.', 'error')
            return redirect(url_for('login'))
        if found_user.active == 0:
            flash('Dados inválidos, favor procurar pelo seu analista.', 'error')
            return redirect(url_for('login'))            
        else:
            session["logged_in"] = True
            session["login"] = found_user.login
            session["user_type"] = found_user.level
            return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/logout")    
@login_required         
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    if session["user_type"] != 3:
        flash("Apenas usuários de nível elevado podem acessar essa página!", "error")
        return redirect(url_for('home'))
    if request.method == "POST":
        search = users.query.filter_by(login=request.form["login"]).first()
        if search is not None:
            flash("Login já existente na base de dados!", "error")
            return redirect(url_for('register'))
        user=users(name=request.form["name"].upper(),login=request.form["login"],email=request.form["email"],password = request.form["password"],site=request.form["aonde"].upper(),level=request.form["level"],active = 1, created_at=dt.now(), updated_at=dt.now())
        db.session.add(user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("register.html", unidades=unidades)
    else:
        unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("register.html", unidades=unidades)

@app.route("/registrarhora", methods=["POST", "GET"])
@login_required  
def register_hora():
    if request.method == "POST":
        hora_inicio = request.form["initial_time"]
        hora_pausa = request.form["pause_launch"]
        hora_volta = request.form["back_launch"]
        hora_final = request.form["final_time"]
        motivo = request.form["motivo"]
        date = request.form["date"]
        aonde = request.form["aonde"]
        if not date:
            flash("Campo data deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not motivo:
            flash("Campo motivo deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not aonde:
            flash("Campo em qual site deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_inicio:
            flash("Campo Inicio Hora deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_final:
            flash("Campo Horario final deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_pausa and not hora_volta:
            hora_pausa = '00:00'
            hora_volta = '00:00'
            time1 = datetime.datetime.strptime(hora_inicio, '%H:%M')
            time4 = datetime.datetime.strptime(hora_final, '%H:%M')
            if time1 > time4:
                flash("Horário final não pode ser maior que horário de início!", 'error')
                return render_template("registrar-hora.html")
            somatotal = time4 - time1
            horas=registro_horas(login=session["login"],date=request.form["date"],aonde=aonde,motivo=request.form["motivo"],initial_time=request.form["initial_time"],pause_launch=request.form["pause_launch"],back_launch=request.form["back_launch"],final_time=request.form["final_time"],total_time=somatotal, done=0, created_at=dt.now(), updated_at=dt.now())
            db.session.add(horas)
            db.session.commit()
            flash("Dados registrados!", 'success')
            registros = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
            return render_template("registrar-hora.html", registros=registros)
        else:
            time1 = datetime.datetime.strptime(hora_inicio, '%H:%M')
            time2 = datetime.datetime.strptime(hora_pausa, '%H:%M')
            time3 = datetime.datetime.strptime(hora_volta, '%H:%M')
            time4 = datetime.datetime.strptime(hora_final, '%H:%M')
            if time1 > time2:
                flash("Horário de saída almoço não pode ser menor que horário de início!", 'error')
                return render_template("registrar-hora.html")
            if time3 < time2:
                flash("Horário da volta almoço não pode ser maior que horário de saída almoço!", 'error')
                return render_template("registrar-hora.html")
            if time3 > time4:
                flash("Horário da volta almoço não pode ser menor que horário final!", 'error')
                return render_template("registrar-hora.html")
            else:
                soma1 = time2 - time1
                soma2 = time4 - time3
                somatotal = soma1 + soma2
                horas=registro_horas(login=session["login"],date=request.form["date"],aonde=aonde,motivo=request.form["motivo"],initial_time=request.form["initial_time"],pause_launch=request.form["pause_launch"],back_launch=request.form["back_launch"],final_time=request.form["final_time"],total_time=somatotal, done=0, created_at=dt.now(), updated_at=dt.now())
                db.session.add(horas)
                db.session.commit()
                flash("Dados registrados!", 'success')
                registros = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
                return render_template("registrar-hora.html", registros=registros)
    else:
        registros = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("registrar-hora.html", registros=registros)
    
@app.route("/unidades", methods=["POST", "GET"])    
@login_required         
def unidades():
    if request.method == "POST":
        unidade = request.form["unidade"].upper()
        search = bool(sites.query.filter_by(unidade=unidade).first())
        if search == True:
            flash("Unidade já cadastrada", 'error')
            return render_template("unidades-np.html")
        if not unidade:
            flash("Nome para unidade deve ser preenchido", 'error')
            return render_template("unidades-np.html")
        else:
            query=sites(unidade=unidade,ativo=1,created_at=dt.now())
            db.session.add(query)
            db.session.commit()
            flash("Unidade cadastrada com sucesso", 'success')
            return redirect(url_for('unidades'))
    else:
        site = sites.query.order_by(sites.unidade.asc())
        return render_template("unidades-np.html", sites=site)

@app.route("/edit_registro/<int:reg_id>", methods=["POST", "GET"])
@login_required
def edit_registro(reg_id):
    registro_id = id

@app.route('/delete/<id>/', methods=['POST'])
@login_required
def delete_registro(id):
    search = registro_horas.query.get(id)
    if search is None:
        flash("Falha ao consultar Registro", "error")
        return redirect(url_for("home"))
    if search.done == True:
        flash("Esse registro não pode ser deletado pois já foi concluído pela coordenação!", "error")
        return redirect(url_for("home"))
    else:
        flash("Registro excluido com sucesso!", "success")
        db.session.delete(search)
        db.session.commit()
        return redirect(url_for("home"))

@app.route('/edit/<id>/', methods=["POST", "GET"])
@login_required
def update_registro(id):
    search = registro_horas.query.get(id)
    if search is None:
        flash("Falha ao consultar Registro", "error")
        return redirect(url_for("home"))
    if search.done == True:
        flash("Esse registro não pode ser editado pois já foi concluído pela coordenação!", "error")
        return redirect(url_for("home"))
    if search.login != session['login']:
        flash("Você sô pode editar um registro que seja de sua autoria!", "error")
        return redirect(url_for("home"))
    if request.method == "POST":
        hora_inicio = request.form["initial_time"]
        hora_pausa = request.form["pause_launch"]
        hora_volta = request.form["back_launch"]
        hora_final = request.form["final_time"]
        motivo = request.form["motivo"]
        date = request.form["date"]
        aonde = request.form["aonde"]
        if not date:
            flash("Campo data deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not motivo:
            flash("Campo motivo deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not aonde:
            flash("Campo em qual site deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_inicio:
            flash("Campo Inicio Hora deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_final:
            flash("Campo Horario final deve ser preenchido!", 'error')
            return render_template("registrar-hora.html")
        if not hora_pausa and not hora_volta:
            hora_pausa = '00:00'
            hora_volta = '00:00'
            time1 = datetime.datetime.strptime(hora_inicio, '%H:%M')
            time4 = datetime.datetime.strptime(hora_final, '%H:%M')
            if time1 > time4:
                flash("Horário final não pode ser maior que horário de início!", 'error')
                return render_template("registrar-hora.html")
            somatotal = time4 - time1
            search.date = request.form["date"]
            search.aonde = aonde
            search.motivo = request.form["motivo"]
            search.inicial_time = request.form["initial_time"]
            search.pause_launch = request.form["pause_launch"]
            search.back_launch = request.form["back_launch"]
            search.final_time = request.form["final_time"]
            search.total_time = somatotal
            search.updated_at = dt.now()
            db.session.commit()
            flash("Dados atualizados!", 'success')
            page = request.args.get('page', 1, type=int)
            registros = registro_horas.query.filter_by(login=session['login']).order_by(registro_horas.date.desc()).paginate(per_page=10)
            return render_template("index.html", registros=registros)
        else:
            time1 = datetime.datetime.strptime(hora_inicio, '%H:%M')
            time2 = datetime.datetime.strptime(hora_pausa, '%H:%M')
            time3 = datetime.datetime.strptime(hora_volta, '%H:%M')
            time4 = datetime.datetime.strptime(hora_final, '%H:%M')
            if time1 > time2:
                flash("Horário de saída almoço não pode ser menor que horário de início!", 'error')
                return render_template("registrar-hora.html")
            if time3 < time2:
                flash("Horário da volta almoço não pode ser maior que horário de saída almoço!", 'error')
                return render_template("registrar-hora.html")
            if time3 > time4:
                flash("Horário da volta almoço não pode ser menor que horário final!", 'error')
                return render_template("registrar-hora.html")
            else:
                soma1 = time2 - time1
                soma2 = time4 - time3
                somatotal = soma1 + soma2
                somatotal = time4 - time1
                search.date = request.form["date"]
                search.aonde = aonde
                search.motivo = equest.form["motivo"]
                search.inicial_time = request.form["initial_time"]
                search.pause_launch = request.form["pause_launch"]
                search.back_launch = request.form["back_launch"]
                search.final_time = request.form["final_time"]
                search.total_time = somatotal
                search.updated_at = dt.now()
                db.session.commit()
                flash("Dados atualizados!", 'success')
                page = request.args.get('page', 1, type=int)
                registros = registro_horas.query.filter_by(login=session['login']).order_by(registro_horas.date.desc()).paginate(per_page=10)
                return render_template("index.html", registros=registros)
    else:
        registros = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("editar-hora.html", registros=registros)

@app.route('/changepass', methods=["POST", "GET"])
@login_required
def changepass():
    find_pass = users.query.filter_by(login=session['login']).first()
    if request.method == "POST":
        passwd = request.form["actualpass"]
        newpass = request.form["newpass"]
        newpassconfirm = request.form["newpassconfirm"]
        if crypt.check_password_hash(find_pass.password, passwd) == False:
            flash("Senha atual não confere com a senha da base de dados!", "error")
            return redirect(url_for('changepass'))
        if newpass != newpassconfirm:
            flash("Nova senha não confere com a confirmação de nova senha!", "error")
            return redirect(url_for('changepass'))
        else:
            hashpass = crypt.generate_password_hash(newpass)
            find_pass.password = hashpass
            db.session.commit()
            flash("Senha alterada com sucesso!", "success")
            return render_template("change-pass.html")
    else:
        return render_template("change-pass.html")

@app.route('/changesite', methods=["POST", "GET"])
@login_required
def changesite():
    if session["user_type"] != 3:
        flash("Apenas usuários de nível elevado podem acessar essa página!", "error")
        return redirect(url_for('home'))
    if request.method == "POST":
        aonde = request.form['aonde']
        login = request.form['login']
        if not aonde and not login:
            flash("Favor selecionar os campo corretamente!", "error")
            return redirect(url_for('changesite'))
        if not login:
            flash("Favor selecionar os campo corretamente!", "error")
            return redirect(url_for('changesite'))
        else:
            print('caiuaqui')
            search = users.query.filter_by(login=login).first()
            search.site = aonde    
            db.session.commit()
            flash("Site atualizado com sucesso!", "success")
            return redirect(url_for('changesite'))
    else:
        logins = users.query.all()
        unidades = sites.query.filter_by(ativo=1).order_by(sites.unidade.asc())
        return render_template("change-site.html", unidades=unidades, logins=logins)

@app.route('/done', methods=["POST", "GET"])
@login_required
def done(): 
    if request.method == "POST":
        mindate = request.form['initialdone']
        maxdate = request.form['finaldone']
        if mindate > maxdate:
            flash("Data de Inicio não pode ser maior que a Final!", "error")
            return render_template("done.html")
        else:
            registro_horas.query.filter(registro_horas.date.between(mindate, maxdate)).update({"done": True}, synchronize_session=False)
            db.session.commit()
            flash("Período informado foi concluído com sucesso!", "success")
            return redirect(url_for('done'))
    else:
        return render_template("done.html")

@app.route('/undone', methods=["POST", "GET"])
@login_required
def undone(): 
    if request.method == "POST":
        mindate = request.form['initialdone']
        maxdate = request.form['finaldone']
        if mindate > maxdate:
            flash("Data de Inicio não pode ser maior que a Final!", "error")
            return render_template("undone.html")
        else:
            registro_horas.query.filter(registro_horas.date.between(mindate, maxdate)).update({"done": False}, synchronize_session=False)
            db.session.commit()
            flash("Período informado foi revertido com sucesso!", "success")
            return redirect(url_for('undone'))
    else:
        return render_template("undone.html")
