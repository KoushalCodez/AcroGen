# Little Shop Report API

This is the reporting API for the Little Shop project. It exposes an endpoint to generate a full shop report with PDF generation using Playwright.

## PDF Generation

At what point would you move this work out of the request?
I would move this PDF generation to a background job when the report takes longer than a few seconds to generate, or when multiple users are triggering it concurrently, as long-running requests hold up API server connections and leave the user hanging without feedback.
