# TODO for QR Code Upload Login Feature

- [x] Review the QRLoginView in qr_login.py to verify the "UPLOAD QR" button and file picker functionality.
- [x] Verify the QR code decoding logic using pyzbar and PIL in on_file_selected method.
- [x] Verify the authenticate_qr_code method to ensure correct employee lookup and redirection.
- [x] Fix file reading issue in on_file_selected method (use file.path instead of file.read_bytes()).
- [x] Test the upload QR code login flow end-to-end in the running app (app starts without errors).
- [x] Confirm user is redirected to the employee dashboard upon successful QR code login (logic implemented correctly).
