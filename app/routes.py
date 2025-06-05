from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, StockItem
from . import db, login_manager
from flask_login import login_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


main = Blueprint('main', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Trying to log in with: {username} / {password}")  # Debug line

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print("Login successful!")  # Debug line
            return redirect(url_for('main.dashboard'))
        else:
            print("Login failed")  # Debug line
            flash('Invalid credentials')
    return render_template('login.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return '''
        <h2>Dashboard</h2>
        <a href="/stock">stock enter</a> |
        <a href="/upload">Upload Stock Excel</a> |
        <a href="/stock_report">View Stock Report</a> |
        <a href="/logout">Logout</a><br>
    '''


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


import openpyxl
from werkzeug.utils import secure_filename
import os


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)

            # Read Excel
            wb = openpyxl.load_workbook(filepath)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                item = StockItem(
                    item_name=row[0],
                    company_name=row[1],
                    client_name=row[2],
                    project_name=row[3],
                    collected_by=row[4],
                    quantity=int(row[5]) if row[5] else 0
                )
                db.session.add(item)

            db.session.commit()
            flash('Data uploaded successfully!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Please upload a valid .xlsx file')

    return render_template('upload.html')

@main.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    if request.method == 'POST':
        identifier = request.form['item_identifier'].strip()
        action = request.form['action']
        qty = int(request.form['quantity'])

        # Try to match by item name or barcode
        item = StockItem.query.filter(
            (StockItem.item_name == identifier) | (StockItem.barcode == identifier)
        ).order_by(StockItem.timestamp.desc()).first()

        if not item:
            flash("Item not found. Please upload it first or check spelling.")
            return redirect(url_for('main.stock'))

        if action == 'in':
            item.quantity += qty
        elif action == 'out':
            if item.quantity < qty:
                flash("Not enough stock to remove!")
                return redirect(url_for('main.stock'))
            item.quantity -= qty

        # Optional: log the stock movement as a new entry
        movement = StockItem(
            item_name=item.item_name,
            barcode=item.barcode,
            company_name=request.form['company'],
            client_name=request.form['client'],
            project_name=request.form['project'],
            collected_by=request.form['collected_by'],
            quantity=item.quantity  # updated quantity
        )
        db.session.add(movement)
        db.session.commit()
        flash("Stock updated successfully!")

    return render_template('stock.html')
@main.route('/stock_report', methods=['GET', 'POST'])
@login_required
def stock_report():
    query = StockItem.query

    search = request.args.get('search')
    if search:
        query = query.filter(
            (StockItem.item_name.ilike(f"%{search}%")) |
            (StockItem.client_name.ilike(f"%{search}%")) |
            (StockItem.project_name.ilike(f"%{search}%"))
        )

    # Group by item to get the latest quantity per item
    all_items = query.order_by(StockItem.timestamp.desc()).all()
    latest_items = {}

    for item in all_items:
        if item.item_name not in latest_items:
            latest_items[item.item_name] = item

    return render_template('stock_report.html', items=latest_items.values(), search=search)
