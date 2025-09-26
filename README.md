# Briefly - Project Brief Management App

A streamlit-based web application for managing project briefs with AI-powered tagline generation.

## Overview

Briefly is a simple yet powerful tool that helps teams and individuals organize project briefs, deadlines, and supporting documents. The app features an integrated AI tagline generator that creates catchy marketing taglines for your projects using the Llama-3.1-70B model via HuggingFace.

## App Link: https://briefly-app.streamlit.app/ 

## Features

- **Project Brief Submission**: Submit project briefs with names, deadlines, links, and file uploads
- **AI Tagline Generation**: Automatically generates catchy taglines for projects using AI
- **File Management**: Upload and download supporting documents (PDFs, DOCX, images, etc.)
- **Brief Organization**: View all submitted briefs in an organized, expandable format
- **Data Persistence**: All briefs are saved locally in JSON format
- **Clean Interface**: Purple and orange themed UI with hover effects

## Prerequisites

- Python 3.7+
- Streamlit
- HuggingFace Hub account and API token

## Installation

1. **Clone the repository** (or download the `brief_app.py` file)

2. **Install required packages**:
   ```bash
   pip install streamlit huggingface-hub
   ```

3. **Set up HuggingFace API**:
   - Create an account at [HuggingFace](https://huggingface.co/)
   - Generate an API token from your HuggingFace settings
   - Set the environment variable:
     ```bash
     export HF_TOKEN="your_huggingface_token_here"
     ```
   
   Or on Windows:
   ```cmd
   set HF_TOKEN=your_huggingface_token_here
   ```

## Usage

1. **Start the application**:
   ```bash
   streamlit run brief_app.py
   ```

2. **Access the app**: 
    Open your browser to the given URL

### Using the App

#### Submit Brief Tab
1. Enter a unique **Project Name** (this helps generate better taglines)
2. Set the **Deadline** using the date picker
3. Add any relevant **Links** in the text area
4. **Upload supporting files** (optional) - supports PDFs, DOCX, images, and more
5. Click **Submit Brief**
6. The AI will automatically generate a tagline for your project

#### Submitted Briefs Tab
- View all submitted briefs in expandable cards
- Download uploaded files for each brief
- See AI-generated taglines
- Clear all briefs using the "Clear Submitted Briefs" button

## File Structure

```
project-folder/
|__requirements.txt
|__README.md
├── brief_app.py          # Main application file
├── briefs.json          # Generated: stores all brief data
└── uploads/             # Generated: stores uploaded files
    ├── file1.pdf
    ├── file2.docx
    └── ...
```

## Data Storage

- **Briefs**: Stored in `briefs.json` in the same directory as the app
- **Uploaded Files**: Stored in the `uploads/` folder
- **File Format**: JSON structure with project details and file references

## AI Integration

The app uses:
- **Model**: `meta-llama/Llama-3.1-70B-Instruct`
- **Provider**: Fireworks AI (via HuggingFace)
- **Purpose**: Generates marketing taglines under 140 characters
- **Fallback**: Shows error message if AI generation fails

## Customization

### Styling
The app uses custom CSS for purple/orange theming. Modify the `st.markdown()` sections in the code to change colors or styling.

### AI Model
To use a different model, change the model parameter in the `generate_tagline()` function:
```python
model="meta-llama/Llama-3.1-70B-Instruct" 
```

### File Types
To restrict file uploads, modify the `type` parameter in `st.file_uploader()`:
```python
type=["pdf", "docx", "png", "jpg", "etc"] 
```

## Challenges faced:
1. Picking the right AI API to generate the taglines, bigger APIs like the meta llama API could not generate the tag lines properly
2. Displaying the correct uploaded files for each uploaded brief. 
3. Find a free AI API to use, since its a small project, a free AI API is the best option.


## What to improve when given more time:
1. Limiting the file types to only appropriate ones
2. Impleting code that avoids duplicate uploads, checks if a newly selected file does not have same file name as already uploaded files for the   same brief submission.
3. Give the option to choose which uploaded brief one wants to delete instead of deleting everything.

## Troubleshooting

### Common Issues

1. **HuggingFace API Error**:
   - Verify your `HF_TOKEN` environment variable is set correctly
   - Check your HuggingFace account has API access
   - Ensure you have sufficient API quota

2. **File Upload Issues**:
   - Check that the `uploads/` directory has write permissions
   - Verify file size limits (Streamlit default is 200MB)

3. **Briefs Not Saving**:
   - Ensure the app directory has write permissions for `briefs.json`
   - Check for any file system restrictions

### Error Messages

- **"Project Name is required"**: Enter a project name before submitting
- **"(AI error: ...)"**: Check your HuggingFace API setup
- **"(missing)"**: Uploaded file was deleted from the uploads folder

## Security Considerations

- This app stores files locally and is intended for development/internal use
- For production deployment, consider:
  - Implementing user authentication
  - Using cloud storage for files
  - Adding input validation and sanitization
  - Setting up proper error handling and logging


## Support

For issues related to:
- **Streamlit**: Check the [Streamlit documentation](https://docs.streamlit.io/)
- **HuggingFace**: Check the [HuggingFace documentation](https://huggingface.co/docs)
- **This app**: Review the code comments and troubleshooting section above