# Appointment Booking System - Complete Implementation

## Overview
A comprehensive appointment booking system with real-time notifications, provider selection, and accept/reject functionality.

## Features Implemented

### ✅ 1. Patient Appointment Booking
- **Provider Selection**: Patients can optionally select a preferred provider when booking
- **Appointment Types**: Therapy, Consultation, Follow-up, Crisis Intervention
- **Date & Time Selection**: User-friendly date/time picker
- **Notes**: Optional field for patient concerns
- **Real-time Notifications**: Providers receive instant notifications when appointments are booked

### ✅ 2. Provider Notifications Dashboard
- **Pending Appointments**: View all pending appointment requests
- **Filter System**: 
  - Pending (default)
  - Accepted
  - Rejected
  - All
- **Real-time Updates**: Automatic page refresh when new appointments arrive
- **Browser Notifications**: Desktop notifications for new appointment requests

### ✅ 3. Accept/Reject Actions
- **Accept**: Provider accepts appointment and gets assigned
- **Reject with Reason**: Modal dialog to provide optional rejection reason
- **Patient Notifications**: Patients receive real-time notifications of acceptance/rejection
- **Status Tracking**: All appointments tracked with status (booked, pending, accepted, rejected)

### ✅ 4. Real-time Communication (SocketIO)
- **User Rooms**: Each user joins their personal notification room on connection
- **Event Types**:
  - `new_appointment`: Sent to providers when patient books
  - `appointment_accepted`: Sent to patient when provider accepts
  - `appointment_rejected`: Sent to patient when provider rejects
- **Browser Notifications**: Native browser notification support
- **In-page Notifications**: Toast-style notifications with auto-dismiss

## Files Modified

### Backend (`app.py`)
1. **`provider_dashboard()`** - Added filter support and appointment fetching
2. **`schedule()`** - Added provider selection and real-time notification emission
3. **`accept_appointment()`** - Accept endpoint with SocketIO notification
4. **`reject_appointment()`** - Reject endpoint with reason and SocketIO notification
5. **SocketIO Handlers**:
   - `@socketio.on('connect')` - User room joining
   - `@socketio.on('disconnect')` - User room leaving

### Database Model (`models.py`)
- **Appointment Model** - Added fields:
  - `rejection_reason` (Text, nullable)
  - `updated_at` (DateTime, auto-update)

### Frontend Templates

#### `templates/schedule.html`
- Added provider selection dropdown
- Populated from backend providers list

#### `templates/provider_dashboard.html`
- Filter buttons (Pending, Accepted, Rejected, All)
- Dynamic table columns based on filter
- Rejection modal with reason textarea
- SocketIO client integration
- JavaScript functions:
  - `openRejectModal(appointmentId)`
  - `closeRejectModal()`
  - `showNotification(message, type)`

#### `templates/patient_dashboard.html`
- SocketIO client integration
- Real-time notification handlers
- Browser notification support

## Database Migration

### Option 1: Run Migration Script (Recommended for SQLite)
```bash
python add_appointment_fields_migration.py
```

### Option 2: Flask-Migrate (For PostgreSQL/MySQL)
```bash
flask db migrate -m "Add rejection_reason and updated_at to appointments"
flask db upgrade
```

### Option 3: Manual (If needed)
```sql
ALTER TABLE appointments ADD COLUMN rejection_reason TEXT;
ALTER TABLE appointments ADD COLUMN updated_at DATETIME;
UPDATE appointments SET updated_at = created_at WHERE updated_at IS NULL;
```

## Usage Guide

### For Patients

1. **Book an Appointment**:
   - Navigate to "Schedule Appointment"
   - Select date, time, and appointment type
   - Optionally select a preferred provider
   - Add any notes/concerns
   - Click "Book Appointment"

2. **Receive Notifications**:
   - Browser notification when provider accepts/rejects
   - In-page toast notification with details
   - View updated status on dashboard

### For Providers

1. **View Pending Appointments**:
   - Login to provider dashboard
   - See "Appointment Notifications" section
   - Default filter shows pending appointments

2. **Accept Appointment**:
   - Click green checkmark icon
   - Appointment status changes to "accepted"
   - Patient receives notification

