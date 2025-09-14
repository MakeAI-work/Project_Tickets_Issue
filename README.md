# Atlan AI Helpdesk System

A sophisticated AI-powered helpdesk system that automatically classifies support tickets and provides intelligent responses using Retrieval-Augmented Generation (RAG). Built with React frontend, FastAPI backend, and integrated with Atlan's documentation ecosystem.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   React Frontend│    │  FastAPI Backend │    │   Vector Databases  │
│                 │    │                  │    │                     │
│ • Modern UI/UX  │◄──►│ • Classification │◄──►│ • DeepLake (docs)   │
│ • Ticket Cards  │    │ • RAG Pipeline   │    │ • DeepLake (dev)    │
│ • Real-time     │    │ • OpenAI GPT-4o  │    │ • OpenAI Embeddings │
│   Analysis      │    │                  │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  User Interface │    │   AI Components  │    │   Knowledge Base    │
│                 │    │                  │    │                     │
│ • Dashboard     │    │ • Classifier     │    │ • docs.atlan.com    │
│ • Filters       │    │ • RAG Engine     │    │ • developer.atlan   │
│ • Stats         │    │ • Retriever      │    │ • Preprocessed      │
│ • Submit Form   │    │                  │    │   Chunks            │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

## 🎯 Key Features

### Intelligent Ticket Classification
- **Multi-dimensional Analysis**: Automatically classifies tickets by topic, sentiment, and priority
- **Context-Aware**: Uses GPT-4o-mini for nuanced understanding of user intent
- **Real-time Processing**: Instant classification with structured JSON output

### Smart Response Generation
- **RAG Pipeline**: Retrieves relevant documentation before generating responses
- **Dual Knowledge Base**: Separate collections for user docs and developer resources
- **Source Attribution**: Provides citations and source URLs for transparency

### Modern Dashboard Interface
- **Premium UI/UX**: Glass-morphism design with smooth animations
- **Interactive Analytics**: Real-time stats with priority breakdown
- **Advanced Filtering**: Topic-based filtering with dynamic updates
- **Responsive Design**: Optimized for desktop and mobile experiences

## 🧠 AI Pipeline Design Decisions

### 1. Classification Strategy
**Decision**: Multi-output classification (topic + sentiment + priority)
**Trade-offs**:
- ✅ **Pros**: Rich metadata for routing and analytics
- ✅ **Pros**: Single API call for complete analysis
- ❌ **Cons**: More complex prompt engineering
- ❌ **Cons**: Higher token usage per request

### 2. RAG Architecture
**Decision**: Topic-based collection routing
**Trade-offs**:
- ✅ **Pros**: Specialized knowledge bases improve accuracy
- ✅ **Pros**: Faster retrieval with smaller, focused datasets
- ❌ **Cons**: Requires manual topic-to-collection mapping
- ❌ **Cons**: Potential for misclassification affecting retrieval

### 3. Vector Database Choice
**Decision**: DeepLake with OpenAI embeddings
**Trade-offs**:
- ✅ **Pros**: Managed infrastructure, easy scaling
- ✅ **Pros**: Built-in versioning and collaboration
- ❌ **Cons**: Network latency for cloud-hosted collections
- ❌ **Cons**: Vendor lock-in considerations

### 4. Model Selection
**Decision**: GPT-4o-mini for classification, GPT-4o-mini for generation
**Trade-offs**:
- ✅ **Pros**: Cost-effective while maintaining quality
- ✅ **Pros**: Fast response times for real-time UX
- ❌ **Cons**: Slightly lower accuracy vs. GPT-4
- ❌ **Cons**: Context window limitations for very long documents

## 🚀 Setup Instructions

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- OpenAI API key
- DeepLake account (optional for cloud storage)

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd atlan-helpdesk
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Environment Variables**
Create `.env` file in backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
ACTIVELOOP_ORG=your_activeloop_org  # Optional
DEEPLAKE_TOKEN=your_deeplake_token  # Optional
```

4. **Frontend Setup**
```bash
cd frontend
npm install
```

### Data Ingestion

1. **Ingest Documentation** (First time setup)
```bash
cd backend
python deeplake_ingest.py
```
This will:
- Crawl docs.atlan.com and developer.atlan.com
- Create vector embeddings
- Store in DeepLake collections

### Running the Application

1. **Start Backend Server**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

2. **Start Frontend Development Server**
```bash
cd frontend
npm start
```

3. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
atlan-helpdesk/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── tickets.py          # API endpoints
│   │   ├── core/
│   │   │   ├── classifier.py       # Ticket classification
│   │   │   ├── rag.py             # RAG pipeline
│   │   │   └── retriever.py       # Vector search
│   │   ├── data/
│   │   │   └── sample_tickets.json # Sample data
│   │   └── main.py                # FastAPI app
│   ├── deeplake_ingest.py         # Data ingestion script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewTicket.jsx      # Ticket submission form
│   │   │   └── TicketsTable.jsx   # Dashboard cards
│   │   ├── styles/
│   │   │   ├── App.css            # Main styles
│   │   │   └── badges.css         # Component styles
│   │   ├── App.js                 # Main application
│   │   └── api.js                 # API client
│   └── package.json
└── README.md
```

## 🔧 Configuration Options

### Backend Configuration
- **Model Selection**: Change models in `core/classifier.py` and `core/rag.py`
- **Collection Paths**: Update `COL_PATHS` in `core/retriever.py`
- **Classification Rules**: Modify prompts in `core/classifier.py`

### Frontend Configuration
- **API Endpoint**: Update `API_BASE_URL` in `src/api.js`
- **Styling**: Customize theme variables in `src/styles/App.css`
- **Components**: Modify React components in `src/components/`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing
1. Submit various ticket types through the UI
2. Verify classification accuracy
3. Check RAG responses for relevance
4. Test filtering and dashboard functionality

## 📊 Performance Considerations

### Optimization Strategies
- **Caching**: Vector stores are cached with `@lru_cache`
- **Chunking**: Documents split into 800-character chunks
- **Retrieval**: Limited to top-3 most relevant chunks
- **Model**: Using cost-effective GPT-4o-mini

### Scaling Recommendations
- **Horizontal Scaling**: Deploy multiple backend instances
- **Database Optimization**: Use local DeepLake for faster access
- **CDN**: Serve static frontend assets via CDN
- **Monitoring**: Implement logging and metrics collection

## 🔒 Security Notes

- Store API keys in environment variables
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Validate and sanitize user inputs
- Regular security audits of dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the GitHub Issues page
2. Review the API documentation at `/docs`
3. Contact the development team

---

Built with ❤️ for Atlan's AI-powered support ecosystem.
