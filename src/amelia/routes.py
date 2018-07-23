# -*- coding: utf-8 -*-

"""
    Amelia: konfiguracja rutingu aplikacji.
"""

from flask import (
    flash,
    render_template,
    redirect,
)

from amelia import amelia
from amelia.models.forms import (
    Event,
    WebRegistrationForm,
    RegistrationForm,
)
from amelia.config import Config


@amelia.route('/', methods=['GET', 'POST'])
def form_show():
    """
        Strona główna - obsługa formularza rejestracji
    """
    form = WebRegistrationForm()
    form.event_id.choices = Event.items()
    if form.validate_on_submit():
        admin_form = RegistrationForm()
        try:
            admin_form.set_data(form.data)
        except Exception:
            # TODO dodać logowanie
            flash('Przepraszamy, wystąpił błąd wewnętrzny.')
            flash('Spróbuj ponownie za chwilę')
        else:
            flash('Dziękujemy za rejestrację!')
        return redirect('/')
    return render_template('content.html', title=Config.TITLE, form=form)
