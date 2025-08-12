from flask import Blueprint, render_template, request, redirect, url_for
from app.email_ingest import parse_and_ingest_mbox
from app.mindsdb_client import query_kb
from app.summarizer import generate_summary
from app.utils import combine_threads

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mbox_file = request.files['email_file']
        mbox_path = f"data/uploaded_emails/{mbox_file.filename}"
        mbox_file.save(mbox_path)
        parse_and_ingest_mbox(mbox_path)
        return redirect(url_for('routes.search'))
    return render_template('index.html')


@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        sender = request.form.get('sender', '').strip() or None
        results = query_kb(query=query, sender_filter=sender)
        return render_template('results.html', results=results, query=query, sender=(sender or ''))
    # GET renders the search form
    return render_template('search.html')


@bp.route('/summarize', methods=['POST'])
def summarize():
    query = request.form.get('query', '').strip()
    sender = request.form.get('sender', '').strip() or None
    results = query_kb(query=query, sender_filter=sender)
    combined = combine_threads(results) if results else ''
    summary = generate_summary(combined) if combined else 'No content to summarize.'
    return render_template('summary.html', summary=summary)
