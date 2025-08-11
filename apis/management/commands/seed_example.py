from django.core.management.base import BaseCommand
from apis.models import DeliveryRequest, Address, BusinessPartner, DeliveryPartner
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Seed example data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding example data..."))

        # superuser
        su = User.objects.create_superuser(
            username="admin",
            password="pass",
        )
        print(f"Created superuser: {su}")

        business_partner_group, _ = Group.objects.get_or_create(name="BusinessPartner")
        delivery_partner_group, _ = Group.objects.get_or_create(name="DeliveryPartner")

        # create normal users
        bu1 = User.objects.create_user(
            username="business_user",
            password="pass",
        )

        bu2 = User.objects.create_user(
            username="business_user2",
            password="pass",
        )

        bu1.groups.add(business_partner_group)
        bu2.groups.add(business_partner_group)

        print("Created business users", bu1, bu2)

        du1 = User.objects.create_user(
            username="delivery_user",
            password="pass",
        )

        du2 = User.objects.create_user(
            username="delivery_user2",
            password="pass",
        )

        du1.groups.add(delivery_partner_group)
        du2.groups.add(delivery_partner_group)
        print(f"Created delivery users: {du1}, {du2}")

        # Create address
        ad1 = Address.objects.create(
            name="Sajilo Life Pvt. Ltd.",
            latitude=27.694937372764176,
            longitude=85.36613559670968,
        )
        ad2 = Address.objects.create(
            name="Lugamandu", latitude=27.693328868381258, longitude=85.36853454640844
        )

        print("Created addresses", ad1, ad2)

        # Create business partner
        bp1 = BusinessPartner.objects.create(
            user=bu1,
            business_name="Sajilo Life Pvt. Ltd.",
        )
        bp1.addresses.add(ad1)
        bp1.save()

        bp2 = BusinessPartner.objects.create(
            user=bu2,
            business_name="Lugamandu",
        )
        bp2.addresses.add(ad2)
        bp2.save()

        print("Created business partners", bp1, bp2)

        # Delivery partners
        dp1 = DeliveryPartner.objects.create(
            user=du1,
            company_name="Nepal Can Move Pvt. Ltd.",
        )
        dp2 = DeliveryPartner.objects.create(
            user=du2,
            company_name="Express Delivery Pvt. Ltd.",
        )

        # delivery partner addresses
        dp_a1 = Address.objects.create(
            name="Nepal Can Move Office",
            latitude=27.6846068368187,
            longitude=85.3478503188922,
        )

        dp_a2 = Address.objects.create(
            name="Express Delivery Office",
            latitude=27.6846068368187,
            longitude=85.4478503188922,
        )

        dp1.addresses.add(dp_a1)
        dp2.addresses.add(dp_a2)

        print("Created delivery partners", dp1, dp2)

        # Create delivery request
        r1 = DeliveryRequest.objects.create(
            description="Send documents to Jhapa",
            requester=bp1,
            receiver_name="Manish Thapa",
            receiver_address="Jhapa, Bhadrapur, Campus Mode, Lalmati Tole",
        )
        r2 = DeliveryRequest.objects.create(
            description="Send documents to Karnali",
            requester=bp2,
            receiver_name="Curious Thapa",
            receiver_address="Karnali khola xeu",
        )

        print("Created delivery request", r1, r2)

        self.stdout.write(self.style.SUCCESS("Successfully seeded example data."))
