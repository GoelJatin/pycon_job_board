# PyCon Job Board

Create a public job board for all attendees to view and share job openings from their organisations.

The Job Board is a Django application with Postgres backend.

It verifies the Email by using an OTP and allows the user to share a job post only after validation.

Submit Job form:

1. Email of the submitter (email validation done via otp)
1. Name of the submitter
1. Redact email? - an option to the submitter whether they wish to show / hide their email
1. OTP
1. Company name
1. Website - Company website URL
1. Title - title / position of the job opening
1. Job URL
1. Description

Either one of job url or description should be provided.
