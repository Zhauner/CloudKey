
from django.conf import settings
from django.contrib.auth.hashers import check_password

settings.configure()
print(check_password('000000000', 'pbkdf2_sha256$600000$Uxm52MmLGPDIsqAtCG7jnK$qr9U/50+q/FrOFS8byKWKRaYvvqMSJ+dvdzBC+d67DQ='))
