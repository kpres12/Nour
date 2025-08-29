#!/usr/bin/env python3
"""
Generate sample CSV files for Nour demo
"""

import csv
import os
from datetime import datetime, timedelta
import random

def generate_deals_csv():
    """Generate sample deals data"""
    deals = [
        {
            'deal_id': 'DEAL001',
            'account': 'Acme Corp',
            'amount': 50000,
            'stage': 'prospecting',
            'created_at': '2024-01-15',
            'closed_at': '',
            'owner': 'John Smith',
            'touches': 3
        },
        {
            'deal_id': 'DEAL002',
            'account': 'TechStart',
            'amount': 75000,
            'stage': 'negotiation',
            'created_at': '2024-01-10',
            'closed_at': '',
            'owner': 'Sarah Johnson',
            'touches': 8
        },
        {
            'deal_id': 'DEAL003',
            'account': 'Global Inc',
            'amount': 120000,
            'stage': 'closed_won',
            'created_at': '2024-01-05',
            'closed_at': '2024-02-15',
            'owner': 'Mike Davis',
            'touches': 12
        },
        {
            'deal_id': 'DEAL004',
            'account': 'Innovate Co',
            'amount': 90000,
            'stage': 'proposal',
            'created_at': '2024-01-20',
            'closed_at': '',
            'owner': 'Lisa Brown',
            'touches': 6
        },
        {
            'deal_id': 'DEAL005',
            'account': 'Enterprise Ltd',
            'amount': 200000,
            'stage': 'negotiation',
            'created_at': '2024-01-12',
            'closed_at': '',
            'owner': 'Tom Wilson',
            'touches': 10
        }
    ]
    
    filename = 'deals.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['deal_id', 'account', 'amount', 'stage', 'created_at', 'closed_at', 'owner', 'touches']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for deal in deals:
            writer.writerow(deal)
    
    print(f"Generated {filename} with {len(deals)} deals")

def generate_invoices_csv():
    """Generate sample invoices data"""
    invoices = [
        {
            'invoice_id': 'INV001',
            'account': 'Acme Corp',
            'amount': 50000,
            'issued_at': '2024-01-15',
            'due_at': '2024-02-15',
            'paid_at': '',
            'terms': 'net30'
        },
        {
            'invoice_id': 'INV002',
            'account': 'TechStart',
            'amount': 75000,
            'issued_at': '2024-01-10',
            'due_at': '2024-02-10',
            'paid_at': '2024-02-08',
            'terms': 'net30'
        },
        {
            'invoice_id': 'INV003',
            'account': 'Global Inc',
            'amount': 120000,
            'issued_at': '2024-01-05',
            'due_at': '2024-02-05',
            'paid_at': '2024-02-03',
            'terms': 'net30'
        },
        {
            'invoice_id': 'INV004',
            'account': 'Innovate Co',
            'amount': 90000,
            'issued_at': '2024-01-20',
            'due_at': '2024-02-20',
            'paid_at': '',
            'terms': 'net30'
        },
        {
            'invoice_id': 'INV005',
            'account': 'Enterprise Ltd',
            'amount': 200000,
            'issued_at': '2024-01-12',
            'due_at': '2024-02-12',
            'paid_at': '',
            'terms': 'net30'
        }
    ]
    
    filename = 'invoices.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['invoice_id', 'account', 'amount', 'issued_at', 'due_at', 'paid_at', 'terms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for invoice in invoices:
            writer.writerow(invoice)
    
    print(f"Generated {filename} with {len(invoices)} invoices")

def generate_tickets_csv():
    """Generate sample support tickets data"""
    tickets = [
        {
            'ticket_id': 'TICKET001',
            'account': 'Acme Corp',
            'opened_at': '2024-01-20',
            'severity': 'high',
            'status': 'open',
            'description': 'Login issues'
        },
        {
            'ticket_id': 'TICKET002',
            'account': 'TechStart',
            'opened_at': '2024-01-18',
            'severity': 'medium',
            'status': 'resolved',
            'description': 'Feature request'
        },
        {
            'ticket_id': 'TICKET003',
            'account': 'Global Inc',
            'opened_at': '2024-01-16',
            'severity': 'low',
            'status': 'closed',
            'description': 'Documentation question'
        },
        {
            'ticket_id': 'TICKET004',
            'account': 'Innovate Co',
            'opened_at': '2024-01-22',
            'severity': 'high',
            'status': 'open',
            'description': 'Performance problems'
        },
        {
            'ticket_id': 'TICKET005',
            'account': 'Enterprise Ltd',
            'opened_at': '2024-01-19',
            'severity': 'medium',
            'status': 'open',
            'description': 'Integration help'
        }
    ]
    
    filename = 'tickets.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ticket_id', 'account', 'opened_at', 'severity', 'status', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for ticket in tickets:
            writer.writerow(ticket)
    
    print(f"Generated {filename} with {len(tickets)} tickets")

def main():
    """Generate all sample CSV files"""
    print("🚀 Generating sample CSV files for Nour demo...")
    print()
    
    generate_deals_csv()
    generate_invoices_csv()
    generate_tickets_csv()
    
    print()
    print("✅ All sample CSV files generated successfully!")
    print()
    print("📁 Files created:")
    print("   - deals.csv (5 deals)")
    print("   - invoices.csv (5 invoices)")
    print("   - tickets.csv (5 support tickets)")
    print()
    print("💡 You can now upload these files to the Nour platform")
    print("   to test the data ingestion and entity resolution features.")

if __name__ == "__main__":
    main()
