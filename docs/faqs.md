# FAQs

### Project Purpose and Scope

**Q: What is the main goal of this project?**  
A: The goal is to automate the generation of email templates using NLP to reduce the manual effort spent composing routine business emails.

**Q: Is this a finished product?**  
A: No, this is a proof of concept (POC) phase. The final product will follow after evaluation and possible adjustments.

**Q: What kind of emails will the system generate?**  
A: The system is designed to generate personalised templates for routine emails such as meeting invites, follow-ups, and status updates.

### Technical Questions

**Q: What technology stack is used?**  
A: The stack includes Python, Hugging Face Transformers, NLTK, PyTorch, and Outlook integration via Pywin32.

**Q: Which NLP models are considered?**  
A: Models like BERT, T5, and GPT-based architectures such as GPT-2 and GPT-4 are being explored.

**Q: What training data is being used?**  
A: A sample dataset of historical emails, partially preprocessed, and additional sources are being evaluated to enhance performance.

**Q: How is the model evaluated?**  
A: BLEU scores are used to assess the quality of the generated emails against reference texts.

**Q: Will the AI write complete emails or just templates?**  
A: The AI generates structured, context-aware email templates that can be edited or sent directly after review.

### Integration

**Q: Will this integrate with Microsoft Outlook?**  
A: Yes, integration with Outlook is a key feature using Pywin32 to automate email sending from templates.

**Q: Is the integration already working?**  
A: Basic Outlook integration is in progress. Final deployment is planned post-POC.

### Data & Privacy

**Q: Is the email data anonymised?**  
A: Yes, all data used for training is anonymised and handled according to data privacy best practices.

**Q: Do we need more data?**  
A: Yes. Additional high-quality email data will improve the model's accuracy and generalisability.

### Team & Timeline

**Q: Who is working on this project?**  
A: A Machine Learning Engineer and a Data Science Trainee are jointly leading the project.

**Q: Why was there a delay in the timeline?**  
A: A four-week delay occurred due to resource constraints and the need for more robust data preprocessing.

**Q: What is the revised project timeline?**  
A: Phase 1 ends in November 2024, with later phases to be confirmed based on progress and testing.

### ROI and Business Value

**Q: What’s the expected return on investment?**  
A: Significant time savings on routine communication and increased consistency in email tone and content.

**Q: Will this save employees time?**  
A: Yes. Automating repetitive emails can help teams focus on high-value work and reduce admin overhead.

### Limitations & Next Steps

**Q: What are the main challenges so far?**  
A: Limited training data and resource allocation have posed challenges in progress and model performance.

**Q: What are the next steps after the POC?**  
A: Evaluate results, secure additional data, refine the model, and begin scaling and full integration.

### Existing FAQs

**Q: Can I connect this directly to Outlook?**  
A: We're working on an integration using Microsoft Graph API. For now, you can copy-paste or simulate sending.

**Q: Does the AI remember me?**  
A: Not yet. But future versions may allow customisation by user or team.
