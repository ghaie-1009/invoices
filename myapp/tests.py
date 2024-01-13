# tests.py

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceModelTestCase(TestCase):
    def test_create_invoice(self):
        invoice = Invoice.objects.create(date='2024-01-13', customer_name='Test Customer')
        self.assertEqual(invoice.__str__(), f"Invoice {invoice.id} - Test Customer")

    def test_create_invoice_detail(self):
        invoice = Invoice.objects.create(date='2024-01-13', customer_name='Test Customer')
        detail = InvoiceDetail.objects.create(invoice=invoice, description='Test Description', quantity=2, unit_price=10.00, price=20.00)
        self.assertEqual(detail.__str__(), f"Detail {detail.id} - Test Description - 20.00")

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {'date': '2024-01-13', 'customer_name': 'Test Customer'}
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_detail_data = {'description': 'Test Description', 'quantity': 2, 'unit_price': 10.00, 'price': 20.00}
        self.invoice_detail_data_invalid = {'description': 'Invalid Description', 'quantity': -1, 'unit_price': 10.00, 'price': 20.00}

    def test_create_invoice(self):
        response = self.client.post('/invoices/', self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_retrieve_invoice(self):
        response = self.client.get(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')

    def test_update_invoice(self):
        updated_data = {'date': '2024-01-14', 'customer_name': 'Updated Customer'}
        response = self.client.put(f'/invoices/{self.invoice.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, 'Updated Customer')

    def test_delete_invoice(self):
        response = self.client.delete(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_create_invoice_detail(self):
        response = self.client.post(f'/invoice_details/', {'invoice': self.invoice.id, **self.invoice_detail_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    def test_create_invoice_detail_invalid_data(self):
        response = self.client.post(f'/invoice_details/', {'invoice': self.invoice.id, **self.invoice_detail_data_invalid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
