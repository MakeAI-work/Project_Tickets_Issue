# Deploying to Render

This guide covers deploying the Atlan AI Helpdesk system to Render.com with both backend API and frontend static site.

## 🚀 Quick Deploy Steps

### 1. Prepare Your Repository

1. **Push to GitHub** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Verify Files**: Ensure these files exist in your repo:
   - `render.yaml` (deployment configuration)
   - `backend/requirements.txt` (Python dependencies)
   - `frontend/package.json` (Node.js dependencies)

### 2. Deploy on Render

1. **Sign up/Login** to [Render.com](https://render.com)

2. **Connect GitHub**: 
   - Go to Dashboard → "New" → "Blueprint"
   - Connect your GitHub account
   - Select your repository

3. **Configure Environment Variables**:
   In Render dashboard, set these environment variables for the backend service:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ACTIVELOOP_ORG=your_activeloop_org (optional)
   DEEPLAKE_TOKEN=your_deeplake_token (optional)
   ```

4. **Deploy**: 
   - Render will automatically detect `render.yaml`
   - Click "Apply" to start deployment
   - Wait for both services to build and deploy

### 3. Configure Frontend API Connection

After backend deploys, you'll get a backend URL like: `https://atlan-helpdesk-api.onrender.com`

1. **Set Frontend Environment Variable**:
   In Render dashboard, add to frontend service:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```

2. **Redeploy Frontend**: Trigger a new deployment to pick up the environment variable.

## 📋 Manual Deployment (Alternative)

If you prefer manual setup instead of Blueprint:

### Backend Service
1. **New Web Service** → Connect GitHub repo
2. **Settings**:
   - Name: `atlan-helpdesk-api`
   - Environment: `Python 3`
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: Leave empty

### Frontend Service  
1. **New Static Site** → Connect same GitHub repo
2. **Settings**:
   - Name: `atlan-helpdesk-frontend`
   - Build Command: `cd frontend && npm ci && npm run build`
   - Publish Directory: `frontend/build`
   - Root Directory: Leave empty

## 🔧 Post-Deployment Setup

### 1. Data Ingestion
After backend is deployed, you need to populate the vector databases:

**Option A: Local Ingestion** (Recommended)
```bash
# Run locally, will populate cloud DeepLake
cd backend
python deeplake_ingest.py
```

**Option B: One-time Render Job**
- Create a new "Background Worker" service
- Use same repo and environment variables
- Start Command: `cd backend && python deeplake_ingest.py`
- Run once, then delete the service

### 2. Test Deployment
1. Visit your frontend URL: `https://your-frontend-name.onrender.com`
2. Submit a test ticket to verify the full pipeline works
3. Check that classification and RAG responses are working

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**:
- Check environment variables are set correctly
- Verify `requirements.txt` has all dependencies
- Check logs in Render dashboard

**Frontend can't connect to backend**:
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings if needed
- Ensure backend is deployed and healthy

**RAG responses are empty**:
- Run data ingestion script
- Check DeepLake credentials
- Verify OpenAI API key is working

**Build failures**:
- Check Node.js/Python versions in logs
- Verify all dependencies are listed
- Check for any missing files

### Performance Optimization

**Free Tier Limitations**:
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Consider upgrading for production use

**Speed Improvements**:
- Use local DeepLake storage for faster retrieval
- Implement caching for frequently accessed data
- Optimize chunk sizes and retrieval limits

## 🔒 Security Considerations

- Never commit API keys to repository
- Use Render's environment variables for secrets
- Enable HTTPS (automatic on Render)
- Consider IP restrictions for admin endpoints

## 📊 Monitoring

- Use Render's built-in logs and metrics
- Monitor API response times
- Track error rates and user activity
- Set up alerts for service downtime

## 💰 Cost Estimation

**Free Tier** (suitable for demo/testing):
- Backend: 750 hours/month free
- Frontend: Unlimited bandwidth
- Automatic sleep after inactivity

**Paid Plans** (for production):
- Starter: $7/month per service
- Standard: $25/month per service
- Pro: $85/month per service

## 🔄 Updates and Maintenance

**Automatic Deployments**:
- Connected to GitHub main branch
- Auto-deploys on push
- Can disable for manual control

**Manual Updates**:
- Use Render dashboard "Manual Deploy"
- Useful for environment variable changes
- Good for testing before merging

---

Your Atlan AI Helpdesk system is now deployed and accessible worldwide! 🎉
