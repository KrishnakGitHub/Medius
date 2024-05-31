import pandas as pd
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from .forms import FileUploadForm


# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')

            # Save the summary to an Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                summary.to_excel(writer, index=False, sheet_name='Summary')
                # writer.save()
            output.seek(0)
            
            # Send email
            email = EmailMessage(
                'Python Assignment - Krishna',
                'Please find the summary report attached.',
                settings.DEFAULT_FROM_EMAIL,
                settings.DEFAULT_TO_EMAIL,
            )
            email.attach('summary_report.xlsx', output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            return render(request, 'success.html')
    else:
        form = FileUploadForm()
        return render(request, 'upload.html', {'form': form})
