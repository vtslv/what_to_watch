from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route('/')
def index_view():
    opinion = random_opinion()
    if opinion is not None:
        return render_template('opinion.html', opinion=opinion)
    abort(404)

# @app.route('/')
# def index_view():
#     # Определяется количество мнений в базе данных
#     quantity = Opinion.query.count()
#     # Если мнений нет,
#     if not quantity:
#         abort(404)
#         # то возвращается сообщение
#         # return 'В базе данных мнений о фильмах нет.'
#     # Иначе выбирается случайное число в диапазоне от 0 и до quantity
#     offset_value = randrange(quantity)
#     # И определяется случайный объект
#     opinion = Opinion.query.offset(offset_value).first()
#     # Вот здесь в шаблон передаётся весь объект opinion
#     return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    # Если ошибок не возникло, то
    if form.validate_on_submit():
        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь,
        if Opinion.query.filter_by(text=text).first() is not None:
            # вызвать функцию flash и передать соответствующее сообщение
            flash('Такое мнение уже было оставлено ранее!')
            # и вернуть пользователя на страницу «Добавить новое мнение»
            return render_template('add_opinion.html', form=form)
        # нужно создать новый экземпляр класса Opinion
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        # Затем добавить его в сессию работы с базой данных
        db.session.add(opinion)
        # И зафиксировать изменения
        db.session.commit()
        # Затем перейти на страницу добавленного мнения
        return redirect(url_for('opinion_view', id=opinion.id))
    # Иначе просто отрисовать страницу с формой
    return render_template('add_opinion.html', form=form)


# Тут указывается конвертер пути для id
@app.route('/opinions/<int:id>')
# Параметром указывается имя переменной
def opinion_view(id):
    # Теперь можно запрашивать мнение по id
    # и если нет мнения get_or_404()
    opinion = Opinion.query.get_or_404(id)
    # И передавать его в шаблон
    return render_template('opinion.html', opinion=opinion)
