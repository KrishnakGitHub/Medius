import pandas as pd
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from .forms import FileUploadForm

def generate_summary_report(df):
    """
    Generate summary report from DataFrame.
    Groups data by 'State' and 'DPD', calculates count,
    and returns a DataFrame with the summary.
    """
    try:
        summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
        return summary
    except Exception as e:
        raise ValueError("Error generating summary report: {}".format(str(e)))

def send_email_with_attachment(subject, body, attachment_content, attachment_filename):
    """
    Send email with attachment.
    """
    try:
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            settings.DEFAULT_TO_EMAIL,
        )
        email.attach(attachment_filename, attachment_content, 'text/csv')
        email.send()
    except Exception as e:
        raise ValueError("Error sending email: {}".format(str(e)))

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                try:
                    # Read Excel file with openpyxl engine
                    df = pd.read_excel(file, engine='openpyxl')
                    # Generate summary report
                    summary = generate_summary_report(df)
                except Exception as e:
                    return render(request, 'upload.html', {'form': form, 'error': str(e)})
            elif file.name.endswith('.csv'):
                try:
                    # Read CSV file
                    df = pd.read_csv(file)
                    # Generate summary report
                    summary = generate_summary_report(df)
                except Exception as e:
                    return render(request, 'upload.html', {'form': form, 'error': str(e)})
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Invalid file format. Please upload an Excel file or a CSV file.'})
            
            # Send summary report via email
            output = BytesIO()
            summary.to_csv(output, index=False)
            output.seek(0)
            try:
                send_email_with_attachment(
                    subject=' Python Assignment - Krishna',
                    body='Please find the summary report attached.',
                    attachment_content=output.getvalue(),
                    attachment_filename='summary_report.csv'
                )
                return render(request, 'success.html')
            except Exception as e:
                return render(request, 'upload.html', {'form': form, 'error': str(e)})
                
    else:
        form = FileUploadForm()
        
    return render(request, 'upload.html', {'form': form})
