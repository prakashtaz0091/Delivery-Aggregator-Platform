from django.contrib import admin
from apis.models import BusinessPartner, DeliveryPartner, DeliveryRequest, Address
from django.utils.html import format_html


class AddressAdmin(admin.ModelAdmin):
    list_display = ["name", "coordinates", "map_url"]

    def coordinates(self, obj):
        return f"{obj.latitude}, {obj.longitude}"

    def map_url(self, obj):
        return format_html(
            '<a href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">{}</a>',
            obj.latitude,
            obj.longitude,
            "View on Google Maps",
        )


class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ["user", "business_name", "address"]

    def address(self, obj):
        addresses = obj.addresses.all()
        links = [
            format_html(
                '<a href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">{}</a>',
                address.latitude,
                address.longitude,
                address.name,
            )
            for address in addresses
        ]
        return format_html(", ".join(links))


class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ["user", "company_name", "address"]

    def address(self, obj):
        addresses = obj.addresses.all()
        links = [
            format_html(
                '<a href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">{}</a>',
                address.latitude,
                address.longitude,
                address.name,
            )
            for address in addresses
        ]
        return format_html(", ".join(links))


class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "requester",
        "receiver_name",
        "receiver_address",
        "status",
        "delivery_partner",
        "pending_sync",
    ]

    def requester(self, obj):
        return obj.requester.business_name


admin.site.register(BusinessPartner, BusinessPartnerAdmin)
admin.site.register(DeliveryPartner, DeliveryPartnerAdmin)
admin.site.register(DeliveryRequest, DeliveryRequestAdmin)
admin.site.register(Address, AddressAdmin)
