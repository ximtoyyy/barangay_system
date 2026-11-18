"""EMAIL MESSAGES: all the emails the system sends. Edit the wording here."""
import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

log = logging.getLogger(__name__)


def _peso(amount):
    return "Free" if amount == 0 else f"PHP {amount:,.2f}"


def _fee_line(req):
    """Fee + how the resident chose to pay (used in the confirmation email)."""
    if req.fee_charged == 0:
        return "Fee: Free"
    line = f"Fee: {_peso(req.fee_charged)}\n"
    if req.payment_method == "qrph":
        return line + "Payment: online via QR Ph. Open your request in the system to see the QR code and send your proof of payment."
    return line + "Payment: cash. Pay at the Barangay Hall when you claim it."


def _send(subject, body, to):
    """Send one email. A failed email never breaks the page: we log a short warning and carry on."""
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to])
        return True
    except Exception as e:
        log.warning("Email to %s could not be sent: %s", to, e)
        return False


def office_recipients():
    """Barangay inbox + every approved staff member / admin who has an email."""
    staff = User.objects.filter(is_staff=True, is_active=True).exclude(email="").values_list("email", flat=True)
    seen, result = set(), []
    for e in [settings.BARANGAY_EMAIL, *staff]:
        if e.lower() not in seen:
            seen.add(e.lower())
            result.append(e)
    return result


def notify_new_request(req):
    """Email the barangay inbox and ALL staff, and send the resident a confirmation."""
    r = req.resident
    for to in office_recipients():
        _send(
            f"New document request: {req.reference_no}",
            f"A new request was submitted.\n\nReference: {req.reference_no}\n"
            f"Resident: {r.full_name}\nEmail: {r.user.email}\nContact: {r.contact_no}\n"
            f"Document: {req.document_type}\nPurpose: {req.purpose}\n\n"
            "Please log in and open Dashboard to handle it.",
            to,
        )
    return _send(
        f"Request received: {req.reference_no}",
        f"Hello {r.full_name},\n\nWe received your request for {req.document_type}.\n"
        f"Your reference number is {req.reference_no}.\n"
        f"{_fee_line(req)}\n"
        "We will email you once it is ready.\n\n- Barangay Office",
        r.user.email,
    )


def notify_status_change(req):
    """Email the resident when the request is approved, rejected, or ready to claim.
    The email is signed with the name of the staff member who handled it."""
    r = req.resident
    if req.status == "ready":
        subject = f"Your document is ready for pickup ({req.reference_no})"
        body = (f"Hello {r.full_name},\n\nYour {req.document_type} is ready. "
                f"Please claim it at the Barangay Hall during office hours.\n"
                f"Bring a valid ID and your reference number: {req.reference_no}.\n")
        if req.fee_charged > 0 and req.payment_status == "verifying":
            body += "We are still checking your online payment.\n"
        elif req.fee_charged > 0 and req.payment_status != "paid":
            body += f"Fee to pay when you claim it: {_peso(req.fee_charged)}.\n"
    elif req.status == "approved":
        subject = f"Request approved ({req.reference_no})"
        body = f"Hello {r.full_name},\n\nYour request for {req.document_type} was approved and is being prepared.\n"
    elif req.status == "rejected":
        subject = f"Request update ({req.reference_no})"
        body = f"Hello {r.full_name},\n\nYour request for {req.document_type} could not be approved.\n"
    else:
        return False
    if req.remarks:
        body += f"\nRemarks from the barangay: {req.remarks}\n"
    sign = f"{req.handler_name}\nBarangay Office" if req.handler_name else "Barangay Office"
    body += f"\n- {sign}"
    return _send(subject, body, r.user.email)


def notify_new_registration(profile, kind="resident"):
    """Tell the barangay a new account is waiting for approval."""
    extra = f"Position: {profile.position or '-'}" if kind == "staff" else f"Address: {profile.address}"
    _send(
        f"New {kind} account waiting for approval: {profile.full_name}",
        f"{profile.full_name} ({profile.user.email}) registered as {kind}.\n{extra}\n"
        f"Contact: {profile.contact_no}\n\n"
        "Log in as admin and open 'Account Approvals' to approve or reject.",
        settings.BARANGAY_EMAIL,
    )


def notify_account_decision(profile, kind="resident"):
    use = "log in to the staff dashboard" if kind == "staff" else "log in and request documents"
    if profile.approval == "approved":
        subject, body = "Your account was approved", (
            f"Hello {profile.full_name},\n\nYour account is approved. You can now {use} "
            "with your email.\n\n- Barangay Office")
    elif profile.approval == "rejected":
        subject, body = "Your registration was not approved", (
            f"Hello {profile.full_name},\n\nWe could not approve your registration. "
            "Please visit or contact the barangay office.\n\n- Barangay Office")
    else:
        return False
    return _send(subject, body, profile.user.email)


def notify_payment_proof(req):
    """Tell the barangay inbox and all staff that a resident sent a QR Ph payment proof."""
    for to in office_recipients():
        _send(
            f"Payment proof received: {req.reference_no}",
            f"{req.resident.full_name} sent proof of payment for {req.document_type}.\n"
            f"Amount: {_peso(req.fee_charged)}\nReference no. from the payment app: {req.payment_reference}\n\n"
            "Please open the request, check the screenshot, and mark it Paid.",
            to,
        )
