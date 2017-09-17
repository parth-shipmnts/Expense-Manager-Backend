from ExpenseManager.models import db, User, Role, CategoriesToUsers, Category, Expense
from datetime import datetime

def create_user(register_form):
    '''
    Creates user based on register_form data and assigns
    default categories to them

    Args:
        register_form: register form which is wtforms submited by user.

    Returns:
        register form after successful creation of user.
    '''
    try:
        user_name = register_form.data['user_name']
        email = register_form.data['email']
        password = register_form.data['password']
        user_role_id = Role.query.filter_by(name='user').first().id
        user = User(user_name, email, password, user_role_id)
        categories = Category.query.filter_by(is_default=True).all()
        for cat in categories:
            cateories_to_user = CategoriesToUsers()
            cateories_to_user.category = cat
            user.categories_to_users.append(cateories_to_user)
        db.session.add(user)
        db.session.commit()
        return register_form
    except Exception as e:
        raise e

def get_categories(user):
    '''
    Get all the categories that belongs to the particular user

    Args:
        user: current logged in user

    Returns:
        list of categories that belongs to given user
    '''
    try:
        categories = (Category.query
                      .join(CategoriesToUsers)
                      .join(User)
                      .filter(User.id == user.id)
                      .all())
        for i, cat in enumerate(categories):
             cat.name.title()
        return categories      
    except Exception as e:
        raise e

def get_expense_details(user, category_name = None, start_date = '1900-01-01', end_date = '9999-12-01'):
    '''
    Get expense details for a particular user

    Args:
        user: current logged in user
        category_name: optional category_name to filter expenses by category
        start_date: date from which expenses should return
        end_date: date until which expenses should return

    Returns:
        list of expenses
    '''
    try:
        ctou = [cat.id for cat in user.categories_to_users]
        if category_name is None:
            data = (db.session.query(Expense, Category.name)
                    .join(CategoriesToUsers)
                    .join(User)
                    .join(Category)
                    .filter(CategoriesToUsers.id.in_(ctou))
                    .filter(Expense.date_added.between(start_date, end_date))).all()
        else:
            category_name = category_name.lower()
            data = (db.session.query(Expense, Category.name)
                    .join(CategoriesToUsers)
                    .join(User)
                    .join(Category)
                    .filter(CategoriesToUsers.id.in_(ctou))
                    .filter(Category.name == category_name)
                    .filter(Expense.date_added.between(start_date, end_date))).all()

        expenses = []
        for d in data:
            expenses.append(
                {
                    "category": d[1].title(),
                    "amount": d[0].amount,
                    "date_added":d[0].date_added.strftime('%Y-%m-%d %H:%M:%S'),
                    "description": d[0].description
                }
            )
        return expenses
    except Exception as e:
        raise e

def add_expense_details(user, expense_form):
    '''
    Add expense details for a particular user

    Args:
        user: current logged in user
        expense_form: expense form sent by user

    Returns:
        expense form on successful addition of expense
    '''
    try:
        category_to_user_id = (db.session.query(CategoriesToUsers.id)
                               .join(User)
                               .join(Category)
                               .filter(User.id == user.id)
                               .filter(Category.name == expense_form.data['category'].lower())).first()

        if expense_form.data['description'] is '':
            description = None
        else:
            description = expense_form.data['description']
        expense = Expense(
            category_to_user_id,
            expense_form.data['amount'],
            datetime.utcnow(),
            description
        )
        db.session.add(expense)
        db.session.commit()
        return expense_form.data
    except Exception as e:
        raise e

def add_category_details(user, category_form):
    '''
    Add category for a particular user. First it will
    check if category already exists in database or not.
    if it exists then get tha category and assign it to user
    other wise create brand new category and assign it to user

    Args:
        user: current logged in user
        category_form: category form sent by user

    Returns:
        category form on successful addition of category
    '''
    try:
        if category_form:
            category = Category.query.filter_by(name=category_form.data['name'].lower()).first()
            if category is None:
                category = Category(category_form.data['name'].lower())
                db.session.add(category)
                db.session.commit()

            category_to_user_id = (db.session.query(CategoriesToUsers.id)
                                   .join(User)
                                   .join(Category)
                                   .filter(User.id == user.id)
                                   .filter(Category.name == category_form.data['name'].lower()))\
                                   .first()
            if category_to_user_id is None:
                cat_to_user = CategoriesToUsers()
                cat_to_user.category = category
                user.categories_to_users.append(cat_to_user)
                db.session.add(category)
                db.session.commit()
                return category_form.data
        else:
            return {"message": "Invalid data sent"}
    except Exception as e:
        raise e