3. **Reject Appointment**:
   - Click red X icon
   - Modal opens for optional rejection reason
   - Enter reason (optional) and confirm
   - Patient receives notification with reason

4. **Filter Appointments**:
   - Click filter buttons: Pending, Accepted, Rejected, All
   - Table updates to show filtered appointments
   - URL parameter persists filter selection

## API Endpoints

### Patient Endpoints
- `GET /schedule` - Show appointment booking form
- `POST /schedule` - Create new appointment

### Provider Endpoints
- `GET /provider-dashboard?filter=<status>` - View appointments with filter
- `POST /appointments/<id>/accept` - Accept appointment
- `POST /appointments/<id>/reject` - Reject appointment (with optional reason)

### SocketIO Events

#### Server → Client
- `connected` - Confirmation of connection
- `new_appointment` - New appointment booked (to provider)
- `appointment_accepted` - Appointment accepted (to patient)
- `appointment_rejected` - Appointment rejected (to patient)

#### Client → Server
- `connect` - User connects and joins personal room
- `disconnect` - User disconnects

## Testing the System

### Test Flow 1: Patient Books → Provider Accepts
1. Login as patient
2. Book appointment (optionally select provider)
3. Login as provider (same institution)
4. See appointment in "Pending" filter
5. Click accept
6. Switch back to patient → see "Accepted" status

### Test Flow 2: Patient Books → Provider Rejects
1. Login as patient
2. Book appointment
3. Login as provider
4. Click reject icon
5. Enter reason in modal
6. Submit
7. Switch back to patient → see rejection notification

### Test Flow 3: Real-time Notifications
1. Open two browser windows
2. Login as patient in window 1
3. Login as provider in window 2
4. Book appointment in window 1
5. See instant notification in window 2
6. Accept/reject in window 2
7. See instant notification in window 1

## Browser Notification Setup

Users will be prompted to allow notifications on first visit. To manually enable:

**Chrome/Edge**:
1. Click lock icon in address bar
2. Site settings → Notifications → Allow

**Firefox**:
1. Click lock icon
2. Permissions → Notifications → Allow

## Troubleshooting

### Issue: No real-time notifications
**Solution**: 
- Ensure SocketIO is running (`socketio.run(app, ...)` in main)
- Check browser console for connection errors
- Verify firewall allows WebSocket connections

### Issue: Migration fails
**Solution**:
- Backup database
- Try manual SQL commands
- Or recreate database with `flask db upgrade`

### Issue: Provider doesn't see appointments
**Solution**:
- Verify patient and provider have same institution
- Check appointment status is 'booked' or 'pending'
- Ensure provider_id is NULL or matches current provider

### Issue: Lint errors in templates
**Note**: Errors like "Property assignment expected" in `provider_dashboard.html` line 132 are false positives. The JavaScript linter doesn't understand Jinja2 template syntax `{{ appt.id }}`. These will work correctly when rendered.

## Security Features

- ✅ CSRF protection on all forms
- ✅ Login required for all endpoints
- ✅ Role-based access control (patient/provider)
- ✅ Provider can only accept/reject their own appointments
- ✅ Institution-based filtering
- ✅ Input sanitization and validation

## Performance Optimizations

- Eager loading with `joinedload` to prevent N+1 queries
- Indexed database columns (user_id, provider_id, status, date)
- Efficient query filtering
- Cached institutional data

## Future Enhancements (Optional)

1. **Email Notifications**: Send email when appointment status changes
2. **SMS Notifications**: Integrate Twilio for SMS alerts
3. **Calendar Integration**: Export to Google Calendar/iCal
4. **Appointment Reminders**: Automated reminders 24h before
5. **Rescheduling**: Allow patients to reschedule appointments
6. **Video Call Integration**: Direct link to telehealth session
7. **Provider Availability**: Calendar view of provider schedules
8. **Appointment History**: Detailed history with notes

## Support

For issues or questions:
1. Check this README
2. Review code comments in `app.py`
3. Check browser console for JavaScript errors
4. Review Flask logs for backend errors

---

**Implementation Status**: ✅ Complete and Ready for Production

All features have been implemented and tested. The system is ready to use after running the database migration.
