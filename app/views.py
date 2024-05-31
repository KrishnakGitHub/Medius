import pandas as pd
from io import BytesIO, StringIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from .forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                try:
                    # Read Excel file
                    df = pd.read_excel(file)
                    
                    # Convert to CSV format
                    csv_buffer = StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    file = csv_buffer
                    
                except Exception as e:
                    return render(request, 'upload.html', {'form': form, 'error': str(e)})
            elif file.name.endswith('.csv'):
                pass  # Already in CSV format, no need to convert
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Invalid file format. Please upload an Excel file or a CSV file.'})
            
            summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')

            # Save the summary to a CSV file in memory
            output = BytesIO()
            summary.to_csv(output, index=False)

            output.seek(0)
            
            # Send email
            email = EmailMessage(
                'Python Assignment - Krishna',
                'Please find the summary report attached.',
                settings.DEFAULT_FROM_EMAIL,
                settings.DEFAULT_TO_EMAIL,
            )
            email.attach('summary_report.csv', output.getvalue(), 'text/csv')
            email.send()
            return render(request, 'success.html')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
