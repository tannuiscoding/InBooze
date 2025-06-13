from flask import Blueprint, render_template, request, redirect
from app.email_ingest import parse_and_ingest_mbox
from app.mindsdb_client import query_kb
from app.summarizer import generate_summary

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mbox_file = request.files['email_file']
        mbox_path = f"data/uploaded_emails/{mbox_file.filename}"
        mbox_file.save(mbox_path)
        parse_and_ingest_mbox(mbox_path)
        return redirect('/search')
    return render_template('index.html')
