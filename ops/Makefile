.PHONY: help demo start stop clean build logs

help: ## Show this help message
	@echo "Nour - Narrative Intelligence Platform"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

demo: ## Run the complete demo (start services, setup data, generate narratives)
	@echo "🚀 Starting Nour demo..."
	@echo "📦 Building and starting services..."
	@docker-compose up -d --build
	@echo "⏳ Waiting for services to be ready..."
	@sleep 30
	@echo "🗄️  Running database migrations..."
	@docker-compose exec backend alembic upgrade head
	@echo "📊 Setting up demo data..."
	@docker-compose exec backend python -c "
import sys
sys.path.append('/app')
from app.core.db import engine
from app.core.models import Base
Base.metadata.create_all(bind=engine)
print('Database tables created')
"
	@echo "✨ Demo is ready!"
	@echo ""
	@echo "🌐 Access the application:"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "🔑 Use any email/password to login (demo mode)"

start: ## Start all services
	@echo "🚀 Starting Nour services..."
	@docker-compose up -d

stop: ## Stop all services
	@echo "🛑 Stopping Nour services..."
	@docker-compose down

clean: ## Stop services and remove all data
	@echo "🧹 Cleaning up Nour services and data..."
	@docker-compose down -v
	@docker system prune -f

build: ## Build all services
	@echo "🔨 Building Nour services..."
	@docker-compose build

logs: ## Show logs from all services
	@docker-compose logs -f

backend-logs: ## Show backend logs
	@docker-compose logs -f backend

frontend-logs: ## Show frontend logs
	@docker-compose logs -f frontend

db-logs: ## Show database logs
	@docker-compose logs -f postgres

shell: ## Open shell in backend container
	@docker-compose exec backend bash

db-shell: ## Open PostgreSQL shell
	@docker-compose exec postgres psql -U nour -d nour

status: ## Show service status
	@docker-compose ps

restart: ## Restart all services
	@echo "🔄 Restarting Nour services..."
	@docker-compose restart

migrate: ## Run database migrations
	@echo "🗄️  Running database migrations..."
	@docker-compose exec backend alembic upgrade head

seed: ## Seed demo data
	@echo "🌱 Seeding demo data..."
	@docker-compose exec backend python -c "
import sys
sys.path.append('/app')
from app.core.db import engine
from app.core.models import Base, Organization, Dataset
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Create demo organization
org = Organization(name='Demo Organization', domain='demo.nour.com')
session.add(org)
session.commit()

# Create demo datasets
datasets = [
    Dataset(name='Sales Data', source_type='csv', acl_tag='sales', org_id=org.id),
    Dataset(name='Invoice Data', source_type='csv', acl_tag='finance', org_id=org.id),
    Dataset(name='Support Tickets', source_type='csv', acl_tag='support', org_id=org.id)
]
for dataset in datasets:
    session.add(dataset)
session.commit()

print('Demo data seeded successfully')
"
