# Little Shop Report API

This is the reporting API for the Little Shop project. It exposes an endpoint to generate a full shop report with PDF generation using Playwright.

## PDF Generation

At what point would you move this work out of the request?
I would move this PDF generation to a background job when the report takes longer than a few seconds to generate, or when multiple users are triggering it concurrently, as long-running requests hold up API server connections and leave the user hanging without feedback.

## Idempotency (Ask Twice, Get One)

Our report generation endpoint checks if a report was already created today and returns the existing one instead of duplicating the work. This check protects against a single user accidentally triggering expensive, time-consuming, or side-effect-heavy tasks multiple times (like double-clicking a submit button). A real-world example where a missing check like this costs money is processing a payment twice, or sending an angry customer the exact same email twice!
