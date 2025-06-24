# Fashion Trend Discovery Platform

A modern web application that analyzes TikTok data to identify trending fashion brands and styles, providing real-time insights through a beautiful consumer-facing interface.

## 🏗️ Cost-Effective Architecture

This platform is designed to be **inexpensive to run and maintain** while still demonstrating technical excellence:

- **Frontend**: Next.js 14 deployed on Vercel (free tier)
- **Backend**: FastAPI deployed on Railway/Render (free tier)
- **Database**: PostgreSQL on Railway/Render (free tier)
- **Caching**: Redis on Upstash (free tier)
- **ML Pipeline**: Hugging Face Spaces (free tier)
- **Data Collection**: Serverless functions with rate limiting
- **Deployment**: Zero-config deployments with automatic scaling

## 💰 Cost Breakdown

### Free Tier Services (Monthly Cost: $0)
- **Vercel**: Hosting for Next.js frontend
- **Railway/Render**: Backend API hosting
- **Upstash**: Redis caching (10,000 requests/day)
- **Hugging Face**: ML model hosting
- **GitHub**: Code repository and CI/CD

### Optional Paid Services (If you scale)
- **Railway Pro**: $5/month for more resources
- **Upstash Pro**: $10/month for higher limits
- **Custom Domain**: $12/year

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- Git

### Local Development Setup

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd tiktok-analysis
   ```

2. **Setup the backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

3. **Launch the frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
tiktok-analysis/
├── backend/                 # FastAPI backend with ML integration
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and utilities
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── ml/             # Machine learning models
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Next.js web application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml      # Local development only
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/fashion_trends
REDIS_URL=redis://localhost:6379
TIKTOK_API_KEY=your_tiktok_api_key
TIKTOK_API_SECRET=your_tiktok_api_secret
SECRET_KEY=your_secret_key
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deployment (Free!)

### Frontend Deployment (Vercel)
```bash
# Connect your GitHub repo to Vercel
# Vercel will automatically deploy on every push
npm run build  # Vercel runs this automatically
```

### Backend Deployment (Railway)
```bash
# 1. Push code to GitHub
git push origin main

# 2. Connect Railway to your GitHub repo
# 3. Railway automatically deploys from main branch
```

### Database Setup
- Railway provides PostgreSQL with free tier
- Upstash provides Redis with free tier
- No manual database management needed

## 📊 Features

### Core Functionality
- **Real-time Trend Detection**: Analyze TikTok videos for fashion trends
- **Brand Recognition**: Identify and track fashion brands
- **Style Classification**: Categorize clothing styles and aesthetics
- **Interactive Dashboard**: Beautiful UI with real-time updates
- **Search & Filter**: Find specific trends, brands, or styles
- **Historical Analysis**: View trend evolution over time

### Technical Highlights
- **Serverless Architecture**: Pay only for what you use
- **Async Processing**: Handle multiple video analysis requests
- **Caching Strategy**: Redis for API response caching
- **Rate Limiting**: Respect TikTok API limits
- **Error Handling**: Robust error management and logging
- **Responsive Design**: Mobile-first approach
- **Type Safety**: Full TypeScript coverage

## 💡 Cost Optimization Strategies

### 1. **Serverless Functions**
- Use Vercel Functions for data processing
- Pay only when functions are called
- Automatic scaling up/down

### 2. **Caching Strategy**
- Cache API responses in Redis
- Reduce database queries
- Use CDN for static assets

### 3. **Database Optimization**
- Use connection pooling
- Implement proper indexing
- Archive old data to reduce storage

### 4. **ML Model Optimization**
- Use lightweight models for inference
- Cache model predictions
- Batch processing when possible

### 5. **API Rate Limiting**
- Respect external API limits
- Implement intelligent retry logic
- Use webhooks when available

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## 📈 Performance

- **API Response Time**: < 500ms for cached responses
- **ML Inference**: < 3 seconds per video analysis
- **Real-time Updates**: WebSocket connections for live data
- **Database Queries**: Optimized with proper indexing

## 🔒 Security

- Input validation and sanitization
- Rate limiting on API endpoints
- CORS configuration
- Environment variable management
- SQL injection prevention

## 🎯 Why This Architecture?

### Perfect for Portfolio Projects:
- **Demonstrates Full-Stack Skills**: Frontend, backend, database, ML
- **Modern Tech Stack**: Next.js, FastAPI, PostgreSQL, Redis
- **Real-world Problem**: Fashion trend analysis is relatable and interesting
- **Scalable Foundation**: Easy to add features as you grow
- **Cost-Effective**: Can run for free or very cheap

### Technical Depth:
- **Async Programming**: FastAPI's async/await patterns
- **Database Design**: Proper schema with relationships
- **API Design**: RESTful endpoints with OpenAPI documentation
- **State Management**: React hooks and context
- **Styling**: Modern CSS with Tailwind
- **Testing**: Unit and integration tests

### Business Value:
- **User-Facing**: Real people can use and benefit from it
- **Data-Driven**: Shows ability to work with real data
- **Performance**: Demonstrates optimization skills
- **UX Focus**: Shows attention to user experience
- **Cost-Aware**: Shows understanding of business constraints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Create an issue in the GitHub repository
- Check the [documentation](docs/)
- Review the [API documentation](http://localhost:8000/docs)

## 🎯 Future Enhancements

- [ ] User authentication and profiles
- [ ] Email notifications for trend alerts
- [ ] Mobile app (React Native)
- [ ] Advanced ML models
- [ ] Social media integration
- [ ] E-commerce partnerships

## 💰 Cost Monitoring

### Free Tier Limits to Watch:
- **Vercel**: 100GB bandwidth/month
- **Railway**: $5 credit/month
- **Upstash**: 10,000 requests/day
- **Hugging Face**: 30,000 requests/month

### Scaling Up (When Needed):
- **Railway Pro**: $5/month for more resources
- **Upstash Pro**: $10/month for higher limits
- **Custom Domain**: $12/year
- **Additional Services**: Only when you have users! 