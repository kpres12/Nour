# Nour Architecture Overview

This document provides a comprehensive overview of the Nour platform architecture, including system design, components, and data flow.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   PostgreSQL    │
│   (React.js)    │◄──►│   (FastAPI)     │◄──►│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │   Core Services │    │   Data Storage  │
│   (Chrome, etc) │    │   & Business    │    │   & Migrations  │
│                 │    │   Logic         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Technology Stack

### Frontend
- **Framework**: React.js 18 (JavaScript only, no TypeScript)
- **Build Tool**: Vite
- **Styling**: CSS with modern design system
- **State Management**: React Context + Hooks
- **Routing**: React Router v6

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with PyJWT
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Entity Resolution**: RapidFuzz for fuzzy matching
- **Rule Engine**: Custom YAML/JSON-based engine

### Database
- **Primary**: PostgreSQL 15
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Development**: Hot-reload enabled
- **Production Ready**: Environment-based configuration

## 📊 Data Model

### Core Entities

```
Organization (Multi-tenant root)
├── Dataset (Data sources)
│   └── RawRecord (Ingested data)
├── Entity (Resolved business entities)
│   ├── Link (Entity relationships)
│   └── Event (Business activities)
├── Signal (Computed metrics)
├── Rule (Business logic)
├── Narrative (Generated insights)
└── AuditLog (System audit trail)
```

### Key Relationships

- **Organization** → **Dataset** (1:many)
- **Dataset** → **RawRecord** (1:many)
- **Organization** → **Entity** (1:many)
- **Entity** → **Link** (1:many, both directions)
- **Entity** → **Event** (1:many)
- **Organization** → **Signal** (1:many)
- **Organization** → **Rule** (1:many)
- **Organization** → **Narrative** (1:many)

## 🔄 Data Flow

### 1. Data Ingestion
```
CSV/API → Upload/Connector → RawRecord → Processing → Entity Resolution
```

### 2. Signal Computation
```
Entity Data → Signal Service → Business Logic → Signal Storage → Rule Evaluation
```

### 3. Narrative Generation
```
Signals + Rules → Rule Engine → Template Engine → Narrative Service → Export
```

## 🏛️ Component Architecture

### Backend Services

#### Core Services
- **EntityResolver**: Fuzzy matching and entity resolution
- **SignalService**: Business metric computation
- **RuleEngine**: YAML/JSON rule evaluation
- **NarrativeService**: Insight generation and templating

#### API Layers
- **Authentication**: JWT-based auth with org context
- **Data Sources**: File upload and connector management
- **Ingestion**: Data processing and storage
- **Entities**: Entity CRUD and search
- **Signals**: Metric computation and management
- **Playbooks**: Rule management and evaluation
- **Narratives**: Insight generation and export

### Frontend Components

#### Layout Components
- **Navbar**: Navigation and user controls
- **Layout**: Page structure and routing

#### Feature Components
- **Dashboard**: Overview and quick actions
- **Sources**: Data source management
- **Entities**: Entity browsing and search
- **Signals**: Metric visualization
- **Playbooks**: Rule management
- **Narratives**: Insight display and export

#### Shared Components
- **Forms**: Reusable form components
- **Cards**: Content display components
- **Modals**: Overlay dialogs

## 🔐 Security Architecture

### Multi-tenancy
- **Organization Isolation**: All data scoped by `org_id`
- **Row-level Security**: Database-level tenant isolation
- **API Security**: JWT tokens with org context

### Authentication & Authorization
- **JWT Tokens**: Secure, stateless authentication
- **Role-based Access**: Viewer, Analyst, Admin roles
- **API Security**: Bearer token authentication

### Data Security
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **File Upload Security**: Type and size validation

## 📈 Scalability Considerations

### Horizontal Scaling
- **Stateless Backend**: FastAPI services can be scaled horizontally
- **Database Connection Pooling**: Efficient connection management
- **Microservice Ready**: Service boundaries for future decomposition

### Performance Optimization
- **Database Indexing**: Strategic indexes on frequently queried fields
- **Caching Strategy**: Redis integration ready
- **Async Processing**: Background tasks for heavy operations

### Data Volume Handling
- **Batch Processing**: Efficient bulk operations
- **Pagination**: API-level result limiting
- **Streaming Ready**: Kafka integration prepared

## 🔌 Integration Points

### External Systems
- **CRM Systems**: Salesforce, HubSpot connectors
- **ERP Systems**: QuickBooks, NetSuite adapters
- **Support Systems**: Zendesk, ServiceNow integration
- **Analytics**: Google Analytics, Mixpanel feeds

### Data Formats
- **CSV/Excel**: Direct file uploads
- **JSON APIs**: RESTful API consumption
- **Webhooks**: Real-time data ingestion
- **Database**: Direct database connections

### Export Capabilities
- **Markdown**: Human-readable reports
- **PDF**: Professional document generation
- **JSON**: API consumption format
- **CSV**: Data analysis export

## 🚀 Deployment Architecture

### Development Environment
```
Local Docker Compose
├── PostgreSQL (local)
├── Backend (hot-reload)
└── Frontend (hot-reload)
```

### Production Environment
```
Load Balancer
├── Frontend (CDN/Static hosting)
├── Backend (Multiple instances)
└── Database (Primary + Replicas)
```

### Environment Configuration
- **Development**: Local Docker setup
- **Staging**: Production-like environment
- **Production**: Cloud deployment ready

## 🔮 Future Architecture

### Planned Enhancements
- **Graph Database**: Neo4j integration for deep relationship analysis
- **Streaming**: Kafka integration for real-time processing
- **LLM Integration**: OpenAI/GPT integration for advanced insights
- **Microservices**: Service decomposition for scale
- **Kubernetes**: Container orchestration for production

### Extensibility
- **Plugin Architecture**: Custom connector development
- **API Versioning**: Backward-compatible API evolution
- **Custom Rules**: Advanced rule engine capabilities
- **Workflow Engine**: Business process automation

## 📋 Architecture Decisions

### Why FastAPI?
- **Performance**: High-performance async framework
- **Type Safety**: Pydantic validation and type checking
- **Documentation**: Automatic OpenAPI/Swagger generation
- **Modern Python**: Async/await support and modern patterns

### Why React.js (No TypeScript)?
- **MVP Focus**: Faster development for initial release
- **Team Familiarity**: JavaScript expertise common
- **Future Migration**: TypeScript can be added incrementally
- **Ecosystem**: Rich JavaScript ecosystem and libraries

### Why PostgreSQL?
- **Reliability**: ACID compliance and data integrity
- **JSON Support**: Native JSONB for flexible data storage
- **Performance**: Excellent query performance and indexing
- **Scalability**: Handles large datasets efficiently

### Why Docker?
- **Consistency**: Same environment across development and production
- **Isolation**: Clean separation of services
- **Deployment**: Easy deployment and scaling
- **Development**: Quick setup and teardown

## 🎯 Architecture Principles

1. **12-Factor App**: Environment-based configuration
2. **Separation of Concerns**: Clear service boundaries
3. **Data Consistency**: ACID compliance and validation
4. **Security First**: Multi-tenant isolation and authentication
5. **Performance**: Efficient data processing and caching
6. **Scalability**: Horizontal scaling and microservice ready
7. **Maintainability**: Clean code and comprehensive testing
8. **Extensibility**: Plugin architecture and API versioning

This architecture provides a solid foundation for the Nour platform while maintaining flexibility for future enhancements and scaling requirements.
