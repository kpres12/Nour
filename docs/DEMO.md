# Nour Demo Guide

This guide will walk you through setting up and running the Nour platform with sample data to demonstrate the complete narrative intelligence workflow.

## 🚀 Quick Start

### 1. Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### 2. Start the Demo
```bash
# Clone the repository
git clone <your-repo-url>
cd Nour

# Navigate to ops directory
cd ops

# Run the complete demo
make demo
```

This command will:
- Build and start all services (PostgreSQL, Backend, Frontend)
- Set up the database with required tables
- Create a demo organization
- Seed initial datasets

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Login
Use any email and password - the system will create a demo organization automatically.

## 📊 Sample Data

The demo includes sample datasets that demonstrate the platform's capabilities:

### Sales Data (deals.csv)
```csv
deal_id,account,amount,stage,created_at,closed_at,owner,touches
DEAL001,Acme Corp,50000,prospecting,2024-01-15,,John Smith,3
DEAL002,TechStart,75000,negotiation,2024-01-10,,Sarah Johnson,8
DEAL003,Global Inc,120000,closed_won,2024-01-05,2024-02-15,Mike Davis,12
DEAL004,Innovate Co,90000,proposal,2024-01-20,,Lisa Brown,6
DEAL005,Enterprise Ltd,200000,negotiation,2024-01-12,,Tom Wilson,10
```

### Invoice Data (invoices.csv)
```csv
invoice_id,account,amount,issued_at,due_at,paid_at,terms
INV001,Acme Corp,50000,2024-01-15,2024-02-15,,net30
INV002,TechStart,75000,2024-01-10,2024-02-10,2024-02-08,net30
INV003,Global Inc,120000,2024-01-05,2024-02-05,2024-02-03,net30
INV004,Innovate Co,90000,2024-01-20,2024-02-20,,net30
INV005,Enterprise Ltd,200000,2024-01-12,2024-02-12,,net30
```

### Support Tickets (tickets.csv)
```csv
ticket_id,account,opened_at,severity,status,description
TICKET001,Acme Corp,2024-01-20,high,open,Login issues
TICKET002,TechStart,2024-01-18,medium,resolved,Feature request
TICKET003,Global Inc,2024-01-16,low,closed,Documentation question
TICKET004,Innovate Co,2024-01-22,high,open,Performance problems
TICKET005,Enterprise Ltd,2024-01-19,medium,open,Integration help
```

## 🔄 Demo Workflow

### Step 1: Data Ingestion
1. Go to **Sources** page
2. Create a new dataset (e.g., "Sales Data")
3. Upload the sample CSV files
4. Start ingestion process

### Step 2: Entity Resolution
1. Go to **Entities** page
2. Run entity resolution on your datasets
3. View resolved entities (companies, deals, invoices)

### Step 3: Signal Computation
1. Go to **Signals** page
2. Compute signals for the last 90 days
3. View generated business metrics and anomalies

### Step 4: Rule Evaluation
1. Go to **Playbooks** page
2. Create business rules (e.g., late invoice alerts)
3. Evaluate rules against current signals

### Step 5: Narrative Generation
1. Go to **Narratives** page
2. Auto-generate narratives based on signals and rules
3. View AI-generated insights and recommendations
4. Export narratives to Markdown or JSON

## 🎯 Expected Outcomes

After running the complete demo, you should see:

- **3+ datasets** created and populated
- **10+ entities** resolved from the sample data
- **3+ signals** computed (pipeline velocity, invoice risk, deal patterns)
- **2+ narratives** generated with actionable insights
- **Export functionality** working for narratives

## 🧪 Testing the Platform

### Test Data Upload
```bash
# Navigate to the backend container
make shell

# Check uploaded files
ls -la uploads/
```

### Test API Endpoints
```bash
# Test authentication
curl -X POST "http://localhost:8000/api/v1/auth/demo-login"

# Test signals computation
curl -X POST "http://localhost:8000/api/v1/signals/compute" \
  -H "Authorization: Bearer <your-token>"
```

### Test Database
```bash
# Connect to PostgreSQL
make db-shell

# View tables
\dt

# Check data
SELECT * FROM organization;
SELECT * FROM dataset;
```

## 🔧 Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   # Check service status
   make status
   
   # View logs
   make logs
   ```

2. **Database connection issues**
   ```bash
   # Check database logs
   make db-logs
   
   # Restart services
   make restart
   ```

3. **Frontend not loading**
   ```bash
   # Check frontend logs
   make frontend-logs
   
   # Rebuild frontend
   make build
   ```

### Reset Demo
```bash
# Clean everything and restart
make clean
make demo
```

## 📈 Next Steps

After running the demo:

1. **Explore the API** at http://localhost:8000/docs
2. **Upload your own data** and see how the platform handles it
3. **Create custom rules** for your business logic
4. **Integrate with external systems** using the connector framework
5. **Enable LLM features** by setting `LLM_ENABLED=true`

## 🎉 Demo Success Criteria

✅ **MVP Acceptance Criteria Met:**
- Upload 3+ CSVs and ingest into ontology
- Compute 3+ signals and evaluate 2+ rules  
- Generate 2+ narratives with evidence and actions
- Export narratives to Markdown
- Multi-tenant with basic RBAC
- End-to-end demo in <5 minutes locally

The platform is now ready for production use and further development!
